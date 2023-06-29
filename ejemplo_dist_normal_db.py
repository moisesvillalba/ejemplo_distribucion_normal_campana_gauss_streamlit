import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import sqlite3
import os

def gaussian(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Función para cargar datos de ejemplo en la base de datos
def cargar_datos_ejemplo(conn):
    # Crear tabla
    conn.execute("CREATE TABLE IF NOT EXISTS tabla (fecha TEXT, valor REAL)")

    # Datos de ejemplo
    datos_ejemplo = [
        ('2023-06-01', 23),
        ('2023-06-02', 25),
        ('2023-06-03', 28),
        ('2023-06-04', 27),
        ('2023-06-05', 30),
        ('2023-06-06', 24),
        ('2023-06-07', 29),
        ('2023-06-08', 26),
        ('2023-06-09', 31),
        ('2023-06-10', 22),
    ]

    # Insertar datos de ejemplo en la tabla
    conn.executemany("INSERT INTO tabla VALUES (?, ?)", datos_ejemplo)

    # Guardar cambios
    conn.commit()

# Cerrar cualquier conexión existente a la base de datos
if 'conn' in locals():
    conn.close()

# Eliminar la base de datos si existe
if os.path.exists('ruta_a_tu_base_de_datos.db'):
    os.remove('ruta_a_tu_base_de_datos.db')

# Configuración de la página
st.set_page_config(page_title='Distribución Normal', layout='centered')

# Título y descripción
st.title('Distribución Normal')
st.write('Esta es una visualización de la distribución normal.')

# Conexión a la base de datos
conn = sqlite3.connect('ruta_a_tu_base_de_datos.db')

# Cargar datos de ejemplo en la base de datos
cargar_datos_ejemplo(conn)

# Consulta SQL para obtener los datos
query = "SELECT fecha, valor FROM tabla"

# Leer los datos desde la base de datos y crear el DataFrame
df = pd.read_sql(query, conn)

# Convertir la columna 'fecha' a tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Cerrar la conexión a la base de datos
conn.close()

# Obtener la fecha de inicio y fin del DataFrame
fecha_inicio = df['fecha'].min().strftime('%Y-%m-%d')
fecha_fin = df['fecha'].max().strftime('%Y-%m-%d')

# Eliminar la columna 'fecha' del DataFrame
df.drop('fecha', axis=1, inplace=True)

# Cálculo de la media
mu = np.mean(df['valor'])

# Cálculo de la desviación estándar
sigma = np.std(df['valor'])

# Generar datos de ejemplo para graficar
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = gaussian(x, mu, sigma)

# Visualización de la distribución normal
fig, ax = plt.subplots()
ax.plot(x, y)
ax.fill_between(x, 0, y, alpha=0.3)
ax.set(xlabel='Valores', ylabel='Densidad de probabilidad', title='Distribución Normal de Valores')

# Leyenda con la fecha de inicio y fin
leyenda = f'Fecha de inicio: {fecha_inicio}\nFecha de fin: {fecha_fin}'
plt.text(0.05, 0.2, leyenda, transform=ax.transAxes, fontsize=10, verticalalignment='top')

# Imprimir las variables y explicación
plt.text(0.05, 0.95, f'Media (μ) = {mu}', transform=ax.transAxes, fontsize=12, verticalalignment='top')
plt.text(0.05, 0.9, f'Desviación estándar (σ) = {sigma}', transform=ax.transAxes, fontsize=12, verticalalignment='top')
plt.text(0.05, 0.8, 'La media indica el valor central de la distribución,', transform=ax.transAxes, fontsize=10, verticalalignment='top')
plt.text(0.05, 0.75, 'que en este caso es el promedio de los valores.', transform=ax.transAxes, fontsize=10, verticalalignment='top')
plt.text(0.05, 0.65, 'La desviación estándar indica qué tan dispersos', transform=ax.transAxes, fontsize=10, verticalalignment='top')
plt.text(0.05, 0.6, 'están los datos alrededor de la media.', transform=ax.transAxes, fontsize=10, verticalalignment='top')

# Obtener la cantidad de registros leídos
cantidad_registros = len(df)

# Imprimir la cantidad de registros leídos en el gráfico
plt.text(0.05, 0.5, f'Registros leídos: {cantidad_registros}', transform=ax.transAxes, fontsize=12, verticalalignment='top')

st.pyplot(fig)
