```python
import backtrader as bt
import statsmodels.api as sm
import numpy as np

class PairsTrading(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0),)

    def __init__(self):
        self.data1_close = self.datas[0].close
        self.data2_close = self.datas[1].close
        
        self.order1 = None
        self.order2 = None

        self.hedge_ratio = None
        self.spread = None
        self.mean = None
        self.std = None

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        if order.ref == self.order1:
            self.order1 = None
        if order.ref == self.order2:
            self.order2 = None

    def next(self):
        if self.order1 or self.order2:
            return
            
        # Calculate hedge ratio and spread
        y = self.data1_close.get(size=self.params.period)
        x = self.data2_close.get(size=self.params.period)
        
        if len(y) < self.params.period or len(x) < self.params.period:
            return
            
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        self.hedge_ratio = model.params[1]
        
        self.spread = self.data1_close[0] - self.hedge_ratio * self.data2_close[0]
        
        spread_series = np.array(self.data1_close.get(size=self.params.period)) - self.hedge_ratio * np.array(self.data2_close.get(size=self.params.period))
        self.mean = np.mean(spread_series)
        self.std = np.std(spread_series)

        if not self.position:
            if self.spread > self.mean + self.params.devfactor * self.std:
                self.log('SELL SPREAD, %.2f' % self.spread)
                self.order1 = self.sell(data=self.datas[0])
                self.order2 = self.buy(data=self.datas[1], size = int(self.position.size * self.hedge_ratio))

            elif self.spread < self.mean - self.params.devfactor * self.std:
                self.log('BUY SPREAD, %.2f' % self.spread)
                self.order1 = self.buy(data=self.datas[0])
                self.order2 = self.sell(data=self.datas[1], size = int(self.position.size * self.hedge_ratio))

        else:
            if abs(self.spread - self.mean) < 0.5 * self.std:
                self.log('CLOSE POSITIONS, %.2f' % self.spread)
                self.close(data=self.datas[0])
                self.close(data=self.datas[1])


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Add the first data feed
    data1 = bt.feeds.YahooFinanceCSVData(
        dataname='../../datas/yhoo-1996-2015.txt',
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2002, 12, 31))
    cerebro.adddata(data1, name='YHOO')

    # Add the second data feed
    data2 = bt.feeds.YahooFinanceCSVData(
        dataname='../../datas/goog-2004-2015.txt',
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2002, 12, 31))
    cerebro.adddata(data2, name='GOOG')
    
    cerebro.addstrategy(PairsTrading)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
```
