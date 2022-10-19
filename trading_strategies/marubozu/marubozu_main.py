from marubozu_backtesting import strategy_marubozu


def results():
    strategy_marubozu.info()
    data = strategy_marubozu.strategy_body()
    stats = strategy_marubozu.run_bt(data, strategy_marubozu)
    results = {}
    return_ = round(stats[6], 2)
    return_buy_hold = round(stats[7], 2)
    return_ann = round(stats[8], 2)
    n_op = stats[17]
    win_ratio = round(stats[18], 2)
    drawdown = round(stats[13], 2)
    volatility = round(stats[9], 2)
    sharpe_ratio = round(stats[10], 2)
    sortino_ratio = round(stats[11], 2)
    calmar_ratio = round(stats[12], 2)
    profit_factor = round(stats[24], 2)
    sqn = round(stats[26], 2)
    dd_duration = stats[15]
    df_dd = stats._equity_curve
    dd_peak = df_dd.iloc[len(df_dd)-1]['DrawdownDuration']
    results = {'Rentabilidad (%)': return_, 'Rentabilidad anualizada (%)': return_ann, 'Número de operaciones': n_op, 'Ratio de aciertos (%)': win_ratio, 'Máximo Drawdown (%)': drawdown,
               'Volatilidad (%)': volatility, 'Ratio Sharpe': sharpe_ratio, 'Ratio Sortino': sortino_ratio,
               'Ratio Calmar': calmar_ratio, 'Factor de beneficio': profit_factor, 'Calidad': sqn, 'Benchmark': return_buy_hold,
               'Caída desde el pico': dd_peak, 'Duración DD': dd_duration}
    [print(key, ':', value) for key, value in results.items()]

    return results


if __name__ == "__main__":
    results()

