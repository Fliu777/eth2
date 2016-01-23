from __future__ import print_function
import socket
import sys
import time

IP = socket.gethostbyname('test-exch-janeavenue')
#IP = socket.gethostbyname('production')
#IP = "1.1.1.1"
PORT = 20000
TEAMNAME = 'JANEAVANUE'

class Client:
  BUFFER_SIZE = 1024
  
  def __init__(self, ip, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((ip, port))
    self.file = self.socket.makefile('w+', 1)

  def send(self, message):
    print(message)
    print(message, file=self.file)

  def close(self):
    self.socket.close()

  def read(self):
    data = self.file.readline().strip() 
    print(data)

client = Client(IP, PORT)

client.send("HELLO JANEAVENUE\n")

import BondHandler

bh = BondHandler.BondHandler(client)

while True:
  data = client.read()

  bh.updatePrice(None)

  time.sleep(0.1)

