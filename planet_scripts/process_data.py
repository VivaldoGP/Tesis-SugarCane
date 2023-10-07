import os

import datetime

import json

import rasterio
from rasterio.io import DatasetReader

from rasterstats import zonal_stats

import fiona

import numpy as np
import pandas as pd
from pandas.errors import DataError

np.seterr(divide='ignore', invalid='ignore')
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

main_path = r"C:\Users\DELL\PycharmProjects\Tesis\planet"
df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\planet"


def ndvi(img: DatasetReader):
    nir_band = img.read(8)
    red_band = img.read(6)

    ndvi_band = (nir_band.astype(float) - red_band.astype(float)) / (nir_band.astype(float) + red_band.astype(float))

    return ndvi_band


ndvi_stats = []
index_start = 0

for root, subdirs, files in os.walk(main_path):
    for file in files:
        if 'udm2' not in file and file.endswith('.tif'):
            with rasterio.open(os.path.join(root, file)) as src:
                transform = src.transform
                ndvi_img = ndvi(src)
                with fiona.open(r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\SHP\Parcelas.shp", "r") as shp:
                    for feature in shp:
                        feature_id = feature['properties']['Id']
                        if feature_id == 1:
                            stats = zonal_stats(feature, ndvi_img, affine=transform, nodata=0)
                            # print(stats)
        elif 'metadata' in file and file.endswith('.json'):
            with open(os.path.join(root, file)) as meta:
                metadata = json.load(meta)
                date_acquired = metadata['properties']['acquired']
                date_object = datetime.datetime.strptime(date_acquired, date_format)
                ndvi_stats.append({'Id': index_start,
                                   'NDVI_mean': stats[0]['mean'],
                                   'NDVI_min': stats[0]['min'],
                                   'NDVI_max': stats[0]['max'],
                                   'Fecha': date_object.date()})
                index_start += 1

try:
    ndvi_df = pd.DataFrame(ndvi_stats)
    ndvi_df.to_csv(path_or_buf=os.path.join(df_path, f"Parcela_1.csv"), index=False)

except DataError:
    print('Algo salió mal')
