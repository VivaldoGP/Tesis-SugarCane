import unittest
from vector_utils.geopro_toos import mem_buffer, mem_centroid
from fiona import MemoryFile
from shapely.geometry import shape
from shapely import area

path = r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\SHP\Parcelas.shp"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mem = mem_buffer(path, buffer_size=-5)
        if type(mem) == MemoryFile:
            with mem.open() as mem:
                for feature in mem:
                    print(feature['properties']['Productor'])
                    print(area(shape(feature.geometry)))
            self.assertEqual(True, True)
        else:
            self.assertEqual(True, False)  # add assertion here
            print(type(mem))

    def test_centroids(self):

        mem = mem_centroid(path)
        if type(mem) == MemoryFile:
            with mem.open() as mem:
                for feature in mem:
                    print(feature['properties']['Productor'])
                    print(feature.geometry['coordinates'])
            self.assertEqual(True, True)
        else:
            self.assertEqual(True, True)
            print(type(mem))


if __name__ == '__main__':
    unittest.main()
