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
    best_buy = obj['buy'][0][1]
    best_sell = obj['sell'][0][1]

    tot = 0.0
    num = 0
    for price,size in obj['buy']:
      if abs(price - best_buy)/best_buy < 0.1:
        tot += price * size
        num += size

    for price,size in obj['sell']:
      if abs(price - best_sell)/best_sell < 0.1:
        tot += price * size
        num += size

    self.stocks[obj['symbol']].append(tot/num)

    print(tot/num, obj, file=sys.stderr)

  def get(self, stock):
    return self.stocks[stock][-1]
