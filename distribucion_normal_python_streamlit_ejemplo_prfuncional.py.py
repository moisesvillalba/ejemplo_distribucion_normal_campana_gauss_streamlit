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
        ("2023-06-01", 23),
        ("2023-06-02", 25),
        ("2023-06-03", 28),
        ("2023-06-04", 27),
        ("2023-06-05", 30),
        ("2023-06-06", 24),
        ("2023-06-07", 29),
        ("2023-06-08", 26),
        ("2023-06-09", 31),
        ("2023-06-10", 22),
    ]

    conn.executemany("INSERT INTO tabla VALUES (?, ?)", datos_ejemplo)
    conn.commit()


def cerrar_conexion(conn):
    if "conn" in locals():
        conn.close()


def eliminar_base_de_datos(ruta_db):
    try:
        if os.path.exists(ruta_db):
            os.remove(ruta_db)
    except Exception as e:
        print(f"Error al eliminar la base de datos: {e}")


def configurar_pagina(titulo, layout):
    st.set_page_config(page_title=titulo, layout=layout)


def crear_titulo(titulo):
    st.title(titulo)


def crear_descripcion(descripcion):
    st.write(descripcion)


def cargar_datos(conn):
    cargar_datos_ejemplo(conn)


def obtener_datos(query, conn):
    return pd.read_sql(query, conn)


def convertir_columna_fecha(df):
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


def eliminar_columna(df):
    return df.drop("fecha", axis=1)


def calcular_media(df):
    return np.mean(df["valor"])


def calcular_desviacion_estandar(df):
    return np.std(df["valor"])


def generar_datos(mu, sigma):
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    y = gaussian(x, mu, sigma)
    return x, y


def generar_grafico(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.fill_between(x, 0, y, alpha=0.3)
    ax.set(
        xlabel="Valores",
        ylabel="Densidad de probabilidad",
        title="Distribución Normal de Valores",
    )
    return fig, ax


def obtener_fecha_inicio(df):
    return df["fecha"].min().strftime("%Y-%m-%d")


def obtener_fecha_fin(df):
    return df["fecha"].max().strftime("%Y-%m-%d")


def generar_leyenda(fecha_inicio, fecha_fin):
    return f"Fecha de inicio: {fecha_inicio}\nFecha de fin: {fecha_fin}"


def generar_texto(mu, sigma):
    texto = f"Media (μ) = {mu}\n"
    texto += f"Desviación estándar (σ) = {sigma}\n"
    texto += "La media indica el valor central de la distribución,\n"
    texto += "que en este caso es el promedio de los valores.\n"
    texto += "La desviación estándar indica qué tan dispersos\n"
    texto += "están los datos alrededor de la media.\n"
    return texto


def obtener_cantidad_registros(df):
    return len(df)


def generar_texto_registros(cantidad_registros):
    return f"Registros leídos: {cantidad_registros}"


def imprimir_texto_grafico(ax, x, y, texto, mu, sigma, cantidad_registros):
    ax.text(
        0.05, 0.2, texto, transform=ax.transAxes, fontsize=10, verticalalignment="top"
    )
    ax.text(
        0.05,
        0.95,
        f"Media (μ) = {mu}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.9,
        f"Desviación estándar (σ) = {sigma}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.8,
        "La media indica el valor central de la distribución,",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.75,
        "que en este caso es el promedio de los valores.",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.65,
        "La desviación estándar indica qué tan dispersos",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.6,
        "están los datos alrededor de la media.",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
    )
    ax.text(
        0.05,
        0.5,
        f"Registros leídos: {cantidad_registros}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
    )


def visualizacion_distribucion_normal(ruta_db, query):
    conn = sqlite3.connect(ruta_db)

    configurar_pagina("Distribución Normal", "centered")
    crear_titulo("Distribución Normal")
    crear_descripcion("Esta es una visualización de la distribución normal.")
    cargar_datos(conn)
    df = obtener_datos(query, conn)
    df = convertir_columna_fecha(df)
    cerrar_conexion(conn)
    fecha_inicio = obtener_fecha_inicio(df)
    fecha_fin = obtener_fecha_fin(df)
    df = eliminar_columna(df)
    mu = calcular_media(df)
    sigma = calcular_desviacion_estandar(df)
    x, y = generar_datos(mu, sigma)
    fig, ax = generar_grafico(x, y)
    leyenda = generar_leyenda(fecha_inicio, fecha_fin)
    texto = generar_texto(mu, sigma)
    cantidad_registros = obtener_cantidad_registros(df)
    texto_registros = generar_texto_registros(cantidad_registros)
    imprimir_texto_grafico(ax, x, y, leyenda, mu, sigma, cantidad_registros)
    st.pyplot(fig)


# Solo se ejecuta si el archivo se ejecuta directamente
if __name__ == "__main__":
    # Aquí puedes agregar el código que deseas ejecutar cuando el archivo se ejecute directamente
    ruta_db = "base_de_datos.db"
    query = "SELECT fecha, valor FROM tabla"
    eliminar_base_de_datos(ruta_db)
    visualizacion_distribucion_normal(ruta_db, query)
