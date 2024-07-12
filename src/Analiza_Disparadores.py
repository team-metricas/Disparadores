import os
import pandas as pd
import sys
import re

# Cambio al directorio de datos
os.chdir("../data/")

# Cargo archivos CSV y elimino filas donde la columna "keywords" es "NaN"
df_tsv = pd.read_csv("rules-2024.07.02-14.33.tsv", sep='\t', on_bad_lines='warn', index_col=False, encoding="latin1")
df_tsv = df_tsv.dropna(subset=['Keywords'])

# Creouna nueva columna con la lista de palabras
df_tsv['keywords_list'] = df_tsv['Keywords'].apply(
    lambda x: [word.strip() for word in re.sub(r'[()]', '', str(x)).replace('|', ',').split(',') if word.strip()]
)

# Creo un nuevo DataFrame con las columnas "Name", "ID" y 'keywords_list'
new_df = df_tsv[['Name', 'ID', 'keywords_list']]

# Creo un nuevo DataFrame con "ID", "Name" y "disparador"
expanded_df = new_df.explode('keywords_list').rename(columns={'keywords_list': 'disparador'})

