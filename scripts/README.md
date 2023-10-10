# Cómo replicar los procedimientos

En esta carpeta se encuentran varios scripts y cada uno cumple una función específica, aquí voy a describir su
funcionamiento y orden de ejecución.

## Adquisición de las imágenes

Primero necesitamos adquirir las imágenes, para eso se desarrolló el script
[ee_fetch_data.py](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/ee_fetch_data.py), el cual descarga
las imágenes a una carpeta de Google Drive, filtra las imágenes que coinciden con las parcelas de estudio, descarta las
que presentan nubes dentro de la geometría de cada una de las parcelas y descarga imágenes individuales por cada parcela.

### Adquisición de los datos de Evapotranspiración
Para esto es necesario crear un script que genere una request a la URL que almacena los archivos deseados, el script es
[dowload_et_images](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/analyze_et_data.py).

## Ordenamiento de las imágenes
Las imágenes se almacenaron en una sola carpeta, por lo que para un mejor manejo se desarrolló un script que ordena las 
imágenes en carpetas individuales dependiendo el id de la parcela.

[move_files](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/move_files.py) es el script que realiza esa tarea.


## Procesamiento de las imágenes

Las imágenes exportadas anteriormente son "crudas", solo contienen las bandas necesarias para posteriormente procesarlas
y para eso existe [analyze_data](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/analyze_data.py), el cual
calcula el ndvi y ndmi para cada imagen y después calcula las estadísticas básicas para imagen y parcela, exportando un 
csv con los datos calculados, estos csv se almacenan en la carpeta [parcelas](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/parcelas).

## Procesamiento de los datos ET

Para cada parcela se obtiene su centroide y se extrae el valor del pixel que intersecta con ese raster, o de forma más
básica, donde cae el punto del centroide, se exporta un csv para cada parcela y así se obtienen los datos de ET para la
zona en la que se encuentra cada parcela, [analyze_et_data](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/analyze_et_data.py)
realiza esta tarea.

## Unión de los datos

Teniendo ya procesados los datos, se procede a unirlos, para esto es necesario haber "limpiado" las imágenes de manera
manual, con esto me refiero a asegurar que no hay nubes o elementos extraños en la escena, ya que eso genera ruido y
valores anormales que perturban el comportamiento de los datos válidos. Resultado de esa limpieza se tienen las siguientes
fechas por parcela en las que hay presencia de nubes.

[Fechas con nubes](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/cloudy_images.json)

Después de hacer eso, se "recortan" los datos ajustados a las fechas de inicio y final del ciclo de desarrollo del cultivo, 
estos datos se encuentran en un archivo json para poder acceder a ellos fácilmente.

[Rango de fechas](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/Parcelas/harvest_dates.json) para cada parcela.

## Presentación de los datos

Finalmente se procede a calcular las variables faltantes, Kc y Etc, no explicaré eso aquí pero el script que hace esa
tarea es [kc_et](https://github.com/VivaldoGP/Tesis-SugarCane/blob/main/scripts/kc_et.py), exportando los datos a archivos
csv por parcela, almacenados en [Evapo](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/Evapo).

