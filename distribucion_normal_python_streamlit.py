import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import sqlite3
import os


def gaussian(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def cargar_datos_ejemplo(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS tabla (fecha TEXT, valor REAL)")

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

    conn.executemany("INSERT INTO tabla VALUES (?, ?)", datos_ejemplo)

    conn.commit()


def eliminar_base_de_datos():
    if os.path.exists('ruta_a_tu_base_de_datos2.db'):
        os.remove('ruta_a_tu_base_de_datos2.db')


def consultar_datos(conn, query):
    df = pd.read_sql(query, conn)
    df['fecha'] = pd.to_datetime(df['fecha'])
    conn.close()
    return df


def obtener_rango_fechas(df):
    fecha_inicio = df['fecha'].min().strftime('%Y-%m-%d')
    fecha_fin = df['fecha'].max().strftime('%Y-%m-%d')
    df.drop('fecha', axis=1, inplace=True)
    return fecha_inicio, fecha_fin, df


def calcular_media_desviacion(df):
    mu = np.mean(df['valor'])
    sigma = np.std(df['valor'])
    return mu, sigma


def generar_datos_ejemplo(mu, sigma):
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    y = gaussian(x, mu, sigma)
    return x, y


def visualizar_distribucion_normal(x, y, fecha_inicio, fecha_fin, mu, sigma, df):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.fill_between(x, 0, y, alpha=0.3)
    ax.set(xlabel='Valores', ylabel='Densidad de probabilidad', title='Distribución Normal de Valores')
    
    leyenda = f'Fecha de inicio: {fecha_inicio}\nFecha de fin: {fecha_fin}'
    plt.text(0.05, 0.2, leyenda, transform=ax.transAxes, fontsize=10, verticalalignment='top')
    
    plt.text(0.05, 0.95, f'Media (μ) = {mu}', transform=ax.transAxes, fontsize=12, verticalalignment='top')
    plt.text(0.05, 0.9, f'Desviación estándar (σ) = {sigma}', transform=ax.transAxes, fontsize=12, verticalalignment='top')
    plt.text(0.05, 0.8, 'La media indica el valor central de la distribución,', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    plt.text(0.05, 0.75, 'que en este caso es el promedio de los valores.', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    plt.text(0.05, 0.65, 'La desviación estándar indica qué tan dispersos', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    plt.text(0.05, 0.6, 'están los datos alrededor de la media.', transform=ax.transAxes, fontsize=10, verticalalignment='top')
    
    cantidad_registros = len(df)
    plt.text(0.05, 0.5, f'Registros leídos: {cantidad_registros}', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    st.pyplot(fig)


def main():
    st.set_page_config(page_title='Distribución Normal', layout='centered')
    conn = sqlite3.connect('ruta_a_tu_base_de_datos2.db')
    eliminar_base_de_datos()
    cargar_datos_ejemplo(conn)
    query = "SELECT fecha, valor FROM tabla"
    df = consultar_datos(conn, query)
    fecha_inicio, fecha_fin, df = obtener_rango_fechas(df)
    mu, sigma = calcular_media_desviacion(df)
    x, y = generar_datos_ejemplo(mu, sigma)
    visualizar_distribucion_normal(x, y, fecha_inicio, fecha_fin, mu, sigma, df)


if __name__ == "__main__":
    main()
