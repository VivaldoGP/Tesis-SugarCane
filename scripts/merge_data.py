import pandas as pd
from pandas import DataFrame
import datetime

import os
import json

et_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\et"
parcelas_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\parcelas"
merged_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\merged"
harvest_path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\harvest_dates.json"
cloudy_dates = r"C:\Users\DELL\PycharmProjects\Tesis\cloudy_images\cloudy_dates.json"


def prepare_data(data: DataFrame, start_date: datetime.datetime, end_date: datetime.datetime):

    data['Fecha'] = data['Fecha'].astype('datetime64[ns]')
    data = data.sort_values(by='Fecha', ascending=True)
    data = data[(data['Fecha'] >= start_date) & (data['Fecha'] < end_date)]
    data = data[data['ndvi_mean'] > 0.2]

    return data


parcels_dict = {}
for parcel_data in os.listdir(parcelas_path):
    filename, ext = parcel_data.split('.')
    name, number = filename.split('_')
    parcels_dict[number] = pd.read_csv(os.path.join(parcelas_path, parcel_data))


precleaned_data_dict = {}
with open(harvest_path, encoding='utf-8') as dates:
    harvest = json.load(dates)
    for harvest_dates in harvest:
        harvest_id = harvest_dates['parcela'][0]
        harvest_date = harvest_dates['parcela'][1]
        # print(harvest_date)
        harvest_range = pd.to_datetime(harvest_date)
        for id_, data_ in parcels_dict.items():
            if int(id_) == harvest_id:
                precleaned_data = prepare_data(data=data_, start_date=harvest_range[0], end_date=harvest_range[1])
                precleaned_data_dict[harvest_id] = precleaned_data


cleaned_data = {}
with open(cloudy_dates, encoding='utf-8') as clouds:
    clouddys = json.load(clouds)
    for clouddys_days in clouddys:
        to_delete = pd.to_datetime(clouddys_days['Fechas'])
        parcel_id = clouddys_days['Parcelas_id']
        for number_id, _data in precleaned_data_dict.items():
            if number_id == parcel_id:
                _data = _data[~_data['Fecha'].isin(to_delete)]
                cleaned_data[number_id] = _data

et_dict = {}

for et_data in os.listdir(et_path):
    filename_, ext_ = et_data.split('.')
    number_ = filename_.split('_')[-1]
    et_dict[number_] = pd.read_csv(os.path.join(et_path, et_data))

for key, value in cleaned_data.items():
    for key_, value_ in et_dict.items():
        value_['Fecha'] = value_['Fecha'].astype('datetime64[ns]')
        if key == int(key_):
            merged = pd.merge(value, value_, on='Fecha')
            # merged.drop(['Unnamed: 0'], axis=1, inplace=True)
            merged.to_csv(os.path.join(merged_path, f"parcela_{key}.csv"), index=False)
