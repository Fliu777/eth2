from __future__ import print_function
import socket
import sys
import time
from time import gmtime, strftime
import json

class Client:
  BUFFER_SIZE = 1024
  
  def __init__(self, ip, port, logf=None):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((ip, port))
    self.file = self.socket.makefile('w+', 1)
    self.logf = logf

  def send(self, obj):
    data = json.dumps(obj)
    print(data, file=self.file)
    #print(data)
    return data

  def close(self):
    self.socket.close()

  def read(self):
    data = self.file.readline().strip() 
    if self.logf: self.logf.write(time.now() + "\t" + data + '\n')
    #print(data)
    return json.loads(data)
