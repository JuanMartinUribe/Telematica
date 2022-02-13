import socket
import sys, getopt
import email
import pprint
from io import StringIO

'''YACURL JUAN MARTIN URIBE, TOPICOS ESPECIALES EN TELEMATICA LABORATORIO1
Se reciben dos argumentos -h host -p port y uno opcional para guardar archivos:

ejemplo de como correr el programa:
python .\yacurl.py -h http://3.217.183.77 -p 80

o para guardar archivo en el directorio actual
python .\yacurl.py -h http://3.217.183.77 -p 80 index.html

'''

def main(argv):

   try:
      opts, args = getopt.getopt(argv,"Hh:p:",["host=","port="])
      print(opts,args)
      host = 80
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
    #Encabezados comunes
    path = ""
    userAgent = "yacurl/1.0"
    accept = "Accept: */*"
    if host[:4] == "http": host = host[7:]

    try:
       path = host[host.index('/'):]
       host = host[:host.index('/')]
       
    except ValueError:
       path = "/"
    print(host,path,port)

    #Conexion mediante socket  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    s.connect((socket.gethostbyname(host),port))

    
    #Construccion del paquete GET
    request_string = 'GET %s HTTP/1.0\r\nHost: %s \r\nUser-Agent: %s \r\nAccept: %s \r\n\r\n' %(path,host,userAgent,accept)
    print(request_string)
    
    #Print de los headers comunes y el paquete get creado
    _, headers = request_string.split('\r\n', 1)
    message = email.message_from_file(StringIO(headers))
    headers = dict(message.items())
    pprint.pprint(headers, width=160)
   
    #Envio de informacion
    s.sendall(bytes(request_string,encoding='utf-8'))
    
    #Recepcion del htpp response y decodificacion dependiendo de si es un arhivo de texto,html, etc o una imagen o gif
    #a veces no se representa el html completo, hay que correr el programa un par de veces para que funcione

    if len(sys.argv)<6:
      try:
         data = s.recv(4096).decode('utf-8')
         print(data)
      except:
         print("data could not be decoded, try output")
    else:
       if 'gif' in sys.argv[5] or 'image' in sys.argv[5]:
          data = s.recv(4096)
          localFile = sys.argv[5]
          file = open(localFile,'w')
          file.write(repr(data))
          file.close()
       else:
          data = s.recv(4096).decode('utf-8')
          localFile = sys.argv[5]
          file = open(localFile,'w')
          file.write(data)
          file.close()
      
if __name__ == "__main__":
    host,port = main(sys.argv[1:])
    client(host,port)