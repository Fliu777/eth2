import socket 

IP = socket.gethostbyname('zihao.me')
#IP = '127.0.0.1'
PORT = 3000

class Socket:
  BUFFER_SIZE = 1024
  
  def __init__(self, ip, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((ip, port))

  def send(self, message):
    self.socket.send(message)
    data = self.socket.recv(Socket.BUFFER_SIZE)
    return data

  def close(self):
    self.socket.close()

s = Socket(IP, PORT)

print(s.send("hello\n"))

s.close()

