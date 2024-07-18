# Disparadores
Análisis cuantitativo de disparadores

Objetivos

1 - Separar cada uno de los disparadores (columna Keywords).

2 - Asignarle su rulename (Name) y su ID: Cada palabra clave se asociará con su rulename y su ID correspondiente. Esto será útil para conectar con el buscador de rulenames.

3 -Elaborar un análisis de la frecuencia de los disparadores: Con los datos preparados, se realizará un análisis para determinar cuántas veces se repite un disparador en el bot. Esto incluirá el cálculo del promedio y la mediana de las frecuencias.

4- Detalle de las 30 palabras más repetidas y las 10 menos repetidas: se proporcionará un resumen de las 30 palabras más comunes y las 10 menos comunes. Esto ayudará a identificar qué palabras clave se utilizan con más frecuencia y cuáles se utilizan con menos frecuencia.

Anexo.  

Dato 1: Cuantas Keywords diferentes tenemos  (es decir contar las palabras que separaste)   
 
Dato 2: Ejemplo: (cuando|que hay|que encuentro),(noche),(librerías)\r\n(noche),(librerías)  
Las frases están divididas por \r\n y lo que se necesita es contar la cantidad de frases por intención  y que se informe cuáles son las intenciones (siempre activas ) que más frases tienen 
 

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Características](#características)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)

### Instalación

#### Requisitos Previos

- Python 3.11 o superior
- pip

#### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/team-metricas/Disparadores

# Entrar al directorio del proyecto
cd src

# Instalar las dependencias
pip install pandas matplotlib seaborn nltk


# ejecutar el programa en /src
python Analiza_Disparadores.py

```

### Uso
 
En la carpeta `/data` se debe hallar el Archivo de input:
`rules-2024.07.02-14.33.tsv`.  



### Características  
**Analiza_Disparadores.py**  

Procesa el archivo TSV de la siguiente forma:  

Cuenta la cantidad de Frases por Intención de la columna `Keywords`, se toma como separador de frases \r\n y se crea el archivo `frases_por_intencion.csv`.    

Elimina las stop-words y simbolos `[().,|?!¡¿]` de la columna `Keywords`.  Suma la cantidad de palabras, crea un ranking decreciente y exporta el archivo `df_tsv_sorted.csv`.    
También se generá el archivo `total_word_count.png` con la cantidad total de palabras.    

Del campo `Keywords` reemplaza los simbolos `|,\r\n.` por el simbolo `,`.  Los simbolos `[()]` son eliminados. Luego de estas operaciones se arma una lista por cada fila son las palabras separadas por `,`.   
Se expande cada fila segun la cantidad de palabras que hayan quedado en la columna `Keywords` de forma tal de aislar los disparadores.    
Se crea la tabla de Frecuencias `frequency_analysis.csv`.   

Se Identifica los 30 valores de mayor frecuencia y los 10 de menor frecuencia. Con ellos se crean los archivos `top_30_frequent.csv` y `bottom_10_frequent.csv`.  
Para identificar los CUX a donde pertenecen los 30 de mayor frecuencia se crea el archivo `top_30_disparadores_details.csv`.  
Para identificar los CUX a donde pertenecen los 10 de menor frecuencia se crea el archivo `bottom_10_disparadores_details.csv`. 

En la sentencia: `curso_df = expanded_df[expanded_df['disparador'].str.contains('curso', case=False, na=False)]` esta preparado para poder aislar las intenciones que poseen una palabra especifica, en este ejemplo la palabra es "curso". 

Por ultimo crean los graficos de frecuencia de los 30 mas frecuentes, los 10 menos frecuentes - `top_30_frequent.png` y `bottom_10_frequent.png` - y la curva de frecuencias `curva_frecuencia_total.png`.  

Los descriptores estadísticos se exportan en `descriptive_stats.csv`

#### Entregables ##  
Los Archivos mencionados en la sección anterior se encuentran en la razi del repositorio. El separador de los archivos  CSV esta definido como Punto y Coma para que sea levantado automaticamente desde __Excel__  
`bottom_10_disparadores_details.csv`  
`bottom_10_frequent.csv`             
`curso_disparadores_details.csv`     
`descriptive_stats.csv`              
`df_tsv_sorted.csv`                  
`frases_por_intencion.csv`           
`frequency_analysis.csv`             
`top_30_disparadores_details.csv`    
`top_30_frequent.csv`                

Imagenes  
`bottom_10_frequent.png`   
`curva_frecuencia_total.png`      
`top_30_frequent.png`   
`total_word_count.png`         

### Contribución  
¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama para tu funcionalidad o corrección de errores (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commits con mensajes claros y concisos (`git commit -m 'Descripción de los cambios'`).
4. Sube tus cambios a tu repositorio (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request en el repositorio original y describe los cambios que has realizado.

Por favor, asegúrate de que tu código sigue los estándares de estilo del proyecto y que todas las pruebas pasan correctamente antes de enviar tu Pull Request.


### Licencia 

Este proyecto está bajo la Licencia MIT.

MIT License

Derechos de autor (c) [2024] [Eduardo Damian Veralli]

Se concede permiso por la presente, sin cargo, a cualquier persona que obtenga una copia
de este software y los archivos de documentación asociados (el "Software"), para tratar
en el Software sin restricciones, incluidos, entre otros, los derechos
para usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender
copias del Software, y para permitir a las personas a quienes se les proporcione el Software
hacerlo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todos
copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIABILIDAD,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O
LOS TITULARES DEL COPYRIGHT SERÁN RESPONSABLES POR CUALQUIER RECLAMACIÓN, DAÑO U OTRA RESPONSABILIDAD,
YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O DE OTRO MODO, QUE SURJA DE, FUERA DE O EN
CONEXIÓN CON EL SOFTWARE O EL USO U OTROS TRATOS EN EL SOFTWARE.


### Contacto 

Para preguntas, sugerencias o comentarios, puedes contactar a:

Eduardo Damián Veralli - [@edveralli](https://x.com/EdVeralli) - edveralli@gmail.com

Enlace del Proyecto: [https://github.com/team-metricas/Disparadores](https://github.com/team-metricas/Variables-y-Tags-en-BM)

