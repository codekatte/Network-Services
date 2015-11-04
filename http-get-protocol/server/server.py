import socket
import sys
def FileCheck(fn):															#TO CHECK IF A FILE CAN BE OPENED
    try:
      open(fn, "r")
      return 1
    except IOError:
      return 0
class HTTP_REQUEST:															# HTTP_REQUEST CLASS
	name=[]
	name_string = ""
	def __init__(self,request):												# PARSES THE REQUEST TO GET THE FILE NAME THAT NEEDS TO SENT BY SERVER
		self.name=[]
		self.name_string = ""
		request_size = len(request)
		for i in range(0,request_size):
			if  request[i] == '/':
				j = i
				while request[j]!=' ':
					self.name.append(request[j])
					j+=1	
				break
		self.name_string = ''.join(self.name)
	
class HTTP_RESPONSE:														# HTTP_RESPONSE CLASS
	request = HTTP_REQUEST("");
	path = "/home/supahacka/Desktop/Assignments/CN/asn2/server"
	file_name=""
	header=""
	def __init__(self, req):												# SEND THE APPROPIATE HTTP REQUEST TO THE CLIENT
		self.file_name=""
		self.header=""
		request = req
		file_name = self.path+req.name_string
		result = FileCheck(file_name)
		if result == 1:
			utf8_text=open(file_name,'r+').read()
			unicode_data = utf8_text.decode('utf8')
			flen =  len(unicode_data)
			self.header = "HTTP/1.1 200 \r\n";
			self.header += "Content-Type: text/html\r\n";
			self.header += "Connection: close \r\n";
			self.header += "Content length: " + str(flen) + "\r\n\r\n";
			with open(file_name) as f:
			  while True:
			    c = f.read(1)
			    if not c:
			      #print "End of file"
			      break
			    self.header+=c
			print "Sending File: ",file_name
			f.close()
		elif result == 0:
			self.header = "HTTP/1.1 404 Not Found\r\n\r\n<body><h1>404 Not Found</h1></body>"
		else:
			self.header = "HTTP/1.1 500 Internal Server Error\r\n\r\n<body><h1>404 Not Found</h1></body>"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)				#CREATING A NEW HTTP SOCKET
PORT = 5000
HOST = "localhost"
server_address = (HOST, PORT)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)
while 1:
    print 'waiting for a connection'
    connection, client_address = sock.accept()
    print 'connection from', client_address
    data = connection.recv(1024)
    if data:
        req = HTTP_REQUEST(data)
        res = HTTP_RESPONSE(req)
        connection.send(res.header)
    else:
        print 'no more data from', client_address
        break
        
    connection.close()
