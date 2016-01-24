from __future__ import print_function
import socket
import sys
import time
import json
from time import gmtime, strftime
import traceback


import Client

from ValueCalculator import ValueCalculator

import BondHandler
import VALE

def run(server, PORT):
  IP = socket.gethostbyname(server)
  #IP = "1.1.1.1"
  PORT = int(port)
  print(IP, PORT)

  logfile = open("log." + strftime("%H%M%S", gmtime()) + ".txt", "w")

  client = Client.Client(IP, PORT, logfile)

  client.send({"type":"hello", "team": "JANEAVENUE"})

  bh = None
  vh=None
  book = {}

  my_orders = {}
  vc = ValueCalculator()

  t0 = time.time()
  t1 = time.time()

  while True:
    obj = client.read()
    if bh:
      bh.floodMarket()
    if obj['type'] == "book":
      orders = [obj['buy'],obj['sell']]
      symbol = obj['symbol']
      if symbol not in book:
        book[symbol] = []
      book[symbol].append(orders)

      if obj['symbol'] == 'XLF':
      	if process(book, "XLF", client):
	  book['XLF'] = []

      if obj['symbol'] == 'BOND':
        bh.handleBook(book, obj['symbol'])

      if obj['symbol'] == 'VALE' or obj['symbol'] == 'VALBZ':
        vh.getOrderBooks(book)

      vc.feed(obj)

    if obj['type'] == "out":
      process_outs(my_orders, obj['order_id'])
  
    if obj['type'] == 'open':
      if 'BOND' in obj['symbols']:
         bh = BondHandler.BondHandler(client)
      if 'VALE' in obj['symbols'] and 'VALBZ' in obj['symbols']:
        vh= VALE.VALETrader(client)
    if obj['type'] == 'close':
      if 'BOND' in obj['symbols']:
        bh = None
      if 'VALE' in obj['symbols'] or 'VALBZ' in obj['symbols']:
        vh = None
    if obj['type'] == 'fill':
      if bh:
        if obj['symbol'] == 'BOND':
          bh.fillOrder(obj)

    t2 = time.time()
    if t2 - t1 > 5:
      vc.report()
      t1 = t2
    time.sleep(0.02)

counter = 200000
def sendOrder(isBuy, amount, price, symbol, client):
    global counter
    counter+=1
    buy_sell_msg = {
        "type": "add",
        "order_id": counter,
        "symbol": symbol,
        "dir": None,
        "price": price,
        "size": amount,
    }
    if isBuy:
        buy_sell_msg['dir'] = "BUY"
        client.send(buy_sell_msg)
    else:
        buy_sell_msg['dir'] = "SELL"
        client.send(buy_sell_msg)

def process(local_book, symbol, client):
    vale_book = local_book[symbol]
    if len(vale_book) >= 5:
	values = vale_book[-5:-1]

	best_sell = 10000000
	best_buy = 0

	for frame in values:
            for order in frame[0]:
	        if order[0] > best_buy:
			best_buy = order[0]
	
            for order in frame[1]:
	        if order[0] < best_sell:
			best_sell = order[0]

        sendOrder(True, 5, best_buy, symbol, client)
        sendOrder(False, 5, best_sell, symbol, client)
    
        return True


def process_outs(orders, order, client):
    if out in orders:
        del order[out]

    for o in orders:
        order[o] += 1
	if order[o] > 3:
	    #Send cancel
	    client.send({"type": "cancel", "order_id": o})

	    del order[o]


    
        
    
       
	




if __name__ == '__main__':
  server = "test-exch-janeavenue"
  port = 25000  
  if len(sys.argv) > 1:
    server = sys.argv[1]
  if len(sys.argv) > 2:
    port = sys.argv[2]
  print(server) 
  while True:
    try:
      run(server, port)
    except Exception, e:
      traceback.print_exc()
      #print(e.message)
      pass
    time.sleep(1)



