from rasterio.mask import mask
from rasterio.io import DatasetReader


def mask_raster(raster: DatasetReader, shapefile):

    masked, mask_transform = mask(raster, shapefile, crop=True, nodata=None, filled=False)

    return masked.squeeze(), mask_transform
