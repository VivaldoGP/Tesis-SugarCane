import numpy as np
import rasterio
import rasterstats

import fiona
import pandas as pd

import os

import datetime

sen_images_path = r"C:\Users\DELL\PycharmProjects\Tesis\imagenes_2"
parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\SHP\Parcelas.shp"


def date_from_filename(filename: str):
    try:
        date_part = filename.split('_')[-3]
        year: int = int(date_part[:4])
        month: int = int(date_part[4:6])
        day: int = int(date_part[6:8])
        return datetime.date(year=year, month=month, day=day)
    except (TypeError, ValueError):
        return None


def ndvi(image):
    """
    Calcula el índice NDVI.
    Args:
        image: Imagen en formato válido para rasterio, tomando las bandas NIR y RED.

    Returns: Un array con los valores de los píxeles calculados.

    """
    nir = image.read(7)
    red = image.read(3)

    ndvi_calc = np.where(
        (nir+red) == 0.,
        0,
        (nir-red)/(nir+red))

    return ndvi_calc


def ndre_1(image):

    nir = image.read(4)
    red = image.read(3)

    nir_2 = image.read(5)
    nir_3 = image.read(6)

    ndre1_calc = (nir.astype('float64') - red.astype('float64')) / (nir_2.astype('float64') + nir_3.astype('float64'))

    return ndre1_calc


def calc_index(image_path: str, shp_path: str):
    try:
        with rasterio.open(image_path) as src:
            transform = src.transform
            index_band = ndvi(src)

            zonal_stats_ = rasterstats.zonal_stats(shp_path, index_band, affine=transform,
                                                   stats=['mean', 'max', 'min'])
            return zonal_stats_
    except (rasterio.errors.RasterioIOError, ValueError):
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

ndvi_stats = {}
for i in parcel_image_list:
    with fiona.open(parcelas_path, "r") as src:
        for features_ in src:
            if i.get("Parcela_dir") == "Parcela_11":
                if features_["properties"]["Id"] == i.get("Parcela_id"):
                    try:
                        with rasterio.open(i.get("Img_path")) as isrc:
                            transform = isrc.transform
                            # print(isrc.width, isrc.height)
                            ndvi_band = ndvi(isrc)

                            zonal_stats = rasterstats.zonal_stats(features_, ndvi_band,
                                                                  affine=transform)
                            print(zonal_stats[0])
                            ndvi_stats[date_from_filename(i.get("Img_path"))] = {"Parcela": i.get("Parcela_id"),
                                                                                 "mean": zonal_stats[0]['mean'],
                                                                                 "min": zonal_stats[0]['min'],
                                                                                 'max': zonal_stats[0]['max']}

                    except rasterio.errors.RasterioIOError:
                        print('f')

print(ndvi_stats)
'''
sen_images = {}

for file in os.listdir(sen_images_path):
    if file.endswith('.tif'):
        full_path = os.path.join(sen_images_path, file)
        fecha = date_from_filename(filename=file)
        if fecha:
            sen_images[fecha] = full_path

ndvi_stats = {}
'''
'''
for fecha, image_path_ in sen_images.items():
    zonal_stats = calc_ndvi(image_path=image_path_, shp_path=parcelas_path)
    if zonal_stats:
        imagen = image_path_.split('_')
        for num, feature in enumerate(zonal_stats):
            key = f"{num + 1}_{imagen[-3]}"
            ndvi_stats[key] = {
                'imagen': imagen[-3],
                'fecha': fecha,
                'num_parcela': num + 1,
                'mean_ndvi': feature['mean'],
                'max_ndvi': feature['max'],
                'min_ndvi': feature['min']
            }

ndvi_df.reset_index(inplace=True)
'''

ndvi_df = pd.DataFrame.from_dict(ndvi_stats, orient='index')
ndvi_df.to_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\parcela11.csv")
print(ndvi_stats)
