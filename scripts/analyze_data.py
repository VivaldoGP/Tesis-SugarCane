import rasterio
import rasterstats

import pandas as pd

import os

import datetime

sen_images_path = r"C:\Users\DELL\PycharmProjects\Tesis\Tesis_caña"
parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\Poligonos\SHP\Rancho_SantaAnita\Lote_Rancho_Santa_Anita.shp"


def date_from_filename(filename: str):
    try:
        date_part = filename.split('_')[4]
        year: int = int(date_part[:4])
        month: int = int(date_part[4:6])
        day: int = int(date_part[6:8])
        return datetime.date(year=year, month=month, day=day)
    except (TypeError, ValueError):
        return None


def ndvi(image):
    nir = image.read(4)
    red = image.read(3)

    nir_dtype = nir.astype('float64')
    red_dtype = red.astype('float64')

    ndvi_calc = (nir_dtype - red_dtype) / (nir_dtype + red_dtype)

    return ndvi_calc


def calc_ndvi(image_path: str, shp_path: str):
    try:
        with rasterio.open(image_path) as src:
            transform = src.transform
            ndvi_band = ndvi(src)

            zonal_stats_ = rasterstats.zonal_stats(shp_path, ndvi_band, affine=transform,
                                                   stats=['mean', 'max', 'min'])
            return zonal_stats_
    except (rasterio.errors.RasterioIOError, ValueError):
        return None


sen_images = {}

for file in os.listdir(sen_images_path):
    if file.endswith('.tif'):
        full_path = os.path.join(sen_images_path, file)
        fecha = date_from_filename(filename=file)
        if fecha:
            sen_images[fecha] = full_path

ndvi_stats = {}

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

ndvi_df = pd.DataFrame.from_dict(ndvi_stats, orient='index')
ndvi_df.reset_index(inplace=True)
