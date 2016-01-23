import socket 
import sys 
import timer

#IP = socket.gethostbyname('test-exch-janeavenue')
IP = socket.gethostbyname('production')
PORT = 25000

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

  def update(self):
    while self.file.readline().strip():



s = Client(IP, PORT)

print(s.send("hello\n"))

s.close()


if __name__ == '__main__':

  c = Client()


  while True:
    c.update()

    timer.sleep(0.05)



