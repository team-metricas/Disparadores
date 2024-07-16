import os
import pandas as pd
import sys
import re
import matplotlib.pyplot as plt

# Cambio al directorio de datos
os.chdir("../data/")

# Cargo archivos CSV y elimino filas donde la columna "Keywords" es "NaN"
df_tsv = pd.read_csv("rules-2024.07.02-14.33.tsv", sep='\t', on_bad_lines='warn', index_col=False, encoding="latin1")
df_tsv = df_tsv.dropna(subset=['Keywords'])

# Elimino filas donde la columna "Active" es booleana y tiene valor FALSE
df_tsv = df_tsv[df_tsv['Active'] != False]

# Creo una nueva columna con la lista de palabras, limpiando delimitadores y reemplazando \r\n por un espacio en blanco
df_tsv['keywords_list'] = df_tsv['Keywords'].apply(
    lambda x: [word.strip() for word in re.sub(r'[().]', '', str(x)).replace('|', ',').replace('\\r\\n', ', ').replace('.', ', ').replace('\\u201d', '  ').replace('\\u201c', '  ').replace('\\u2018', '  ').replace('\\u2019', '  ').split(',') if word.strip()]
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
curso_df = curso_df[~curso_df['disparador'].str.contains('concurso', case=False, na=False)]

# Exporto el DataFrame filtrado a un archivo CSV
curso_df.to_csv("../curso_disparadores_details.csv", sep=';', index=False, encoding='utf-8-sig')

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

# Calculo de descriptores estadísticos
descriptive_stats = frequency_analysis['frecuencia'].describe()
descriptive_stats = descriptive_stats.apply(lambda x: round(x, 2))

# Calculo de la mediana
median_value = round(frequency_analysis['frecuencia'].median(), 2)

# Agrego la mediana a los descriptores estadísticos
descriptive_stats['median'] = median_value

print(descriptive_stats)

# Guardar los descriptores estadísticos a un archivo CSV
descriptive_stats.to_csv("../descriptive_stats.csv", sep=';', encoding='utf-8-sig')

# Encuentra la moda de la columna 'disparador'
moda_disparadores = frequency_analysis.loc[frequency_analysis['frecuencia'].idxmax(), 'disparador']
print(f"La moda de la columna 'disparador' es: {moda_disparadores}")
