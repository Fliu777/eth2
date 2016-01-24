from __future__ import print_function
import math
import sys
import time
import scipy
import random
from scipy import stats
import numpy as np

class ValueCalculator:
  
  def __init__(self, client):
    self.connection = client
    self.stocks = {
      "BOND": [[],[]],
      "VALBZ": [[],[]],
      "VALE": [[],[]],
      "GS": [[],[]],
      "MS": [[],[]],
      "WFC": [[],[]],
      "XLF": [[],[]],
    }

  def feed(self, obj, t0):
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
    self.stocks[obj['symbol']][1].append(time.time() - t0)

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
    return
    for s in ["GS","MS","WFC"]:
      tt = self.stocks[s][1][-1]
      i = len(self.stocks[s][1])-1
      while i >= 0 and self.stocks[s][1][i] > tt - 20:
        i -= 1
      
      x = np.array(self.stocks[s][0][-i:])
      t = np.array(self.stocks[s][1][-i:])
      
      if len(x) < 10: return
      slope, intercept, r_value, p_value, std_err = stats.linregress(t, x)

      if r_value**2 > 0.7:
        print(x,t)
        print(slope, intercept)
        fy = slope * (tt + 20) + intercept
        if fy/self.stocks[s][0][-1] > 1.01:
           self.sendOrder(True, s, 10, int(math.ceil(self.stocks[s][0][-1])))
        if fy/self.stocks[s][0][-1] < 0.99:
           self.sendOrder(False, s, 10, int(math.floor(self.stocks[s][0][-1])))

  def sendOrder(self, isBuy, name,amount, price):
    return
    buy_sell_msg = {
        "type": "add",
        "order_id": random.randint(10000,1000000),
        "symbol": name,
        "dir": None,
        "price": price,
        "size": amount,
    }
    print(buy_sell_msg)
    if isBuy:
      buy_sell_msg['dir'] = "BUY"
      self.connection.send(buy_sell_msg)
    else:
      buy_sell_msg['dir'] = "SELL"
      self.connection.send(buy_sell_msg)



