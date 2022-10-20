# ESTRATEGIA DE TRADING Nº3: Marubozu en banda media
#### Por SaraSTEM
>_El éxito es quererte, querer lo que haces y querer cómo lo haces._ - Maya Angelou.

## Descripción de la estrategia

Esta semana he programado en Python la estrategia con la que empecé a operar en Bolsa. Consiste en comprar tras formarse una vela completa (llamada marubozu o longline) cruzando a la banda media de Bollinger. El stop se mueve a la altura de la media simple de 20 sesiones siempre que el precio haya superado al alza la banda superior de Bollinger. Para el caso bajista es justo al revés. 

Aquí tienes de ejemplo el backtest con el CRUDO en diario, pero al descargar la estrategia en tu ordenador, puedes probar con cualquier otro producto y cualquier otro timeframe, además de poder cambiar los parámetros de capital y gestión de riesgo como quieras para ver los resultados.

### Ejemplo de una entrada
![entrada](https://www.sarastem.com/wp-content/uploads/2022/06/entrada_estrategia3.png)
