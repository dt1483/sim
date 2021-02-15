import pdb
import time
import io

FLOAT_COLS = [
    'open', 'high', 'low', 'close', 'Volume ETH',
    'Volume USDT'
]
INT_COLS = ["tradecount"]

class Sim:
    def __init__(self, fname):
        '''
        fname: string name of file containing historical data csv
        '''
        self.fname = fname
        self.file_handle = io.open(fname)
        self.attrs = self._get_next().strip().split(",")

    def step(self):
        '''
        Returns: dict containing the open/high/low/close of the past time period
        '''
        line = self._get_next()
        res = self._parse_line(line)
        return res

    def _get_next(self):
        '''
        Grabs the next line in the csv
        '''
        return self.file_handle.readline().strip()

    def _parse_line(self, line):
        '''
        line: string containing contents of the current line of the csv
        Returns: dict containing current price data
        '''
        res = {}
        split = line.split(",")
        for idx, val in enumerate(split):
            key = self.attrs[idx]
            if val in FLOAT_COLS:
                res[key] = float(val)
            elif val in INT_COLS:
                res[key] = int(val)
            else:
                res[key] = val

        return res

if __name__ == '__main__':
    fname = './data/eth_usdt_small.csv'
    sim = Sim(fname)
    print(sim.step())
