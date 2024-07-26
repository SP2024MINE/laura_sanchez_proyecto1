import streamlit as st
from sodapy import Socrata
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv('.env')

APP_TOKEN = os.getenv("TOKEN_SODAPY")
DATASET_ID = os.getenv("DATASET_ID2")

st.title("""CONECTIVIDAD EN SEDES EDUCATIVAS DE MUNICIPIOS NO CERTIFICADOS DE SANTANDER""")
st.write('Rendimiento ancho de banda')

client = Socrata("www.datos.gov.co", APP_TOKEN)

Query = """
select 
    no, municipio, establecimiento_educativo, sede, zona, operador_conectividad, ancho_banda
limit
10000000
"""

results = client.get(DATASET_ID, query=Query)

df = pd.DataFrame.from_records(results)
df['municipio'] = df['municipio'].str.upper()
df['ancho_banda'] = df['ancho_banda'].astype(float)

list_municipios = df['municipio'].drop_duplicates()

municipio = st.selectbox('Seleccione un municipio', list_municipios, 
                        placeholder='Seleccione un municipio unico')


dataset_mun = df[df['municipio'] == municipio]

# Incluir la cantidad de colegios en el municipio seleccionado
cantidad_colegios = dataset_mun['establecimiento_educativo'].count()
st.metric(label=f'Cantidad de sedes en {municipio}', value=cantidad_colegios)

promedio_ancho_banda = dataset_mun.groupby('zona')['ancho_banda'].mean().reset_index()

# Crear el gráfico
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(promedio_ancho_banda['zona'], promedio_ancho_banda['ancho_banda'], color='skyblue')
ax.set_xlabel('Zona')
ax.set_ylabel('Promedio de Ancho de Banda')

# Añadir etiquetas a las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height,
            f'{height:.2f}', ha='center', va='bottom')


# Mostrar el gráfico en Streamlit
st.pyplot(fig)





