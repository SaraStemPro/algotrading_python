# ESTRATEGIA DE TRADING Nº4: Cruce de medias ajustado
#### Por SaraSTEM
>_Sé tú mismo. Todos los demás ya están ocupados._- Óscar Wilde.

## Descripción de la estrategia

Esta semana he programado en Python una estrategia diseñada por uno de mis grupos de clase. Consiste en marcar dos medias móviles en el gráfico, de 8 y de 50 periodos y comprar cuando ambas se crucen y el precio esté por encima de dicho cruce. Pero añadimos un ajuste de volatilidad, ya que también le pedimos que el máximo de la vela no esté por encima de la banda superior de Bollinger de 20 periodos. Para el caso bajista es justo al revés.

Aquí tienes de ejemplo el backtest con el ALGODÓN (COTTON) en 1 hora, pero al descargar la estrategia en tu ordenador, puedes probar con cualquier otro producto y cualquier otro timeframe, además de poder cambiar los parámetros de capital y gestión de riesgo como quieras para ver los resultados.

### Ejemplo de una entrada
![entrada](https://www.sarastem.com/wp-content/uploads/2022/10/Captura-de-pantalla-2022-10-20-a-las-19.36.44-p. m..png)
