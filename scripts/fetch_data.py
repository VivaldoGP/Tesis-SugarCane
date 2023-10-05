import ee
import json

ee.Initialize()


def does_intersect(img, feature_geom):
    """
    Esta función revisa si las geometrías de los parámetros intersectan.
    Args:
        img: Imagen de ee
        feature_geom: Geometría del feature o polígono

    Returns:
        Un valor True o False, dependiendo la operación.
    """
    intersecta = img.geometry().intersects(feature_geom, maxError=0.01)

    return intersecta.getInfo()


def count_cloud_pixels(img, cloud_percent, aoi):
    """
    Cuenta los pixeles considerados como nubes dentro de la zona de interés en la imagen
    Args:
        img: Imagen de ee
        cloud_percent: Porcentaje de nubosidad
        aoi: Zona de estudio

    Returns:
        Un diccionario con los valores de pixeles "limpios" y con nubes.
    """
    cloud_band = img.select('MSK_CLDPRB').gt(cloud_percent)
    pixel_count = cloud_band.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(),
        geometry=aoi,
        scale=10,
        maxPixels=1e9
    )

    return pixel_count.get('MSK_CLDPRB').getInfo()


def export_images(folder: str, img, bands, aoi, to_crs: str, filename):
    """
        Esta función exporta imágenes a un directorio en Google Drive.
    Args:
        folder: Directorio de destino en la raíz del drive
        img: Imagen de ee
        bands: Bandas de la imagen
        aoi: Región de interés
        to_crs: EPSG deseado para las imágenes exportadas
        filename: Nombre del archivo

    Returns:
        Una confirmación por cada imagen exportada correctamente.
    """
    raw_image = img.select(bands)

    export_params = {
        'driveFolder': f'{folder}',
        'fileFormat': 'GeoTiff',
        'scale': 10,
        'region': aoi,
        'crs': to_crs,
    }

    task = ee.batch.Export.image.toDrive(image=raw_image, description=filename, **export_params)

    task.start()
    task.status()

    return print(f"{filename} exportada correctamente.")


with open(r"C:\Users\DELL\PycharmProjects\Tesis\Parcelas\Parcelas_2.geojson", encoding='utf-8') as geom:
    parcelas = json.load(geom)

fc = ee.FeatureCollection(parcelas)

fc_bbox = fc.geometry().bounds()

'''
for feature in fc.getInfo()['features']:
    fn = ee.Feature(feature)
    area = fn.geometry().area()
    print(f"El área de {fn.getInfo()['properties']['Productor']} es {area.divide(10000).getInfo()}")
'''

start_date = '2022-01-01'
end_date = '2023-05-01'

ic = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(start=start_date, opt_end=end_date).filter(
    ee.Filter.eq('MGRS_TILE', '14QML')
)

try:
    inside = 0
    out = 0
    cloud_free = 0
    semi_free = 0

    images_ready = []

    for image in ic.getInfo()['features']:
        resultado = does_intersect(img=ee.Image(image['id']), feature_geom=fc_bbox)

        if resultado:
            inside += 1
            cloud_pixels = count_cloud_pixels(img=ee.Image(image['id']), cloud_percent=50, aoi=fc)
            if '1' not in cloud_pixels:
                # print(cloud_pixels, 'Limpia')
                images_ready.append(ee.Image(image['id']))
                cloud_free += 1
            elif '1' in cloud_pixels:
                if cloud_pixels['1'] < 3000:
                    images_ready.append(ee.Image(image['id']))
                    # print(cloud_pixels, 'menor a 3k')
                    semi_free += 1
        else:
            out += 1

    print(len(images_ready))
    print(f"Dentro: {inside}, Fuera: {out}, Libre de nubes: {cloud_free}, {semi_free}")

    # print(images_ready[1].getInfo()['id'])

    for i in images_ready:
        for feature in fc.getInfo()['features']:
            parcela = ee.Feature(feature)
            # print(f"Imagen: {i}, Parcela: {parcela.getInfo()['properties']['Id']}")
            export_images(folder='Tesis_caña4', img=i, bands=['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B11', 'B12'],
                          aoi=parcela.geometry(), to_crs='EPSG:32614',
                          filename=f"Parcela_{parcela.getInfo()['properties']['Id']}_{i.getInfo()['id'].replace('/', '_')}")
finally:
    print('f')
