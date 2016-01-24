class Stock
  def __init__(self, symbol, client):
    self.symbol = symbol
    self.client = client
    self.book = None

  def update(book):
    self.book = book

  def sell(self, a = 1):
    for i in self.book['buy']:
      if i[1] >= a:
        self.sendOrder(False, a, i[0])
        break
      self.sendOrder(False, i[1], i[0])
      tot += i[0] * i[1]
      a -= i[1]

  def buy(self, a = 1):
    for i in self.book['buy']:
      if i[1] >= a:
        self.sendOrder(True, a, i[0])
        break
      self.sendOrder(True, i[1], i[0])
      tot += i[0] * i[1]
      a -= i[1]
    if a > 0:
      return -99999
    return tot

  def sell_convert(self, a = 1):
    self.convert(False, a)

  def buy_convert(self, a = 1):
    self.convert(True, a)

  def get_sell(self, a = 1):
    if not self.book:
      return -99999
    tot = 0
    for i in self.book['sell']:
      if i[1] >= a:
        tot += i[0] * a
        a = 0
        break
      tot += i[0] * i[1]
      a -= i[1]
    if a > 0:
      return -99999
    return tot

  def get_buy(self, a = 1):
    if not self.book:
      return -99999
    tot = 0
    for i in self.book['buy']:
      if i[1] >= a:
        tot += i[0] * a
        a = 0
        break
      tot += i[0] * i[1]
      a -= i[1]
    if a > 0:
      return -99999
    return tot

  def sendOrder(self, isBuy, amount, price):
    buy_sell_msg = {
      "type": "add",
      "order_id": random.randint(10000,1000000),
      "symbol": self.symbol,
      "dir": None,
      "price": price,
      "size": amount,
    }
    if isBuy:
      buy_sell_msg['dir'] = "BUY"
      self.connection.send(buy_sell_msg)
    else:
      buy_sell_msg['dir'] = "SELL"
      self.connection.send(buy_sell_msg)
  def convert(self, isBuy, amount):
    #return
    buy_sell_msg = {
      "type": "convert",
      "order_id": random.randint(10000,1000000),
      "symbol": self.symbol,
      "dir": None,
      "size": amount,
    }
    if isBuy:
      buy_sell_msg['dir'] = "BUY"
      self.connection.send(buy_sell_msg)
    else:
      buy_sell_msg['dir'] = "SELL"
      self.connection.send(buy_sell_msg)
