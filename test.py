from __future__ import print_function
import socket
import sys
import time
import json
from time import gmtime, strftime

import Client

def run(server):
  IP = socket.gethostbyname(server)
  #IP = "1.1.1.1"
  print(IP)
  PORT = 25000

  logfile = open("log." + strftime("%H%M%S", gmtime()) + ".txt", "w")

  client = Client.Client(IP, PORT, logfile)

  client.send({"type":"hello", "team": "JANEAVENUE"})

  import BondHandler

  bh = None

  while True:
    obj = client.read()

    if obj['type'] == 'open':
      if 'BOND' in obj['symbols']:
         bh = BondHandler.BondHandler(client)

    if obj['type'] == 'close':
      if 'BOND' in obj['symbols']:
        bh = None

    if obj['type'] == 'fill':
      if bh:
        if obj['symbol'] == 'BOND':
          bh.fillOrder(obj)

    time.sleep(0.011)

if __name__ == '__main__':
  server = "test-exch-janeavenue"
  if len(sys.argv) > 1:
    server = sys.argv[1]
  print(server) 
  while True:
    try:
      run(server)
    except Exception as e:
      print(e) 
      pass
    time.sleep(1)



