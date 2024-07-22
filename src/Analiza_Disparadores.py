import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Si no tienes las stopwords de NLTK, necesitas descargarlas
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Definir stop words en español
stop_words_es = set(stopwords.words('spanish'))

# Cambio al directorio de datos
os.chdir("../data/")

# Cargo archivos CSV y elimino filas donde la columna "Keywords" es "NaN"
df_tsv = pd.read_csv("rules-2024.07.02-14.33.tsv", sep='\t', on_bad_lines='warn', index_col=False, encoding="latin1")
df_tsv = df_tsv.dropna(subset=['Keywords'])

# Elimino filas donde la columna "Active" es booleana y tiene valor FALSE
df_tsv = df_tsv[df_tsv['Active'] != False]

# Agrego una columna con la cantidad de veces que se encontró la cadena "\r\n" en "Keywords" y le sumo 1
df_tsv['frases_por_intencion'] = df_tsv['Keywords'].str.count(re.escape(r'\r\n')) + 1

# Ordeno el DataFrame por 'frases_por_intencion' en orden decreciente
df_tsv_sorted = df_tsv.sort_values(by='frases_por_intencion', ascending=False)

# Exporto el DataFrame con las columnas "Name", "ID", "Keywords" y "frases_por_intencion" en orden decreciente
df_tsv_sorted[['Name', 'ID', 'Keywords', 'frases_por_intencion']].to_csv("../frases_por_intencion.csv", sep=';', index=False, encoding='utf-8-sig')

# Función para eliminar stop words y limpiar caracteres no deseados
def clean_and_remove_stopwords(text):
    # Reemplazar caracteres no deseados por un espacio en blanco, excepto \r\n
    text = re.sub(r'[().,|?!¡¿]', ' ', text)
    # Tokenizar el texto
    words = word_tokenize(text, language='spanish')
    # Eliminar stop words
    words_filtered = [word for word in words if word.lower() not in stop_words_es]
    return ' '.join(words_filtered)

# Creo una nueva columna "Keywords_limpias" eliminando las stop words y saco simbolos molestos
df_tsv['Keywords_limpias'] = df_tsv['Keywords'].apply(clean_and_remove_stopwords)

# Calculo la cantidad de palabras totales en "Keywords_limpias"
df_tsv['word_count'] = df_tsv['Keywords_limpias'].apply(lambda x: len(word_tokenize(x, language='spanish')))

# Ordeno el DataFrame por 'word_count' en orden decreciente
df_tsv_sorted = df_tsv.sort_values(by='word_count', ascending=False)

# Exporto el DataFrame ordenado a un archivo CSV
df_tsv_sorted[['Name', 'ID', 'Keywords_limpias', 'word_count']].to_csv("../df_tsv_sorted.csv", sep=';', index=False, encoding='utf-8-sig')

# Suma de todos los valores en la columna 'word_count'
total_word_count = df_tsv_sorted['word_count'].sum()

# Generar un gráfico que muestre el número total de palabras
plt.figure(figsize=(8, 6))
plt.text(0.5, 0.5, f'Total de palabras:\n{total_word_count}', fontsize=16, ha='center', va='center')
plt.axis('off')  # Desactivar ejes para que solo muestre el texto
plt.savefig("../total_word_count.png", bbox_inches='tight', pad_inches=0.1)  # Guardar la imagen como PNG
plt.show()

#  FIN de calculo cantidad de palabras y cantidad de frases por intencion


# Creo una nueva columna con la lista de palabras, limpiando delimitadores y reemplazando \r\n por un espacio en blanco
df_tsv['keywords_list'] = df_tsv['Keywords'].apply(
    lambda x: [word.strip() for word in re.sub(r'[()]', '', str(x)).replace('|', ',').replace('\\r\\n', ', ').replace('.', ', ').replace('\\u201d', '  ').replace('\\u201c', '  ').replace('\\u2018', '  ').replace('\\u2019', '  ').split(',') if word.strip()]
)

# Creo un nuevo DataFrame con las columnas "Name", "ID" y 'keywords_list'
new_df = df_tsv[['Name', 'ID', 'keywords_list']]

# Creo un nuevo DataFrame con "ID", "Name" y "disparador"
expanded_df = new_df.explode('keywords_list').rename(columns={'keywords_list': 'disparador'})

# Análisis de frecuencia de la columna "disparador"
frequency_analysis = expanded_df['disparador'].value_counts().reset_index()
frequency_analysis.columns = ['disparador', 'frecuencia']

# Exporto el análisis de frecuencia a un archivo CSV
frequency_analysis.to_csv("../frequency_analysis.csv", sep=';', index=False, encoding='utf-8-sig')

# Identifico los 30 valores de mayor frecuencia y los 10 de menor frecuencia
top_30_frequent = frequency_analysis.head(30)
bottom_10_frequent = frequency_analysis.tail(10)

# Exporto los valores de mayor y menor frecuencia a archivos CSV
top_30_frequent.to_csv("../top_30_frequent.csv", sep=';', index=False, encoding='utf-8-sig')
bottom_10_frequent.to_csv("../bottom_10_frequent.csv", sep=';', index=False, encoding='utf-8-sig')

# Filtro el expanded_df para obtener solo los 30 disparadores más frecuentes
top_30_disparadores = top_30_frequent['disparador']
filtered_top_30_df = expanded_df[expanded_df['disparador'].isin(top_30_disparadores)]

# Guardo el DataFrame filtrado a un archivo CSV
filtered_top_30_df.to_csv("../top_30_disparadores_details.csv", sep=';', index=False, encoding='utf-8-sig')

# Filtro el expanded_df para obtener solo los 10 disparadores menos frecuentes
bottom_10_disparadores = bottom_10_frequent['disparador']
filtered_bottom_10_df = expanded_df[expanded_df['disparador'].isin(bottom_10_disparadores)]

# Exporto el DataFrame filtrado a un archivo CSV
filtered_bottom_10_df.to_csv("../bottom_10_disparadores_details.csv", sep=';', index=False, encoding='utf-8-sig')

# Filtro el expanded_df para obtener las filas donde "disparador" contiene la palabra "curso" pero no "consurso"
curso_df = expanded_df[expanded_df['disparador'].str.contains('curso', case=False, na=False)]
curso_df = curso_df[~curso_df['disparador'].str.contains('consurso', case=False, na=False)]

# Exporto el DataFrame filtrado a un archivo CSV
curso_df.to_csv("../curso_disparadores_details.csv", sep=';', index=False, encoding='utf-8-sig')


# Filtro el expanded_df para obtener las filas donde "disparador" contiene la palabra "paseo" pero no "consurso"
paseo_df = expanded_df[expanded_df['disparador'].str.contains('paseo', case=False, na=False)]
#paseo_df = paseo_df[~paseo_df['disparador'].str.contains('consurso', case=False, na=False)]

# Exporto el DataFrame filtrado a un archivo CSV
paseo_df.to_csv("../paseo_disparadores_details.csv", sep=';', index=False, encoding='utf-8-sig')



"""
# Graficos del análisis de frecuencia
plt.figure(figsize=(12, 8))
plt.bar(frequency_analysis['disparador'][:20], frequency_analysis['frecuencia'][:20])
plt.xlabel('Disparador')
plt.ylabel('Frecuencia')
plt.title('Análisis de Frecuencia de Disparadores')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../frequency_analysis.png")
plt.show()
"""

# 30 valores TOP de mayor frecuencia
plt.figure(figsize=(12, 8))
plt.bar(top_30_frequent['disparador'], top_30_frequent['frecuencia'])
plt.xlabel('Disparador')
plt.ylabel('Frecuencia')
plt.title('Top 30 Disparadores más Frecuentes')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../top_30_frequent.png")
plt.show()

# 10 valores de menor frecuencia
plt.figure(figsize=(12, 8))
plt.bar(bottom_10_frequent['disparador'], bottom_10_frequent['frecuencia'])
plt.xlabel('Disparador')
plt.ylabel('Frecuencia')
plt.title('Bottom 10 Disparadores menos Frecuentes')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("../bottom_10_frequent.png")
plt.show()

# Curva de frecuencia total
plt.figure(figsize=(12, 8))
sns.lineplot(data=frequency_analysis, x='disparador', y='frecuencia', marker='o')
plt.xlabel('Disparador')
plt.ylabel('Frecuencia')
plt.title('Curva de Frecuencia Total de Disparadores')
plt.xticks(rotation=45, ha='right')
#plt.tight_layout()
plt.savefig("../curva_frecuencia_total.png")
plt.show()

# Calculo de descriptores estadísticos
descriptive_stats = frequency_analysis['frecuencia'].describe()
descriptive_stats = descriptive_stats.apply(lambda x: round(x, 2))

# Calculo de la mediana
median_value = round(frequency_analysis['frecuencia'].median(), 2)

# Agrego la mediana a los descriptores estadísticos, no me venia en el paquete
descriptive_stats['median'] = median_value

# Exporto los descriptores estadísticos a un archivo CSV
descriptive_stats.to_csv("../descriptive_stats.csv", sep=';', encoding='utf-8-sig')

"""
# invento una nueva columna con la longitud de cada cadena en la columna "disparador"
expanded_df['length'] = expanded_df['disparador'].apply(len)

# Ordeno el DataFrame por la longitud de las cadenas de forma descendente
expanded_df_sorted = expanded_df.sort_values(by='length', ascending=False)

# armo un ranking basado en la longitud de las cadenas
expanded_df_sorted['ranking'] = expanded_df_sorted['length'].rank(method='dense', ascending=False).astype(int)

#Seleccionolas 30 primeras filas
top_30_longest = expanded_df_sorted.head(30)

# Exporto las 30 primeras filas a un archivo CSV
top_30_longest[['ID', 'Name', 'disparador', 'length', 'ranking']].to_csv("../top_30_longest_disparadores.csv", sep=';', index=False, encoding='utf-8-sig')
"""


"""
Percentiles: Los percentiles dividen un conjunto de datos en 100 partes iguales. El valor en el percentil 
𝑝 es el valor por debajo del cual cae el p% de los datos.
En otras palabras, si un valor se encuentra en el percentil 25,
significa que el 25% de los datos son menores o iguales a ese valor.
"""


