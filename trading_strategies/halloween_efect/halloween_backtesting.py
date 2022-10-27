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


load_dotenv('variables_halloween.env')
product = os.environ['product']
period = os.environ['period']
interval = os.environ['interval']
capital = int(os.environ['capital'])
commission = float(os.environ['commission'])
margin = float(os.environ['margin'])
max_inv_product = float(os.environ['max_inv_product'])


class strategy_halloween(Strategy):
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
        data = data.iloc[:-1]
        data=data.reset_index()
        data['month'] = data['Date'].map(lambda x: x.strftime("%m"))


        # Buy
        data['signal'] = 0
        data['pr_signal'] = 0.0
        for i in range(len(data)):
            if data['month'][i] == '11' and data['month'][i-1] == '10':
                data['signal'][i] = 100
                data['pr_signal'][i] = data['Close'][i]

        # Close
        for i in range(len(data)):
            if data['month'][i] == '05' and data['month'][i-1] == '04':
                data['signal'][i] = -100
                data['pr_signal'][i] = data['Close'][i]

        # Investment
        data['cfds_buy'] = 0
        data = data.dropna()
        for x in range(len(data)):
            if data['pr_signal'][x] > 0 and data['signal'][x] == 100:
                data['cfds_buy'][x] = math.ceil((
                    max_inv_product*capital)/data['pr_signal'][x])

        data.index = pd.to_datetime(data['Date'])

        return data


    def next(self):
        pr_signal = self.data.pr_signal
        signal = self.data.signal
        cfds_buy = self.data.cfds_buy
        
        if signal == 100 and pr_signal > 0:
            bull = cfds_buy[np.argwhere(
                (signal == 100) & (pr_signal > 0))[-1]]
            self.buy(size=bull[0])
        if signal == -100 and pr_signal > 0:
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
