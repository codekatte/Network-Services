import socket   #for sockets
import sys  #for exit
import time
import math 
import datetime
import random
AVERAGE_DELAY = 0.00004
def Message(addr,port):  					#	CREATE THE MESSAGE TO BE SEND ENCODING THE MESSAGE FROM THE CLIENT,DATE,PLATFORM..ETC
    mssg=''
    mssg += "UDP"
    str_addr = str(addr)
    time.sleep(AVERAGE_DELAY)
    serverDelay = str(datetime.datetime.now());
    mssg = mssg + "0"*(16-len(str(addr))) + str(addr) + "0"*(4-len(str(port))) + str(port) + serverDelay + str(sys.platform) + "Server Created"
    return mssg

PORT = 8000
HOST = 'localhost'
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# CREATE AND OPEN UDP SOCKET
	print 'Socket created successfully!'
except socket.error, mssg :
	print 'Failed to create socket. Error code: ' + str(mssg[0]) + ' Message ' + mssg[1]
try:
	s.bind((HOST,PORT))										# BIND THE SOCKET TO (HOST,PORT)
	print 'BIND COMPLETED'
except socket.error,mssg:
	print 'Bind failed. Error Code : ' + str(mssg[0]) + ' Message ' + mssg[1]


noOfpacketstobemissed = random.randint(1,10);				# RANDOMLY CHOOSE NUMBER OF PACKETS TO BE DROPPED.
print "Number of packets to be missed: ", noOfpacketstobemissed
print "And the packet indices are: "
missedPacketsIndexes = []
while len(missedPacketsIndexes)<noOfpacketstobemissed:		# RANDOMLY CHOOSE THE INDEXES OF THE DROPPED PACKETS
	temp = random.randint(1,10)
	if temp not in missedPacketsIndexes:
		print temp
		missedPacketsIndexes.append(temp)

counter = 0
while 1:													#LISTEN INDEFITELY ON THE SOCKET 's'.
	counter =counter + 1
	if(counter >10):
		break
	print "\nPing: ", counter
	data, addr = s.recvfrom(1024)
	print 'Data recieved from Client->', addr, ' is : ',data
	if (counter not in missedPacketsIndexes):
		mssg=Message(addr, PORT)
		s.sendto(mssg,addr)
		print 'Data sent to Client->', addr, ' is : ', mssg
s.close()
