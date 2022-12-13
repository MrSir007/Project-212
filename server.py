import socket
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import time
import os

SERVER = None
ip_address = "127.0.0.1"
port = 1050
buffer_size = 4096
clients = {}

is_dir_exists = os.path.isdir('shared_files')
print(is_dir_exists)
if(not is_dir_exists):
    os.makedirs('shared_files')

def acceptConnections () :
  global SERVER
  global clients

  while True :
    client, addr = SERVER.accept()
    client_name = client.recv(4096).decode().lower()
    clients[client_name]  = {
      "client": client,
      "address": addr,
      "connected_with": "",
      "file_name": "",
      "file_size": 4096
    }

    print(f"Connection established with {client_name} : {addr}")

    thread = Thread(target=handleClient, args=(client, client_name))
    thread.start()

def handleClient(client, client_name):
  global clients
  global SERVER

  banner = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
  client.send(banner.encode())

def ftp () :
  global ip_address

  authorizer = DummyAuthorizer()
  authorizer.add_user("lftpd", "lftpd", ".", perm="elradfmr")
  handler = FTPHandler
  handler.authorizer = authorizer
  ftp_server = FTPServer((ip_address, 21), handler)
  ftp_server.serve_forever()    

def setup () :
  print("\n\t\t\t\t\tIP Messager\n")

  global SERVER
  global ip_address
  global port

  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.bind((ip_address, port))

  SERVER.listen(100)

  print("\t\t\t\tServer is waiting for incoming connection...")
  print("\n")

  acceptConnections()

setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp)
ftp_thread.start()