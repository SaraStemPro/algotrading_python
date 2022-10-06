from strategy_backtesting import strategy_marubozu


def results():
    data = strategy_marubozu.strategy_body()
    stats = strategy_marubozu.run_bt(
        data, strategy_marubozu)
    results = {}
    return_ = round(stats[6], 2)
    n_op = stats[17]
    win_ratio = round(stats[18], 2)
    drawdown = round(stats[13], 2)
    volatility = round(stats[9], 2)
    sharpe_ratio = round(stats[10], 2)
    results = {'Rentabilidad (%)': return_, 'Nº trades': n_op, 'Ratio de aciertos (%)': win_ratio, 'Máx. Drawdown (%)': drawdown,
               'Volatilidad (%)': volatility, 'Ratio Sharpe': sharpe_ratio}
    [print(key, ':', value) for key, value in results.items()]

    return results

if __name__ == "__main__":
    strategy_marubozu.info()
    results()
