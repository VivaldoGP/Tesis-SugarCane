import rasterio
import rasterstats

import geopandas as gpd
import pandas as pd

from os import listdir
from os import path

# from datetime import datetime
from datetime import date

parcelas = gpd.read_file(r'C:\Users\DELL\PycharmProjects\Tesis\Poligonos\SHP\Rancho_SantaAnita'
                         r'\Lote_Rancho_Santa_Anita.shp',
                         encoding='utf-8')

parcelas_wgs_84 = parcelas.to_crs(4326)


def ndvi(image):
    nir = image.read(4)
    red = image.read(3)

    nir_dtype = nir.astype('float64')
    red_dtype = red.astype('float64')

    ndvi_calc = (nir_dtype - red_dtype) / (nir_dtype + red_dtype)

    return ndvi_calc


sen_images_path = r"C:\Users\DELL\PycharmProjects\Tesis\imagenes_sentinel"

sen_images = {}

try:
    for file in listdir(sen_images_path):
        if file.endswith('.tif'):
            full_path = path.join(sen_images_path, file)
            splited_file_name = file.split('_')
            year, month, day = (int(splited_file_name[4][0:4]), int(splited_file_name[4][4:6]),
                                int(splited_file_name[4][6:8]))
            fecha = date(year, month, day)
            sen_images[fecha] = full_path
except ValueError:
    print('algo salio mal')

stats_ndvi = {}

try:
    for fecha, image_path in sen_images.items():

        imagen = image_path.split('_')
        src = rasterio.open(image_path)
        transform = src.transform
        ndvi_band = ndvi(src)

        for num, feature in enumerate(rasterstats.zonal_stats(r'C:\Users\DELL\PycharmProjects\Tesis\Poligonos\SHP'
                                                              r'\Rancho_SantaAnita\Lote_Rancho_Santa_Anita.shp',
                                                              ndvi_band, affine=transform, stats=['mean', 'max',
                                                                                                  'min'])):
            # print(num, feature)

            key = f"{num + 1}_{imagen[-3]}"
            stats_ndvi[key] = {
                'Imagen': imagen[-3],
                'Fecha': fecha,
                'Num_parcela': num + 1,
                'mean_ndvi': feature['mean'],
                'max_ndvi': feature['max'],
                'min_ndvi': feature['min']
            }
    ndvi_df = pd.DataFrame.from_dict(stats_ndvi, orient='index')
    ndvi_df.reset_index(inplace=True)
except TypeError:
    print('chin')

print(ndvi_df.loc[ndvi_df['Num_parcela'] == 1])
