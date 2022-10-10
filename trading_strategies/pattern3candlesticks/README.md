# ESTRATEGIA Nº2: Patrón de 3 velas en Bollinger
#### Por SaraSTEM
>_La bolsa es soberana y se coge el moño donde le da la gana._ - Mi padre.

## Descripción de la estrategia

Esta semana he programado en Python una estrategia de trading enviada por uno de mis grupos de clase donde, tras un patrón de tres velas rojas tocando la banda inferior de Bollinger, compramos si se produce una vela verde justo después. El stop se mueve a la altura de la media simple de 25 sesiones siempre que el precio haya superado al alza la banda superior de Bollinger. Para el caso bajista es justo al revés.

Aquí he hecho el backtest con el ORO en diario, pero al descargar la estrategia en tu ordenador, puedes probar con cualquier otro producto y cualquier otro timeframe, además de poder cambiar los parámetros de capital y gestión de riesgo como quieras para ver los resultados.

### Ejemplo de una entrada
![entrada](https://www.sarastem.com/wp-content/uploads/2022/06/entrada_estrategian2_.png)
