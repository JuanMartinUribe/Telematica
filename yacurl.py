import socket
import sys, getopt

def main(argv):

   try:
      opts, args = getopt.getopt(argv,"Hh:p:",["host=","port="])
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
    #host de prueba 'www.py4inf.com'
    #puerto 80
    #http request get b'GET /code/romeo.txt HTTP/1.0\r\nHost: www.py4inf.com\r\n\r\n'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostbyname(host),port))

    s.sendall(b'GET /code/romeo.txt HTTP/1.0\r\nHost: www.py4inf.com\r\n\r\n')

    data = s.recv(1024)
    print('Received', repr(data))

if __name__ == "__main__":
    host,port = main(sys.argv[1:])
    client(host,port)