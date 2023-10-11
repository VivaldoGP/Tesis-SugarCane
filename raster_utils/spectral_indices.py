from rasterio import DatasetReader


def ndvi(img: DatasetReader, nir_band: int = 4, red_band: int = 3):
    """
    Calcula el ndvi
    Args:
        nir_band:
        red_band:
        img: un imagen de rasterio

    Returns:
        un ndarray con los valores del ndvi para pixel
    """
    nir_band = img.read(nir_band)
    red_band = img.read(red_band)

    ndvi_band = (nir_band.astype(float) - red_band.astype(float)) / (nir_band.astype(float) + red_band.astype(float))

    return ndvi_band


def msi(img: DatasetReader, swir_band: int = 5, nir_band: int = 4):
    """
    Calcula el msi
    Args:
        swir_band:
        nir_band:
        img: Una imagen de rasterio

    Returns:
        un ndarray con los valores del msi para pixel
    """
    swir_band = img.read(swir_band)
    nir_band = img.read(nir_band)

    msi_band = swir_band.astype(float) / nir_band.astype(float)

    return msi_band


def ndmi(img: DatasetReader, swir_band: int = 5, nir_band: int = 4):
    """
    Calcula el ndmi
    Args:
        swir_band:
        nir_band:
        img: un imagen de rasterio

    Returns:
        un ndarray con los valores del ndvi para pixel
    """
    nir_band = img.read(nir_band)
    swir_band = img.read(swir_band)

    ndmi_band = (nir_band.astype(float) - swir_band.astype(float)) / (nir_band.astype(float) + swir_band.astype(float))

    return ndmi_band
