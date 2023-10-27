import datetime
import os

import fiona

import numpy as np
import pandas as pd

import rasterio
from rasterstats import zonal_stats

from raster_utils.spectral_indices import ndvi, msi, ndmi
from vector_utils.geopro_toos import mem_buffer

np.seterr(divide='ignore', invalid='ignore')

sen_images_path = r"G:\Mi unidad\Tesis_5"
parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\SHP\Parcelas.shp"

mem = mem_buffer(parcelas_path, buffer_size=-5)


def date_from_filename(filename: str):
    try:
        date_part = filename.split('_')[-3]
        year: int = int(date_part[:4])
        month: int = int(date_part[4:6])
        day: int = int(date_part[6:8])
        return datetime.date(year=year, month=month, day=day)
    except (TypeError, ValueError):
        return None


parcel_image_list = []


for dir_ in os.listdir(sen_images_path):
    dir_path = os.path.join(sen_images_path, dir_)
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        with fiona.open(parcelas_path, "r") as shp:
            for features in shp:
                feature_id = f"Parcela_{features['properties']['Id']}"
                if feature_id == dir_:
                    parcel_image_list.append({"Parcela_dir": dir_, "Parcela_id": features['properties']['Id'],
                                              "Img_path": file_path})
                    # print(date_from_filename(filename=file_path))


index_start = 0
indices_stats = []
for i in parcel_image_list:
    with mem.open() as src:
        for features_ in src:
            if i.get("Parcela_dir") == "Parcela_1":
                if features_["properties"]["Id"] == i.get("Parcela_id"):
                    try:
                        with rasterio.open(i.get("Img_path")) as isrc:
                            transform = isrc.transform
                            # print(isrc.width, isrc.height)
                            ndvi_img = ndvi(isrc)
                            ndmi_img = ndmi(isrc)
                            msi_img = msi(isrc)

                            zonal_stats_ndvi = zonal_stats(features_, ndvi_img,
                                                           affine=transform, nodata=-999)
                            zonal_stats_ndmi = zonal_stats(features_, ndmi_img,
                                                           affine=transform, nodata=-999)
                            zonal_stats_msi = zonal_stats(features_, msi_img,
                                                          affine=transform, nodata=-999)

                            index_start += 1
                            print(i.get('Img_path'))
                            print(zonal_stats_ndvi[0])
                            indices_stats.append({"Id": index_start,
                                                  "Fecha": date_from_filename(i.get("Img_path")),
                                                  "Parcela": i.get("Parcela_id"),
                                                  "ndvi_mean": zonal_stats_ndvi[0]['mean'],
                                                  "ndvi_min": zonal_stats_ndvi[0]['min'],
                                                  'ndvi_max': zonal_stats_ndvi[0]['max'],
                                                  "ndmi_mean": zonal_stats_ndmi[0]['mean'],
                                                  "ndmi_min": zonal_stats_ndmi[0]['min'],
                                                  "ndmi_max": zonal_stats_ndmi[0]['max'],
                                                  "msi_mean": zonal_stats_msi[0]['mean'],
                                                  "msi_min": zonal_stats_msi[0]['min'],
                                                  "msi_max": zonal_stats_msi[0]['max']})

                    except rasterio.errors.RasterioIOError:
                        print(f'Algo salió mal en {i}')

# print(ndvi_stats)

ndvi_df = pd.DataFrame(indices_stats)
ndvi_df.to_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\parcelas\parcela_1_test.csv", index=False)
