# ESTRATEGIA DE TRADING Nº1: Envolvente en Bollinger
#### Por SaraSTEM
>_En mi vida he sufrido cosas terribles, aunque la mayoría de ellas nunca ocurrieron._ - Mark Twain.

## Descripción de la estrategia

Esta semana he programado en Python una estrategia con la que llevo trabajando mucho años y que avisa del impulso con mucha antelación. Consiste en comprar tras encontrar una envolvente que toque en alguna parte de su cuerpo o mecha la banda inferior de Bollinger. El stop se mueve a la altura de la banda media de Bollinger de 20 sesiones siempre que el precio haya cerrado por encima de la banda superior. Para el caso bajista es justo al revés. 

Aquí tienes de ejemplo el backtest con el DAX en 15min, pero al descargar la estrategia en tu ordenador, puedes probar con cualquier otro producto y cualquier otro timeframe, además de poder cambiar los parámetros de capital y gestión de riesgo como quieras para ver los resultados.

### Ejemplo de una entrada
![entrada](https://www.sarastem.com/wp-content/uploads/2022/06/entrada_estrategian1.png)
