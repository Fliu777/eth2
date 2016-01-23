import socket 
import sys 
import timer
from __future__ import print_function

IP = socket.gethostbyname('test-exch-janeavenue')
#IP = socket.gethostbyname('production')
PORT = 20000
TEAMNAME = 'JANEAVANUE'

class Client:
  BUFFER_SIZE = 1024
  
  def __init__(self, ip, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((ip, port))
    self.file = self.socket.makefile('w+', 1)

  def send(self, message):
    print(message, file=self.file)

  def close(self):
    self.socket.close()

  def read(self):
    return self.file.readline().strip()


client = Client(IP, PORT)

client.send("HELLO JANEAVANUE")

import BondHandler

bh = BondHandler.BondHandler(client)

while True:
  data = client.read()

  bh.updatePrice(None)

  timer.sleep(0.1)

