class Arb

  def __init__(self, stocks, combo, ratio, etf, fee):
    self.stocks = stocks
    self.combo = combo
    self.etf = etf
    self.fee = fee
    self.ratio = ratio

  def run(self):
    # R to ETF
    v1 = 0
    good = True
    for i in self.combo:
      v1 += self.stocks[i[0]].get_sell(i[1])
      if v1 < 0:
        good = False

    if good and v1 + self.fee < self.etf.buy_price * self.ratio:
      self.buyR()
    
    # ETF to R
    v2 = 0
    for i in self.combo:
      v2 += self.stocks[i[0]].get_buy(i[1])
      if v2 < 0:
        good = False

    if good and self.etc.sell_price * self.ratio + self.fee  < v2:
      self.buyETF()

  def buyR(self):
    for i in self.combo:
      self.stocks[i[0]].buy(i[1])
    self.etf.buy_convert()
    self.etf.sell()

  def buyETF(self):
    self.etf.buy()
    self.etf.sell_convert()
    for i in self.combo:
      self.stocks[i[1]].sell(i[0])




