import pandas as pd

import os

et_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\et"
parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\parcelas"
merged_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\merged"

parcelas_dict = {}

for i in os.listdir(parcelas_path):
    filename, ext = i.split('.')
    name, number = filename.split('_')
    parcelas_dict[number] = pd.read_csv(os.path.join(parcelas_path, i))

et_dict = {}

for j in os.listdir(et_path):
    filename_, ext_ = j.split('.')
    number_ = filename_.split('_')[-1]
    et_dict[number_] = pd.read_csv(os.path.join(et_path, j))

for key, value in parcelas_dict.items():
    value['Fecha'] = value['Unnamed: 0'].astype('datetime64[ns]')
    for key_, value_ in et_dict.items():
        value_['Fecha'] = value_['Fecha'].astype('datetime64[ns]')
        if key == key_:
            merged = pd.merge(value, value_, on='Fecha')
            merged.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)
            merged.to_csv(os.path.join(merged_path, f"parcela_{key}.csv"), index=True)
