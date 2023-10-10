# Estructura de carpetas

En cada carpeta se almacenan los datos estadísticos por parcela, se dividen en 4 bloques principales:
1. [parcelas](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/parcelas), de forma simple es donde se
guardan los datos "crudos" obtenidos, dentro de esta carpeta se encuentra un csv por cada parcela, en este punto no están
limpios los datos y se pueden visualizar valores anormales debido a la presencia de nubes en la escena, cosa que posteriormente
soluciona.
2. [et](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/et), de igual forma que en la carpeta anterior,
por cada parcela se tiene un csv y en estos se almacenan los valores de la Evapotranspiración obtenidos del dataset 
*AgERA5*.
3. [merged](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/merged), en este punto las nubes fueron removidas y
los datos fueron recortados a las fechas de cosecha por cada parcela, se realizó la unión de los dos dataset anteriores.
4. [Evapo](https://github.com/VivaldoGP/Tesis-SugarCane/tree/main/dataframes/Evapo), se calcularon las variables de interés
y se almacenaron en csv individuales, teniendo así todos los datos necesarios para el estudio (casi).