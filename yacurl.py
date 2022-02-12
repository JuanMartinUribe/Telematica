import socket
import sys, getopt
import requests
import email
import pprint
from io import StringIO
from urllib.parse import urlparse


def main(argv):

   try:
      opts, args = getopt.getopt(argv,"Hh:p:",["host=","port="])
      print(opts,args)
   except getopt.GetoptError:
      print ('yacurl.py -h <host> -p <port>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-H':
         print ('yacurl.py -h <host> -p <port>')
         sys.exit()
      elif opt in ("-h", "--host"):
         host = str(arg)
      elif opt in ("-p", "--port"):
         port = int(arg)
   return host,port

def client(host,port):
    
    if host[:4] == "http": host = host[7:]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   
    s.connect((socket.gethostbyname(host),port))
    
    request_string = 'GET / HTTP/1.0\r\nHost: ec2-3-217-183-77.compute-1.amazonaws.com\r\n\r\n'
    
    
    print(socket.gethostbyname(host))
    

    _, headers = request_string.split('\r\n', 1)
   
    prueba = urlparse(socket.gethostbyname(host))
    print(prueba)
    # construct a message from the request string
    message = email.message_from_file(StringIO(headers))

    # construct a dictionary containing the headers
    headers = dict(message.items())

    # pretty-print the dictionary of headers
    pprint.pprint(headers, width=160)
      
    s.sendall(b'GET / HTTP/1.0\r\nHost: 3.217.183.77 \r\n\r\n')

    data = s.recv(1024)
    print('Received', repr(data))

if __name__ == "__main__":
    host,port = main(sys.argv[1:])
    client(host,port)