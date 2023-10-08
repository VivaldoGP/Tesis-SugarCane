import os

import datetime

import json

import rasterio
from rasterio.io import DatasetReader
from rasterio.errors import RasterioIOError

from rasterstats import zonal_stats

import fiona

import numpy as np
import pandas as pd
from pandas.errors import DataError

np.seterr(divide='ignore', invalid='ignore')
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

path_images = r"C:\Users\DELL\PycharmProjects\Tesis\planet\parcela_1_psscene_analytic_8b_sr_udm2"
df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\planet"
parcelas_shp = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\SHP\Parcelas.shp"
parcela_id = 1


def ndvi(img: DatasetReader):
    """
    Calcula el ndvi
    Args:
        img: un imagen de rasterio

    Returns:
        un ndarray con los valores del ndvi para pixel
    """
    nir_band = img.read(8)
    red_band = img.read(6)

    ndvi_band = (nir_band.astype(float) - red_band.astype(float)) / (nir_band.astype(float) + red_band.astype(float))

    return ndvi_band


ndvi_stats: list = []
index_start: int = 0

for root, subdirs, files in os.walk(path_images):
    for subdir in subdirs:
        sub_path = os.path.join(root, subdir)
        if os.path.isdir(sub_path):
            for file in os.listdir(os.path.join(root, subdir)):
                if 'udm2' not in file and file.endswith('.tif'):
                    file_path = os.path.join(sub_path, file)
                    try:
                        with rasterio.open(file_path) as src:
                            transform = src.transform

                            ndvi_img = ndvi(src)

                            with fiona.open(parcelas_shp, "r") as shp:
                                for feature in shp:
                                    feature_id = feature['properties']['Id']
                                    if feature_id == parcela_id:
                                        stats = zonal_stats(feature, ndvi_img, affine=transform, nodata=0)
                                        # print(stats)
                                        index_start += 1
                    except RasterioIOError:
                        print(f"Something went wrong! in {file_path}")

                elif 'metadata' in file and file.endswith('.json'):
                    metadata_file_path = os.path.join(sub_path, file)
                    with open(metadata_file_path) as meta:
                        metadata = json.load(meta)
                        date_acquired = metadata['properties']['acquired']
                        date_object = datetime.datetime.strptime(date_acquired, date_format)
                        ndvi_stats.append({'Id': index_start, 'ndvi_mean': stats[0]['mean'],
                                           'ndvi_min': stats[0]['min'], 'ndvi_max': stats[0]['max'],
                                           'Fecha': date_object.date()})


print(index_start)


try:
    ndvi_df = pd.DataFrame(ndvi_stats)
    ndvi_df.to_csv(path_or_buf=os.path.join(df_path, f"Parcela_1.csv"), index=False)

except DataError:
    print('Algo salió mal')
