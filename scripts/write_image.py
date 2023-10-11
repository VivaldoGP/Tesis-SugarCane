import os
import rasterio
import numpy as np

from raster_utils.spectral_indices import ndvi, msi, ndmi

main_path = r"G:\Mi unidad\Tesis_5"
dest_path = r"C:\Users\DELL\PycharmProjects\Tesis\spectral_indices_images"

parcel_ids = [i.split('_')[1] for i in os.listdir(main_path)]


for root, dirs, files in os.walk(main_path):
    for dir_ in dirs:
        dir_path = os.path.join(root, dir_)
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            file_name = f"{file.split('.')[0]}_indices"
            with rasterio.open(file_path) as src:
                profile = src.profile
                profile.update(dtype=rasterio.float32, count=3)
                ndvi_band = ndvi(src)
                msi_band = msi(src)
                ndmi_band = ndmi(src)

                stacked = np.stack((ndvi_band, msi_band, ndmi_band))

                with rasterio.open(os.path.join(dest_path, f"{file_name}.tif"), 'w', **profile) as dst:
                    dst.descriptions = (['ndvi', 'msi', 'ndmi'])
                    dst.write(stacked.astype(rasterio.float32))
