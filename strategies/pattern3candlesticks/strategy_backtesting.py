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


load_dotenv('variables.env')
product = os.environ['product']
period = os.environ['period']
interval = os.environ['interval']
period_bb = int(os.environ['period_bb'])
period_avg = int(os.environ['period_avg'])
risk_op = float(os.environ['risk_op'])
capital = int(os.environ['capital'])
commission = float(os.environ['commission'])
margin = float(os.environ['margin'])


class strategy_pattern3candlesticks(Strategy):

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
        data['AVG'] = ta.MA(data['Close'], timeperiod=period_avg, matype=0)

        # Buy/Sell
        data['signal'] = 0
        for i in range(len(data)):
            if data['Close'][i-1] < data['Open'][i-1] and data['Close'][i-2] < data['Open'][i-2] and data['Close'][i-3] < data['Open'][i-3] and data['Close'][i] > data['Open'][i] and ((data['Low'][i-1] < data['LBB'][i-1]) and (data['Low'][i-2] < data['LBB'][i-2]) and (data['Low'][i-3] < data['LBB'][i-3])):
                data['signal'][i] = 100
            elif data['Close'][i-1] > data['Open'][i-1] and data['Close'][i-2] > data['Open'][i-2] and data['Close'][i-3] > data['Open'][i-3] and data['Close'][i] < data['Open'][i] and ((data['High'][i-1] > data['UBB'][i-1]) and (data['High'][i-2] > data['UBB'][i-2]) and (data['High'][i-3] > data['UBB'][i-3])):
                data['signal'][i] = -100

        # Stop Loss
        data['pr_signal'] = 0.0
        data['stop_buy'] = 0.0
        data['stop_sell'] = 0.0
        data_ = data
        data_ = data_.reset_index()

        # First
        for t in range(len(data)):
            if data['signal'][t] == 100:
                data['pr_signal'][t] = data['Close'][t]
                stop_a = data_.loc[t-4:t, 'Low'].min()
                data['stop_buy'][t] = stop_a
            elif data['signal'][t] == -100:
                data['pr_signal'][t] = data['Close'][t]
                stop_b = data_.loc[t-4:t, 'High'].max()
                data['stop_sell'][t] = stop_b

        # Continue
        for x in range(len(data)):
            if data['Close'][x] > data['UBB'][x]:
                data['stop_buy'][x] = data['AVG'][x]
            if data['Close'][x] < data['LBB'][x]:
                data['stop_sell'][x] = data['AVG'][x]

        data['stop_buy'].replace(0, np.nan, inplace=True)
        data['stop_buy'].fillna(method='ffill', inplace=True)
        data['stop_buy'] = data['stop_buy'].fillna(0)
        data['stop_sell'].replace(0, np.nan, inplace=True)
        data['stop_sell'].fillna(method='ffill', inplace=True)
        data['stop_sell'] = data['stop_sell'].fillna(0)

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
        if signal == 100 and pr_signal > 0:
            bull = cfds_buy[np.argwhere(
                (signal == 100) & (pr_signal > 0))[-1]]
            self.buy(size=bull[0])
        if signal == -100 and pr_signal > 0:
            bear = cfds_sell[np.argwhere(
                (signal == -100) & (pr_signal > 0))[-1]]
            self.sell(size=bear[0])
        for trade in self.trades:
            if trade.is_long:
                trade.sl = stop_buy
            if trade.is_short:
                trade.sl = stop_sell


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


