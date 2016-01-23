from __future__ import print_function
import sys
import time
import scipy

from scipy import stats
import numpy as np

class ValueCalculator:
  
  def __init__(self):
    self.stocks = {
      "BOND": [[],[]],
      "VALBZ": [[],[]],
      "VALE": [[],[]],
      "GS": [[],[]],
      "MS": [[],[]],
      "WFC": [[],[]],
      "XLF": [[],[]],
    }

  def feed(self, obj):
    if len(obj['buy']) == 0 or len(obj['sell']) == 0:
      return

    best_buy = obj['buy'][0][0]
    best_sell = obj['sell'][0][0]

    tot = 0.0
    num = 0
    for price,size in obj['buy']:
      if abs(price - best_buy)/float(best_buy) < 0.05:
        tot += price * size
        num += size

    for price,size in obj['sell']:
      if abs(price - best_sell)/float(best_sell) < 0.05:
        tot += price * size
        num += size

    self.stocks[obj['symbol']][0].append(tot/num)
    self.stocks[obj['symbol']][1].append(time.time())

    # print(tot/num, obj['symbol'])

  def get(self, stock):
    return self.stocks[stock][-1]

  def report(self):
    with open("sequence.log", 'w') as f:
      f.write(str(self.stocks['VALBZ']) + '\n')
      f.write(str(self.stocks['VALE']) + '\n')
      print(self.stocks['VALBZ'][-1])
      print(self.stocks['VALE'][-1])

  def ml(self):
    for s in self.stocks:
      t = self.stocks[s][1][-1]
      i = len(self.stocks[s][1])
      while i > 0 and self.stocks[s][1][i] < t - 30:
        i -= 1
      x = np.array(self.stocks[s][0][-i:])
      t = np.array(self.stocks[s][1][-i:])

      slope, intercept, r_value, p_value, std_err = stats.linregress(x,t)

      if r_value**2 > 0.7:
        print(x,t)
        fy = slope * (t + 30) + intercept
        print(fy)



