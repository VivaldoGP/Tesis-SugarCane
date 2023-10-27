import rasterio

import fiona
from shapely.geometry import shape

import pandas as pd

import os

import datetime
from calendar import monthrange

agera_path = r"C:\Users\DELL\PycharmProjects\Tesis\AGERA5_PF"
puntos_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Centroides\centroides.shp"

agpf_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\AGpf"


def date_from_filename(filename: str):
    try:
        final_part = filename.split('_')[-1]
        date_part, extension = tuple(final_part.split('.'))
        year: int = int(date_part[:4])
        month: int = int(date_part[5:7])
        last_day = monthrange(year, month)[1]
        return datetime.date(year=year, month=month, day=last_day)
    except (TypeError, ValueError):
        return None


parcelas_df = {}

for file in os.listdir(agera_path):
    if file.endswith('.tif'):
        full_path = os.path.join(agera_path, file)
        fecha = date_from_filename(filename=full_path)
        print(fecha)

        with rasterio.open(full_path) as isrc:
            transform = isrc.transform

            with fiona.open(puntos_path, 'r') as src:
                for feature in src:
                    geom = shape(feature['geometry'])
                    x_coord, y_coord = geom.x, geom.y
                    row, col = isrc.index(x_coord, y_coord)
                    pixel_value = isrc.read(1, window=((row, row + 1), (col, col + 1)))

                    parcela_id = feature['properties']['Id']

                    if parcela_id not in parcelas_df:
                        parcelas_df[parcela_id] = pd.DataFrame(columns=['Fecha', 'PF'])

                    parcelas_df[parcela_id] = pd.concat([
                        parcelas_df[parcela_id],
                        pd.DataFrame({'Fecha': [fecha], 'PF': [pixel_value[0][0]]})
                    ])

for id_, df_ in parcelas_df.items():
    df_.to_csv(os.path.join(agpf_path, f"pf_parcela_{id_}.csv"), index=False)
    print(id_, df_)
