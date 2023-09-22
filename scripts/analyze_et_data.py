import rasterio

import fiona
from shapely.geometry import shape

import pandas as pd

import os

import datetime

agera_path = r"C:\Users\DELL\Documents\Tesis_sugarCane\pruebas"
puntos_path = r"C:\Users\DELL\PycharmProjects\Tesis\Poligonos\SHP\Centroides_RSA\centroides.shp"

et_images = {}

for file in os.listdir(agera_path):
    if file.endswith('.tif'):
        full_path = os.path.join(agera_path, file)
        path_parts = full_path.split('_')
        last_part = path_parts[-1]
        fecha, extension = tuple(last_part.split('.'))
        year, month, day = int(fecha[0:4]), int(fecha[4:6]), int(fecha[6:8])
        fecha_final = datetime.date(year=year, month=month, day=day)
        et_images[fecha_final] = full_path

fsrc = fiona.open(puntos_path, 'r')

et_stats = {}

for fecha_, image_path_ in et_images.items():
    # image_str = str(image)
    # fecha = f'{image_str[16:20]}-{image_str[20:22]}-{image_str[22:24]}'
    src = rasterio.open(image_path_)
    # earthpy.plot.plot_bands(et)
    transform = src.transform

    pixel_values = []

    for feature in fsrc:
        geom = shape(feature['geometry'])
        x_coord, y_coord = geom.x, geom.y
        # print(x_coord, y_coord)
        row, col = src.index(x_coord, y_coord)
        pixel_value = src.read(1, window=((row, row+1), (col, col+1)))
        pixel_values.append(pixel_value[0][0])

    et_stats[fecha_] = {'Imagen': image_path_, 'Pixel_values': pixel_values}


fechas = []
imagenes = []
columnas_pixel = {}

for fecha, valores in et_stats.items():
    fechas.append(fecha)
    imagenes.append(valores['Imagen'])
    for i, valor in enumerate(valores['Pixel_values']):
        if i not in columnas_pixel:
            columnas_pixel[i] = []
        columnas_pixel[i].append(valor)

# Crear el DataFrame
df_et = pd.DataFrame({'Fecha': fechas, 'Imagen': imagenes, **columnas_pixel})

print(df_et.shape)
print(df_et.columns)

df_et.to_csv(r'C:\Users\DELL\PycharmProjects\Tesis\dataframes\et_RSA.csv')
