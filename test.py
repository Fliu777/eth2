from __future__ import print_function
import socket
import sys
import time
from time import gmtime, strftime

import Client

def run(server):
  IP = socket.gethostbyname(server)
  #IP = "1.1.1.1"
  print(IP)
  PORT = 25000

  logfile = open("log." + strftime("%H%M%S", gmtime()) + ".txt", "w")

  client = Client(IP, PORT)

  client.send("HELLO JANEAVENUE\n")

  import BondHandler

  bh = BondHandler.BondHandler(client)

  while True:
    obj = client.read()

    bh.updatePrice(None)

    time.sleep(0.1)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    server = sys.argv[1]
  else:
    server = "test-exch-janeavenue"
 
  while True;
    try:
      run(server)
    except: 
      pass
    time.sleep(1)



