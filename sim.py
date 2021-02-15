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
        Returns: tuple of
            - dict containing the open/high/low/close of the past time period
            - true/false to indicate if the simulation is done

        If the simulation is done, the first return parameter will be None
        '''

        line = self._get_next()
        if not line:
            return None, True

        res = self._parse_line(line)
        return res, False

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
            if key in FLOAT_COLS:
                res[key] = float(val)
            elif key in INT_COLS:
                res[key] = int(val)
            else:
                res[key] = val

        return res

if __name__ == '__main__':
    fname = './data/eth_usdt_small.csv'
    sim = Sim(fname)
    for i in range(20):
        res, done = sim.step()
        print(f"Iter {i:2d} | {res}")
        if done:
            break
