from __future__ import print_function
import sys

class ValueCalculator:
  
  def __init__(self):
    self.stocks = {
      "BOND": [],
      "VALBZ": [],
      "VALE": [],
      "GS": [],
      "MS": [],
      "WFC": [],
      "XLF": [],
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

    self.stocks[obj['symbol']].append(tot/num)

    print(tot/num, obj['symbol'])

  def get(self, stock):
    return self.stocks[stock][-1]
