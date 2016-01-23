from __future__ import print_function
import socket
import sys
import time
import json
from time import gmtime, strftime
import traceback


import Client

from ValueCalculator import ValueCalculator

def run(server, PORT):
  IP = socket.gethostbyname(server)
  #IP = "1.1.1.1"
  PORT = int(port)
  print(IP, PORT)

  logfile = open("log." + strftime("%H%M%S", gmtime()) + ".txt", "w")

  client = Client.Client(IP, PORT, logfile)

  client.send({"type":"hello", "team": "JANEAVENUE"})

  import BondHandler
  import VALE

  bh = None
  vh=None
  book = {}

  vc = ValueCalculator()

  t0 = time.time()
  t1 = time.time()

  while True:
    obj = client.read()
    if bh:
      bh.floodMarket()

    if obj['type'] == "book":
      orders = [obj['buy'],obj['sell'] ]
      symbol = obj['symbol']
      if symbol not in book:
        book[symbol] = []
      book[symbol].append(orders)
      try:
          bh.handleBook(book, obj['symbol'])

          vc.feed(obj)
      except Exception as e:
	  traceback.print_exc()

    if obj['type'] == 'open':
      if 'BOND' in obj['symbols']:
         bh = BondHandler.BondHandler(client)
      if 'VALE' in obj['symbols'] and 'VALBZ' in obj['symbols']:
        vh= VALE.VALETrader(client)


    if obj['type'] == 'close':
      if 'BOND' in obj['symbols']:
        bh = None
      if 'VALE' in obj['symbols'] and 'VALBZ' in obj['symbols']:
        vh = None

    if obj['type'] == 'fill':
      if bh:
        if obj['symbol'] == 'BOND':
          bh.fillOrder(obj)
    vh.getOrderBooks(book)


    t2 = time.time()
    if t2 - t1 > 5:
      vc.report()
      t1 = t2

    time.sleep(0.011)

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
    except Exception as e:
      print(e) 
      pass
    time.sleep(1)



