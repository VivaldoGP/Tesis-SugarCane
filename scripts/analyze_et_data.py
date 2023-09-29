import rasterio

import fiona
from shapely.geometry import shape

import pandas as pd

import os

import datetime

agera_path = r"C:\Users\DELL\Documents\Tesis_sugarCane\pruebas"
puntos_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Centroides\centroides.shp"


def date_from_filename(filename: str):
    try:
        final_part = filename.split('_')[-1]
        date_part, extension = tuple(final_part.split('.'))
        year: int = int(date_part[:4])
        month: int = int(date_part[4:6])
        day: int = int(date_part[6:8])
        return datetime.date(year=year, month=month, day=day)
    except (TypeError, ValueError):
        return None


et_images = {}

for file in os.listdir(agera_path):
    if file.endswith('.tif'):
        full_path = os.path.join(agera_path, file)
        et_images[date_from_filename(filename=full_path)] = full_path

for fecha_, image_path_ in et_images.items():
    with rasterio.open(image_path_) as isrc:
        transform = isrc.transform

        pixel_values = []

        with fiona.open(puntos_path, 'r') as src:
            for feature in src:
                geom = shape(feature['geometry'])
                x_coord, y_coord = geom.x, geom.y
                row, col = isrc.index(x_coord, y_coord)
                pixel_value = isrc.read(1, window=((row, row+1), (col, col+1)))
                pixel_values.append(pixel_value)
                print(pixel_value[0][0], feature['properties']['Id'], date_from_filename(image_path_))
