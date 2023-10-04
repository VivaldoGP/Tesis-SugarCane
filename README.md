# En este repo voy a desarrollar mi tesis de licenciatura.

El objetivo es estimar el rendimiento del cultivo de caña de azúcar a través de derivados satelitales,
en espécifico imágenes de la misión Sentinel 2 y los datos derivados de Agera5.

## Adquisición y procesamiento de las imágenes

Para esto se usarán las imágenes de Sentinel 2 en el nivel de procesamiento 2A, procesadas con la plataforma de
[Earth Engine](https://earthengine.google.com/) con la API de Python.

Dentro del repositorio se encuentran los notebooks de la adquisición y el procesamiento de las imágenes, en el
directorio [Notebooks](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/notebooks) se encuentran el notebook para
filtrar la colección de imágenes. Los filtros o parámetros son los siguientes:

1. Fecha de inicio y final
2. Tilde Id de la imagen, que en el caso de la zona es 14QML

Para cada imagen se accede a la banda que contiene el porcentaje de nubosidad, para valores mayores al 50% se considera
que el pixel corresponde a una nube, descartando las imágenes que contienen nubes en la zona de estudio. Dicha zona que
se encuentra en [Parcelas](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/Parcelas/Parcelas_estudio.geojson),
es el bbox de todas las parcelas.

Para cada parcela se exporta una imagen con las bandas necesarias para el cálculo de los índices deseados, teniendo así
un aproximado de 40 imágenes por polígono.

## Agera5
Para obtener los datos de evapotranspiración de referencia se descargan los datos de
[AgERA5](https://data.apps.fao.org/static/data/index.html?prefix=static%2Fdata%2Fc3s%2FAGERA5_ET0), para cada polígono 
correspondiente a una parcela se obtiene su centroide y así se extrae el valor de la ET.

## Procesamiento de las imágenes descargadas

Para cada imagen se calcula el NDVI y se almacena en un dataframe, con sus valores promedio, mínimo y máximo, con su
fecha, se une con los datos de ET haciendo un merge con las fechas de las imágenes con los de la ET.

