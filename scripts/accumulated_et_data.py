import pandas as pd
from pandas import DataFrame
import datetime
import os
import json

stats_df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\stats"
et_df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\et"
fechas = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\harvest_dates.json"


def prepare_data(data: DataFrame, start_date: datetime.datetime, end_date: datetime.datetime):

    data['Fecha'] = data['Fecha'].astype('datetime64[ns]')
    data = data.sort_values(by='Fecha', ascending=True)
    data = data[(data['Fecha'] >= start_date) & (data['Fecha'] < end_date)]

    return data


et_dict = {}
for et_data in os.listdir(et_df_path):
    filename, ext = et_data.split('.')
    number = filename.split('_')[-1]
    et_dict[number] = pd.read_csv(os.path.join(et_df_path, et_data))

cleaned_data = {}
with open(fechas, encoding='utf-8') as dates:
    harvest_dates = json.load(dates)
    for harvest_date in harvest_dates:
        harvest_id = harvest_date['parcela'][0]
        harvest_range = pd.to_datetime(harvest_date['parcela'][1])
        for id_, data_ in et_dict.items():
            if int(id_) == harvest_id:
                precleaned_data = prepare_data(data=data_, start_date=harvest_range[0], end_date=harvest_range[1])
                # precleaned_data.to_csv(os.path.join(stats_df_path, f'et_{id_}.csv'), index=False)
                cleaned_data[id_] = precleaned_data

et_stats = []
for i, j in cleaned_data.items():
    et_stats.append({"Parcela": i, "ET_acumulado": j['Valor'].sum(), "ET_promedio": j['Valor'].mean()})

et_stats_df = pd.DataFrame(et_stats)
et_stats_df.to_csv(os.path.join(stats_df_path, 'et_stats.csv'), index=False)
