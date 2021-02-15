## Sim
`sim.py` is a simple class that replays historical data from a csv. It has one function `step` which
simply returns a dictionary containing price data of the next time step in the given
historical data csv.

## Sample Usage
```
from sim import Sim

fname = './data/eth_usdt_small.csv'
sim = Sim(fname)
print(sim.step())
```
