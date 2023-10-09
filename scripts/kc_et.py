import os
import pandas as pd

data_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\merged"
evapo_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"

parcelas_df = {}

for i in os.listdir(data_path):
    filename, ext = i.split('.')
    name, number = filename.split('_')
    parcelas_df[number] = pd.read_csv(os.path.join(data_path, i))

for parcela_id, parcela_df in parcelas_df.items():
    parcela_df['Kc'] = 1.15 * parcela_df['ndvi_mean'] + 0.17
    parcela_df['ETc'] = parcela_df['Kc'] * parcela_df['Valor']
    parcela_df.to_csv(os.path.join(evapo_path, f"parcela_{parcela_id}.csv"), index=True)
