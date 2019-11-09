import time
import backtrader as bt
import datetime as dt

from config import BINANCE, ENV, PRODUCTION, COIN_TARGET, COIN_REFER, DEBUG

from strategies.basic_rsi import BasicRSI
from utils import print_trade_analysis, print_sqn

class CustomDataset(bt.feeds.GenericCSVData):
    params = (
        ('time', -1),
        ('timestamp', 0),
        ('datetime', 1),
        ('open', 3),
        ('high', 4),
        ('low', 5),
        ('close', 6),
        ('volume', 7),
        ('openinterest', -1),
    )

class CustomDataset2(bt.feeds.GenericCSVData):
    params = (
        ('time', -1),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6),
    )

def main():
    cerebro = bt.Cerebro(quicknotify=True)

    data = CustomDataset(
            name=COIN_TARGET,
            dataname="data/gemini_BTCUSD_1hr-reversed.csv",
            timeframe=bt.TimeFrame.Minutes,
            fromdate=dt.datetime(2018, 1, 1),
            todate=dt.datetime(2018, 12, 30),
            nullvalue=0.0
        )

    class FullMoney(bt.sizers.PercentSizer):
        params = (
            ('percents', 99),
        )

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=1)

    broker = cerebro.getbroker()
    broker.setcommission(commission=0.001, name=COIN_TARGET)  # Simulating exchange fee
    broker.setcash(100000.0)
    cerebro.addsizer(FullMoney)

    # Analyzers to evaluate trades and strategies
    # SQN = Average( profit / risk ) / StdDev( profit / risk ) * SquareRoot( number of trades )
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    #cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='mysharpe')

    # Include Strategy
    cerebro.addstrategy(BasicRSI)

    # Starting backtrader bot
    initial_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % initial_value)
    result = cerebro.run()
    
    # Print analyzers - results
    final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_value)
    print('Profit %.3f%%' % ((final_value - initial_value) / initial_value * 100))
    print_sqn(result[0].analyzers.sqn.get_analysis())
    #print('Sharpe Ratio:', result[0].analyzers.mysharpe.get_analysis())
    print_trade_analysis(result[0].analyzers.ta.get_analysis())
    

    # plot result
    if DEBUG:
        cerebro.plot()
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("finished.")
        time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        print("Finished finished at time: ", time)
    except Exception as err:
        print("Finished with error: ", err)
        raise