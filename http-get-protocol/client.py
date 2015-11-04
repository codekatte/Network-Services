import socket  
import sys  	
import time
import math 
import datetime
import select
import thread

def removeheader(data):														#FUNCTION TO REMOVE EXTRA HTTP HEADER INFORMATION FROM THE DOWNLOADED HTML FILE
	length = len(data)
	i=0
	count = 0
	while i<length:
		if(data[i]=='\r' and data[i+1]=='\n' and data[i+2]=='\r' and data[i+3]=='\n'):
			count += 1
			if count == 1:
				i = i+3
				break
		i+=1
	newdata = ""
	while i<length:
		newdata+=data[i]
		i+=1
	return newdata

def downloadfiles(filelist,HOST,PORT,BUFFER_SIZE,path):						#FUNCTION TO DOWNLOAD THE files in the filelist. i.e. the .html links on the page
	count = 0
	countmax = 6
	for link in filelist:
		count+=1
		if(count == countmax):
			break
		print "Downloading file ......",link
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		MESSAGE=""
		MESSAGE+="GET /"+str(link)+" HTTP/1.1\r\n"
		MESSAGE+= "Host: "+str(HOST)+":"+str(PORT)+"\r\n\r\n"
		s.send(MESSAGE)
		data=""
		data1 = ""
		while True:
			data1= s.recv(BUFFER_SIZE)
			if not data1:
				break
			data+=data1
		print data
		link1=""
		link1+=path
		link1+=link
		file = open(str(link1),'a')
		data = removeheader(data)
		file.write(data);
		file.close()

def extactfiles(data):												# from the page that user asked for we are extracting the .html files
	length = len(data)
	i=0
	atags = []
	allfiles = []
	while i<length:
		temp = ""
		if(data[i] == '<' and data[i+1] == 'a'):
			j = i
			while data[j]!='>' and j<length:
				temp+=data[j]
				j+=1
			if len(temp) !=0 :
				atags.append(str(temp))
			i = j
		i+=1
									
	for x in atags:												#atag are the entire <a></a> tags
		length = len(x)
		i=0
		while i<length:
			if x[i] == 'h' and x[i+1] == 'r' and x[i+2] == 'e' and x[i+3] == 'f':
				j = i+4
				while x[j] == ' ' and j<length:
					j+=1
				if x[j] == '=':
					k = j+1
					link = ""
					while x[k] == ' ':
						k+=1
					k+=1
					while x[k]!='"' and k<length:
						link+=x[k]
						k+=1
					j = k
					if len(link)!=0:
						if(link[-5:len(link)] == ".html"):
							allfiles.append(link)
					i = j
			i+=1
	return allfiles 										# allfiles contains the names of all .html files to be downloaded
    
HOST = "127.0.0.1"
PORT = 5050
path="/home/supahacka/Desktop/Assignments/CN/asn2/" #appropiate path here
data=""
BUFFER_SIZE = 1024
sys_len = len(sys.argv)
if sys_len>=3:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	path = sys.argv[3]
	BUFFER_SIZE = 500
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print "(HOST,PORT): ",HOST,PORT
	MESSAGE = "GET "+path+" HTTP/1.1\r\n"
	MESSAGE+= "Host: "+str(HOST)+":"+str(PORT)+"\r\n\r\n" 
	s.send(MESSAGE)
	data1 = ""
	while True:
		data1= s.recv(BUFFER_SIZE)
		if not data1:
			break
		data+=data1
	error_header = "HTTP/1.1 404 Not Found\r\n\r\n<body><h1>404 Not Found</h1></body>"
	if error_header in data:
		print "HTTP/1.1 404 Not Found"
	else:
		allfiles= []
		allfiles_new= []
		allfiles = extactfiles(data)
		for x in allfiles:
			link = ""
			for j in range(0,len(x)):
				if(x[j] != ' '):
					link+=x[j]
				link = str(link)
			allfiles_new.append(link)
		downloadfiles(allfiles_new,HOST,PORT,BUFFER_SIZE,"")
		s.close()
if(sys_len == 1):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(("localhost", PORT))
	except socket.error, exc:
	    print "Caught exception socket.error : %s" % exc
	MESSAGE = "GET /index.html HTTP/1.1\r\n"
	MESSAGE+= "Host: "+str("localhost")+":"+str(PORT)+"\r\n\r\n"
	s.send(MESSAGE)
	data1 = ""
	while True:
		data1= s.recv(BUFFER_SIZE)
		if not data1:
			break
		data+=data1

	error_header = "HTTP/1.1 404 Not Found\r\n\r\n<body><h1>404 Not Found</h1></body>"
	if error_header in data:
		print "HTTP/1.1 404 Not Found"
	else:
		allfiles= []
		allfiles_new= []
		allfiles = extactfiles(data)
		for x in allfiles:
			link = ""
			for j in range(0,len(x)):
				if(x[j] != ' '):
					link+=x[j]
				link = str(link)
			allfiles_new.append(link)
		downloadfiles(allfiles_new,"localhost",PORT,BUFFER_SIZE,path)	
	s.close()
