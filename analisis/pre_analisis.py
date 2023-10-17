import os
import pandas as pd
import numpy as np
import json
import random

from stats_utils.regression_models import simple_weight_regression

parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Parcelas_2.geojson"
df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"


ndvi_ana = []
ndvi_data = []

for i in os.listdir(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"):
    df = pd.read_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo\{}".format(i))
    df['Fecha'] = df['Fecha'].astype('datetime64[ns]')
    df = df.sort_values(by='Fecha', ascending=True)
    file_name, ext = i.split('.')
    parcela_id = file_name.split('_')[1]

    with open(parcelas_path, encoding='utf-8') as par:
        parcelas = json.load(par)
    for j in parcelas['features']:
        if j['properties']['Productor'] == 'Ana Isabel Govea Echavarría':
            if int(parcela_id) == j['properties']['Id']:
                ndvi_ana.append((int(parcela_id), j['properties']['Rendimiento'], j['properties']['Productor'], df['ndvi_mean'].mean()))
        elif j['properties']['Productor'] != 'Ana Isabel Govea Echavarría':
            if int(parcela_id) == j['properties']['Id']:
                ndvi_data.append((int(parcela_id), j['properties']['Rendimiento'], j['properties']['Productor'], df['ndvi_mean'].mean()))


df_ana = pd.DataFrame(ndvi_ana, columns=['Parcela', 'Rendimiento', 'Productor', 'NDVI'])
print(df_ana['NDVI'].mean())
fila_al = df_ana.sample(n=1)
datos_ana = (5, fila_al['Rendimiento'].values[0],
             fila_al['Productor'].values[0], df_ana['NDVI'].mean())
ndvi_data.append(datos_ana)
for i in ndvi_data:
    print(i)

df_data = pd.DataFrame(ndvi_data, columns=['Parcela', 'yield', 'Productor', 'ndvi'])
df_data.drop(df_data[df_data['Parcela'] == 12].index, inplace=True)
df_data = df_data.sort_values(by='Parcela', ascending=True)
df_data.to_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\ndvi_data.csv", index=False)
