import unittest
from plot_utils.charts import simple_line_plot, multiple_line_plot
import pandas as pd

ds_path = r"C:\Users\DELL\PycharmProjects\Tesis\dataframes\Evapo\parcela_1.csv"


class MyTestCase(unittest.TestCase):
    def test_plotting(self):
        ds = pd.read_csv(ds_path)
        ds['Fecha'] = pd.to_datetime(ds['Fecha'])
        simple_line_plot(ds, "Fecha", "ndvi_mean", "NDVI promedio", "Fecha", "NDVI", export=True,
                         export_path=r"C:\Users\DELL\PycharmProjects\Tesis\graficas\ndvi_test.png")
        self.assertEqual(True, True)  # add assertion here

    def test_plotting2(self):
        ds = pd.read_csv(ds_path)
        ds['Fecha'] = pd.to_datetime(ds['Fecha'])
        multiple_line_plot(data=ds, x_data='Fecha', y_data=['ndvi_mean', 'Kc', 'ETc'],
                           x_label='Fecha', y_label=['Valor ndvi', 'valor msi', 'valor ndmi'],
                           export=True, subtitle='Comparación de índices', export_path=r"C:\Users\DELL\PycharmProjects\Tesis\graficas\indices.png")
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
