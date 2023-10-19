import unittest
import os
import json
import pandas as pd
import numpy as np
from stats_utils.regression_models import simple_regression
from plot_utils.charts import regression_plot
from sklearn.metrics import mean_squared_error, r2_score


path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Parcelas_2.geojson"
df_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"


class MyTestCase(unittest.TestCase):
    def test_something(self):

        ndvi_promedio = {}

        for i in os.listdir(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"):
            df = pd.read_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo\{}".format(i))
            df['Fecha'] = df['Fecha'].astype('datetime64[ns]')
            df = df.sort_values(by='Fecha', ascending=True)
            file_name, ext = i.split('.')
            parcela_id = file_name.split('_')[1]

            with open(path, encoding='utf-8') as par:
                parcelas = json.load(par)
            for j in parcelas['features']:
                if int(parcela_id) == j['properties']['Id']:
                    # print(parcela_id, j['properties']['Rendimiento'])
                    ndvi_promedio[parcela_id] = (df['ndvi_mean'].mean(), df['ndmi_mean'].mean(), df['msi_mean'].mean(), df['ETc'].mean(), j['properties']['Rendimiento'], int(parcela_id))

        ndvi_yield_df = pd.DataFrame.from_dict(ndvi_promedio, orient='index', columns=['ndvi', 'ndwi', 'msi', 'etc', 'yield', 'id'])
        x = ndvi_yield_df[['ndvi', 'msi', 'ndwi']]
        y = ndvi_yield_df['yield']
        model = simple_regression(x, y)
        equation = 'y = {}x + ({})'.format(model.coef_, model.intercept_)
        y_pred = model.predict(x)
        ndvi_yield_df['predict'] = y_pred
        print(f"Coeficientes: {model.coef_}")
        print(f"Intercepto: {model.intercept_}")
        print(f"Error cuadrático medio: {mean_squared_error(y, y_pred)}")
        print(f"R2: {r2_score(y, y_pred)}")
        print(model.score(x, y))
        print(ndvi_yield_df.sort_values(by='id', ascending=True))

        self.assertEqual(True, True)  # add assertion here



if __name__ == '__main__':
    unittest.main()
