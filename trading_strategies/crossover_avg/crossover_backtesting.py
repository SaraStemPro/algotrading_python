from dotenv import load_dotenv
from backtesting import Backtest, Strategy
import yfinance as yf
import talib as ta
import pandas as pd
import numpy as np
import math
import os
import warnings
warnings.filterwarnings('ignore')


load_dotenv('variables_crossover.env')
product = os.environ['product']
period = os.environ['period']
interval = os.environ['interval']
period_bb = int(os.environ['period_bb'])
risk_op = float(os.environ['risk_op'])
capital = int(os.environ['capital'])
commission = float(os.environ['commission'])
margin = float(os.environ['margin'])
max_inv_product = float(os.environ['max_inv_product'])


class strategy_crossover_avg(Strategy):
    max_inv_product = float(os.environ['max_inv_product'])


    def init(self):
        pass


    @staticmethod
    def info():
        print(product, interval, period)


    @staticmethod
    def strategy_body():
        # Download data
        data = yf.download(tickers=product,
                           period=period, interval=interval)
        if interval == '5m' or interval == '15m' or interval == '1h':
            data = data.reset_index()
            data = data.rename({'index': 'Datetime'}, axis=1)
            data.index = pd.to_datetime(
                data['Datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
            data = data.drop(['Datetime'], axis=1)
        data.index = pd.to_datetime(data.index)
        data = data.iloc[:-1]
        # Indicators
        data['UBB'], data['MBB'], data['LBB'] = ta.BBANDS(
            data['Close'], period_bb)
        data['AVG_8'] = ta.MA(data['Close'], timeperiod=8, matype=0)
        data['AVG_50'] = ta.MA(data['Close'], timeperiod=50, matype=0)

        # Buy/Sell and Stop Loss
        data['signal'] = 0
        data['pr_signal'] = 0.0
        data['stop_buy'] = data['LBB']
        data['stop_sell'] = data['UBB']
        for i in range(len(data)):
            if data['AVG_8'][i] > data['AVG_50'][i] and data['AVG_8'][i-1] < data['AVG_50'][i-1] and data['Close'][i] > data['AVG_8'][i] and data['Close'][i] > data['AVG_50'][i] and data['High'][i] < data['UBB'][i]:
                data['signal'][i] = 100
                data['pr_signal'][i] = data['Close'][i]
            elif data['AVG_8'][i] < data['AVG_50'][i] and data['AVG_8'][i-1] > data['AVG_50'][i-1] and data['Close'][i] < data['AVG_8'][i] and data['Close'][i] < data['AVG_50'][i] and data['Low'][i] < data['LBB'][i]:
                data['signal'][i] = -100
                data['pr_signal'][i] = data['Close'][i]

        # Investment
        data['cfds_buy'] = 0
        data['cfds_sell'] = 0
        data = data.dropna()
        for x in range(len(data)):
            if data['pr_signal'][x] > 0 and data['signal'][x] == 100:
                data['cfds_buy'][x] = math.ceil(
                    (risk_op*capital)/(data['pr_signal'][x]-data['stop_buy'][x]))
            elif data['pr_signal'][x] > 0 and data['signal'][x] == -100:
                data['cfds_sell'][x] = math.ceil(
                    abs((risk_op*capital)/(data['pr_signal'][x]-data['stop_sell'][x])))

        return data


    def next(self):
        pr_signal = self.data.pr_signal
        signal = self.data.signal
        cfds_buy = self.data.cfds_buy
        cfds_sell = self.data.cfds_sell
        stop_buy = self.data.stop_buy
        stop_sell = self.data.stop_sell
        if not self.position.is_long:
            if signal == 100 and pr_signal > 0:
                bull = cfds_buy[np.argwhere(
                    (signal == 100) & (pr_signal > 0))[-1]]
                if margin*(bull[0]*pr_signal) < (self.max_inv_product*capital):
                    self.buy(size=bull[0])
        if not self.position.is_short:
            if signal == -100 and pr_signal > 0:
                bear = cfds_sell[np.argwhere(
                    (signal == -100) & (pr_signal > 0))[-1]]
                if margin*(bear[0]*pr_signal) < (self.max_inv_product*capital):
                    self.sell(size=bear[0])
        for trade in self.trades:
            if trade.is_long:
                if self.data.Low < stop_buy:
                    self.position.close()
            if trade.is_short:
                if self.data.High > stop_sell:
                    self.position.close()


    def run_bt(data, strategy):
        btest = Backtest(data, strategy, cash=capital, commission=commission,
                         exclusive_orders=False, hedging=True, trade_on_close=True, margin=margin)
        stats = btest.run()
        graphs = 'graphs'
        if not os.path.exists(graphs):
            os.makedirs(graphs)
        btest.plot(open_browser=False, filename='graphs/' +
                   product+'_'+interval+'_'+period)
        
        return stats


    def walk_forward(data, strategy, warmbull_bars, lookback_bars, validation_bars):
        # The code for Walk Forward Testing
        stats_master = []
        for i in range(lookback_bars + warmbull_bars, len(data)-validation_bars, validation_bars):
            training_data = data.iloc[i-lookback_bars-warmbull_bars:i]
            validation_data = data.iloc[i-warmbull_bars:i+validation_bars]
            bt_training = Backtest(training_data, strategy, cash=capital, commission=commission,
                                   exclusive_orders=False, hedging=True, trade_on_close=True, margin=margin)
            stats_training = bt_training.optimize(
                max_inv_product=[0.15, 0.45, 0.1], maximize='SQN')
            print(stats_training._strategy)
            max_inv_product = stats_training._strategy.max_inv_product
            bt_validation = Backtest(validation_data, strategy, cash=capital, commission=commission,
                                     exclusive_orders=False, hedging=True, trade_on_close=True, margin=margin)
            stats_validation = bt_validation.run(
                max_inv_product=max_inv_product)

            stats_master.append(stats_validation)
        
        return stats_master
