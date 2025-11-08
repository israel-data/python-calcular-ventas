
# Autor: -工丂尺闩㠪㇄ ᗪ闩ㄒ闩-
# Creado: Noviembre 2025.
# Versión: 1.0.1
# Descripción: Análisis de tiendas para el Challenge 1 de Ciencia de Datos - Alura Latam.
# Repositorio base: https://github.com/israel-data

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

url_tienda1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_1%20.csv"
url_tienda2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_2.csv"
url_tienda3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_3.csv"
url_tienda4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_4.csv"

tienda1 = pd.read_csv(url_tienda1)
tienda2 = pd.read_csv(url_tienda2)
tienda3 = pd.read_csv(url_tienda3)
tienda4 = pd.read_csv(url_tienda4)

tiendas = {
    "Tienda 1": tienda1,
    "Tienda 2": tienda2,
    "Tienda 3": tienda3,
    "Tienda 4": tienda4
}

def buscar_columna(df, palabras_clave):   # Funcion para buscar columnas.
    columnas = {c.lower(): c for c in df.columns}
    for palabra in palabras_clave:
        for c_min, c_original in columnas.items():
            if palabra in c_min:
                return c_original
    return None

carpeta_salida = "resultados_challenge_alura"  # Se crea la carpeta de salida 
os.makedirs(carpeta_salida, exist_ok=True)

palabras_precio = ["precio", "price", "valor", "monto"] # Ingresos totales por tienda.
ingresos = {}

for nombre, datos in tiendas.items():
    col_precio = buscar_columna(datos, palabras_precio)
    if col_precio is None:
        raise RuntimeError(f"No se encontró columna de Precio en {nombre}. Columnas: {datos.columns.tolist()}")
    ingresos[nombre] = datos[col_precio].sum()

df_ingresos = pd.DataFrame(list(ingresos.items()), columns=["Tienda", "Ingreso Total"])
print("Ingreso total por tienda:")
print(df_ingresos)
df_ingresos.to_csv(os.path.join(carpeta_salida, "ingresos_por_tienda.csv"), index=False)

colors = ["#1A1A1D", "#4E4E50", "#6F2232", "#950740", "#C3073F"]
plt.figure(figsize=(8, 5))  # Grafico. Ingresos por tienda
plt.bar(df_ingresos["Tienda"], df_ingresos["Ingreso Total"], color=colors)
plt.title("Ingreso total por tienda.")
plt.ylabel("Ingreso total.")
plt.xlabel("Tienda.")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_salida, "grafico_ingresos_por_tienda.png"))
plt.show()

palabras_categoria = ["categoria", "category", "cat"]   # Ventas por categorias.
ventas_por_categoria = {}

for nombre, datos in tiendas.items():
    col_categoria = buscar_columna(datos, palabras_categoria)
    if col_categoria is None:
        raise RuntimeError(f"No se encontró columna de Categoría en {nombre}. Columnas: {datos.columns.tolist()}")
    conteo = datos[col_categoria].value_counts().reset_index()
    conteo.columns = [col_categoria, "Ventas"]
    ventas_por_categoria[nombre] = conteo
    conteo.to_csv(os.path.join(carpeta_salida, f"ventas_por_categoria_{nombre.replace(' ', '_')}.csv"), index=False)

# --- Gráfico: Top 5 categorías ---
fig, ejes = plt.subplots(2, 2, figsize=(12, 10))
ejes = ejes.flatten()

colors = ["#2E294E", "#541388", "#F1E9DA", "#FFD400", "#D90368"]
for eje, (nombre, conteo) in zip(ejes, ventas_por_categoria.items()):
    top5 = conteo.head(5).sort_values("Ventas", ascending=True)
    eje.barh(top5.iloc[:, 0], top5["Ventas"], color=colors)
    eje.set_title(f"Top categorías - {nombre}")
    eje.set_xlabel("Ventas")

plt.tight_layout()
plt.savefig(os.path.join(carpeta_salida, "top_categorias_por_tienda.png"))
plt.show()

palabras_calificacion = ["calif", "rating", "reseña", "reseñas", "review", "puntuacion", "valoracion", "valoración"] # Calificacion promedio por tienda
promedios_calificacion = {}

for nombre, datos in tiendas.items():
    col_calificacion = buscar_columna(datos, palabras_calificacion)
    if col_calificacion is None:
        promedios_calificacion[nombre] = np.nan
        print(f"No se encontró columna de calificación en {nombre}")
    else:
        promedios_calificacion[nombre] = datos[col_calificacion].mean()

df_calificaciones = pd.DataFrame(list(promedios_calificacion.items()), columns=["Tienda", "Calificación Promedio"])
print("\nCalificación promedio por tienda:")
print(df_calificaciones)
df_calificaciones.to_csv(os.path.join(carpeta_salida, "calificaciones_promedio_por_tienda.csv"), index=False)

colors = ["#3D2C2E", "#6E3B3B", "#B17457", "#DDA15E", "#F6BD60"]
plt.figure(figsize=(8, 5)) # Grafico
plt.bar(df_calificaciones["Tienda"], df_calificaciones["Calificación Promedio"], color=colors)
plt.title("Calificación promedio por tienda")
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_salida, "calificacion_promedio_por_tienda.png"))
plt.show()

palabras_producto = ["producto", "nombre", "product", "item"] # Productos mas y menos vendidos
estadisticas_productos = {}

for nombre, datos in tiendas.items():
    col_producto = buscar_columna(datos, palabras_producto)
    if col_producto is None:
        raise RuntimeError(f"No se encontró columna de producto en {nombre}. Columnas: {datos.columns.tolist()}")
    conteo = datos[col_producto].value_counts().reset_index()
    conteo.columns = [col_producto, "Ventas"]
    mas_vendidos = conteo.head(5)
    menos_vendidos = conteo.tail(5).sort_values("Ventas", ascending=True)
    estadisticas_productos[nombre] = {"mas_vendidos": mas_vendidos, "menos_vendidos": menos_vendidos, "conteo": conteo}
    mas_vendidos.to_csv(os.path.join(carpeta_salida, f"top5_mas_vendidos_{nombre.replace(' ', '_')}.csv"), index=False)
    menos_vendidos.to_csv(os.path.join(carpeta_salida, f"top5_menos_vendidos_{nombre.replace(' ', '_')}.csv"), index=False)

conteo_global = pd.DataFrame()  # Top de productos globales.

for nombre, info in estadisticas_productos.items():
    dfc = info["conteo"].copy()
    dfc = dfc.rename(columns={dfc.columns[0]: "producto", "Ventas": f"Ventas_{nombre}"})
    if conteo_global.empty:
        conteo_global = dfc
    else:
        conteo_global = conteo_global.merge(dfc, on="producto", how="outer")

conteo_global = conteo_global.fillna(0)
columnas_ventas = [c for c in conteo_global.columns if c.startswith("Ventas_")]
conteo_global["Ventas_total"] = conteo_global[columnas_ventas].sum(axis=1)
top_productos_global = conteo_global.sort_values("Ventas_total", ascending=False).head(10)
top_productos_global.to_csv(os.path.join(carpeta_salida, "top_productos_global.csv"), index=False)

colors = ["#2E294E", "#541388", "#6A4C93", "#B497BD", "#E0A96D"]
plt.figure(figsize=(10, 6)) # Grafico. Top de 10prductos mas vendidoa
plt.barh(top_productos_global["producto"].iloc[::-1], top_productos_global["Ventas_total"].iloc[::-1], color=colors)
plt.title("Top 10 productos más vendidos (todas las tiendas)")
plt.xlabel("Ventas totales")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_salida, "top10_productos_global.png"))
plt.show()

palabras_envio = ["envio", "shipping", "ship", "envío", "costo envio", "valor envio"] # Analisis promedio por tienda.
promedio_envio = {}

for nombre, datos in tiendas.items():
    col_envio = buscar_columna(datos, palabras_envio)
    if col_envio is None:
        promedio_envio[nombre] = np.nan
        print(f"No se encontró columna de envío en {nombre}")
    else:
        promedio_envio[nombre] = datos[col_envio].mean()

df_envio = pd.DataFrame(list(promedio_envio.items()), columns=["Tienda", "Envío Promedio"])
df_envio.to_csv(os.path.join(carpeta_salida, "envio_promedio_por_tienda.csv"), index=False)
print("\nEnvío promedio por tienda:")
print(df_envio)

plt.figure(figsize=(8, 5))
plt.bar(df_envio["Tienda"], df_envio["Envío Promedio"], color="plum")
plt.title("Envío promedio por tienda")
plt.ylabel("Costo de envío promedio")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_salida, "grafico_envio_promedio_por_tienda.png"))
plt.show()

palabras_lat = ["lat", "latitude"]  # Analisis geofrafico opcional
palabras_lon = ["lon", "lng", "longitud", "longitude"]
tiene_geo = False

plt.figure(figsize=(8, 6))
for nombre, datos in tiendas.items():
    col_lat = buscar_columna(datos, palabras_lat)
    col_lon = buscar_columna(datos, palabras_lon)
    if col_lat and col_lon:
        tiene_geo = True
        plt.scatter(datos[col_lon], datos[col_lat], label=nombre, alpha=0.6, s=20)

if tiene_geo:
    plt.title("Ventas por ubicación (longitud vs latitud)")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "mapa_ventas.png"))
    plt.show()
else:
    print("No se encontraron columnas de coordenadas geográficas; se omite el análisis.")

df_resumen = df_ingresos.merge(df_calificaciones, on="Tienda").merge(df_envio, on="Tienda")  # Resumen 
df_resumen["Total Ventas (n)"] = [len(tiendas[t]) for t in df_resumen["Tienda"]]
df_resumen = df_resumen[["Tienda", "Total Ventas (n)", "Ingreso Total", "Calificación Promedio", "Envío Promedio"]]
df_resumen.to_csv(os.path.join(carpeta_salida, "resumen_por_tienda.csv"), index=False)

print("\nAnálisis completado correctamente.")
print("Resultados guardados en la carpeta:", carpeta_salida)