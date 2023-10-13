import unittest
import os
import json
from plot_utils.charts import simple_line_plot, multiple_line_plot, regression_plot
import pandas as pd
from sklearn.linear_model import LinearRegression

ds_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo\parcela_11.csv"


class MyTestCase(unittest.TestCase):
    def test_plotting(self):
        ds = pd.read_csv(ds_path)
        ds['Fecha'] = pd.to_datetime(ds['Fecha'])
        simple_line_plot(ds, "Fecha", "ndvi_mean", "NDVI promedio", "Fecha", "NDVI", export=False,
                         export_path=r"C:\Users\DELL\PycharmProjects\Tesis\graficas\ndvi_test.png")
        self.assertEqual(True, True)  # add assertion here

    def test_plotting2(self):
        ds = pd.read_csv(ds_path)
        ds['Fecha'] = pd.to_datetime(ds['Fecha'])
        multiple_line_plot(data=ds, x_data='Fecha', y_data=['ndvi_mean', 'Kc', 'ETc'],
                           x_label='Fecha', y_label=['Valor ndvi', 'valor msi', 'valor ndmi'],
                           export=True, subtitle='Comparación de índices', export_path=r"C:\Users\DELL\PycharmProjects\Tesis\graficas\indices.png")
        self.assertEqual(True, True)  # add assertion here

    def test_plotting3(self):

        ndvi_promedio = {}

        for i in os.listdir(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo"):
            df = pd.read_csv(r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo\{}".format(i))
            df['Fecha'] = df['Fecha'].astype('datetime64[ns]')
            df = df.sort_values(by='Fecha', ascending=True)
            file_name, ext = i.split('.')
            parcela_id = file_name.split('_')[1]
            ndvi_promedio[parcela_id] = df['ndvi_mean'].mean()

        ndvi_promedio.pop('12')
        with open(r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Parcelas_2.geojson") as parcelas:
            parcelas = json.load(parcelas)

        ndvi_yield = {}
        for id_, ndvi_value in ndvi_promedio.items():
            for i in parcelas['features']:
                if i['properties']['Id'] == int(id_):
                    print(ndvi_value, i['properties']['Rendimiento'])
                    ndvi_yield[id_] = (ndvi_value, i['properties']['Rendimiento'])

        ndvi_yield_df = pd.DataFrame.from_dict(ndvi_yield, orient='index', columns=['ndvi', 'yield'])
        X = ndvi_yield_df['ndvi'].values.reshape(-1, 1)
        y = ndvi_yield_df['yield'].values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        equation = 'y = {}x + ({})'.format(model.coef_[0][0], model.intercept_[0])
        equation_2 = 'y = 176.09x + 53.475'
        y_pred = model.predict(X)
        ndvi_yield_df['predict'] = y_pred

        article_data = {
            '20': (0.36903, 115.4, 118.46),
            '21': (0.3803, 119.5, 120.44),
            '22': (0.34294, 111.4, 113.86),
            '23': (0.36155, 117.1, 117.14),
            '24': (0.36822, 118.4, 118.32),
            '25': (0.36149, 117.8, 117.13),
            '26': (0.38484, 124.8, 121.24),
            '27': (0.37575, 115, 119.64),
            '28': (0.42134, 127.4, 127.67),
            '29': (0.37896, 124.6, 120.21),
            '30': (0.34917, 110.6, 114.96),
            '31': (0.25724, 97.4, 98.77),
            '32': (0.38454, 122.1, 121.19),
            '33': (0.28536, 104.2, 103.72),
            '34': (0.32225, 110.1, 110.22),
            '35': (0.32615, 113.2, 110.91),
            '36': (0.23933, 95.9, 95.62),
            '37': (0.33058, 113.4, 111.69),
            '38': (0.3198, 110.5, 109.79),
            '39': (0.34046, 116.2, 113.43),
            '40': (0.30194, 107, 106.64),
            '41': (0.34599, 113.3, 114.4),
            '42': (0.39713, 123.4, 123.41)
        }

        article_data_df = pd.DataFrame.from_dict(article_data, orient='index', columns=['ndvi', 'yield', 'predict'])

        regression_plot(data=ndvi_yield_df, extra_data=article_data_df, title='Relación ndvi vs rendimiento', x_label='NDVI', y_label='Toneladas por Ha', legend=equation, score=model.score(X, y), legend_2=equation_2,
                        export=True, export_path=r"C:\Users\DELL\PycharmProjects\Tesis\graficas\regresion_articulo.png")
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
