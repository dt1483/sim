import pdb
from collections import namedtuple
import numpy as np
from sim import Sim

Transaction = namedtuple("Transaction", ("buy_price", "sell_price", "amount", "buy_time", "sell_time"))

class SimpleTrader:
    def __init__(self, buy_len, sell_len, buy_limit):
        '''
        buy_len: int, window of time (number of previous time steps) to consider when making a buy decision
        sell_len: int, window of time (number of previous time steps) to consider when making a sell decision
        buy_limit: float, units of asset to buy

        This simple trader will:
        - buy if the current price is less than the average of the previous {buy_len} time steps.
        - sell if the current bought price is higher than the average of the previous {sell_len}
        time steps

        If the SimpleTrader is holding, it can only hold or sell
        '''
        self.buy_len = buy_len
        self.sell_len = sell_len
        self.buy_limit = buy_limit
        self._hist_buy_price = np.zeros(buy_len) # cache the potential buy/sell prices
        self._hist_sell_price = np.zeros(sell_len)

        self._cnt = 0
        self._pnl = 0
        self._txs = []
        self._holding = False
        self._last_buy_price = None
        self._last_buy_time = None

    def act(self, exchange_data):
        # can only buy at hi, can only sell at low
        self._hist_buy_price[self._cnt % len(self._hist_buy_price)] = exchange_data['high']
        self._hist_sell_price[self._cnt % len(self._hist_sell_price)] = exchange_data['low']

        if self._holding:
            self.maybe_sell(exchange_data)
        elif not self._holding:
            self.maybe_buy(exchange_data)

        self._cnt += 1

    def maybe_buy(self, exchange_data):
        '''
        buy if: current buy price ("high") is lower than the avg of the previous buy prices
        '''

        # cannot buy if already holding
        if self._holding:
            return

        buy_price = exchange_data['high']
        avg_past_price = self._hist_buy_price[-self.buy_len:].mean()
        if buy_price < avg_past_price:
            # toggling holding counts as "buying"
            self._holding = True
            self._last_buy_price = buy_price
            self._last_buy_time = exchange_data['date']

    def maybe_sell(self, exchange_data):
        '''
        sell if: current sell price ("low") is lower than the previous sell prices
        '''
        if not self._holding:
            return

        sell_price = exchange_data['low']
        sell_time = exchange_data['date']
        avg_past_price = self._hist_sell_price[-self.sell_len:].mean()

        if sell_price > avg_past_price and sell_price > self._last_buy_price:
            tx = Transaction(self._last_buy_price,
                             sell_price,
                             self.buy_limit,
                             self._last_buy_time,
                             sell_time)
            self._txs.append(tx)
            self._pnl += (sell_price - self._last_buy_price) * self.buy_limit

            # toggle variables
            self._holding = False
            self._last_buy_price = None
            self._last_buy_time = None

    def pnl(self):
        return sum([(x.sell_price - x.buy_price) * x.amount for x in self._txs])

    def transactions(self):
        return self._txs

if __name__ == '__main__':
    fname = './data/eth_usdt_med.csv'
    sim = Sim(fname)
    sim_iters = 50000
    buy_len = 3
    sell_len = 2
    limit = 0.01 # amount to buy
    trader = SimpleTrader(buy_len, sell_len, limit)
    done = False

    for i in range(sim_iters):
        exchange_data, done = sim.step()

        if done:
            break

        trader.act(exchange_data)

    print("Done simulating {} steps".format(i))
    print("SimpleTrader params: buy len {}, sell len {}, buy limit {}".format(
        buy_len, sell_len, limit
    ))
    print("PnL: {:.3f}".format(trader.pnl()))
    print("First 3 transactions:")
    for t in trader.transactions()[:3]:
        print(t)
