# Análisis de los datos

Recapitulando, se cuentan con 15 parcelas de estudio (la 12 se descartó de momento),
de la 5 a la 11 le pertenecen a la misma persona y conforman un lote de parcelas de las cuales
el rendimiento es el mismo para las 7, esto debido a que así lo registra el Ingenio, 
la diferencia son las fechas de corte por lo que se asumieron como parcelas individuales.
El problema llega al momento de realizar un análisis estadístico, por lo que la solución inicial propuesta 
es la siguiente:

## Primera opción

Asignarle un porcentaje de rendimiento a cada parcela en función de sus áreas,
pero esto de momento no ha sido posible.

## Segunda opción

De las 7 parcelas se obtiene el promedio del **NDVI**, y al tener el mismo rendimiento se le puede asignar ese valor
promedio al rendimiento. Así tendríamos una parcela única que en realidad sería el lote original y se puede agregar a la
regresión lineal junto a los datos de las otras parcelas.

