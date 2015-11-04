import socket  
import sys  	
import time
import math 
import datetime
import select
import thread
# GLOBAL VARIABLES 
host = 'localhost'
port = 8000 
flag = 0								#flag to check if data is received from server in the thread
delay = 0
delayArr = []
MAXRTT = None
MINRTT = None
receivedPackets = 0
missedPackets = 0
totalTime = 0
average = 0
mdev = 0
#


def printDetails():					   # FUNCTION TO PRINT ALL THE STATISTICS FOR THE PING PROTOCOL IN THE END.

    print "----- ping ",host,"statistics-----------"
    global MAXRTT
    global MINRTT
    global delay
    global totalTime
    global receivedPackets
    global missedPackets
    global average
    global mdev
    total = receivedPackets + missedPackets
    print "Missed packets:", missedPackets
    lossRate = float(missedPackets)/10
    if not MAXRTT is None:
        MAXRTT *= 1000
        MINRTT *= 1000
        x = 0
        for i in range(len(delayArr)):
            x = x+(delayArr[i]*1000)
 
        average = x/len(delayArr)				#sum/no of recieved packets
        mdev = 0.0

        for i in range(len(delayArr)):
            mdev += math.pow(((delayArr[i]*1000)-average),2)
        mdev=math.sqrt(mdev/len(delayArr))					#standard deviation
    if(MAXRTT is None):
    	MAXRTT = 0
    if(MINRTT is None):
    	MINRTT = 0
  	print "10 packets transmitted, %s received, %.1f%% packet loss"%(receivedPackets, lossRate*100)
    print "rtt min/avg/max/mdev = %.4f/%.4f/%.4f/%.4f ms"%(MINRTT, average,MAXRTT,mdev) 

def pingOnce(host, timeout):						# function that opens a socket and send data to clinet and calculates the delay if the server ping back some data
	global flag
	global delay
	starttime=""
	starttime+= str(datetime.datetime.now())[17:]
	msg = "Hello Server"
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		clientsocket.sendto(msg,(host,port))
	except socket.error, (errornumber, msg):
		if errornumber == 1:
			msg = msg + "Process needs to be run as root "
		raise socket.error(msg)
	try:
		receivedPacket,addr = clientsocket.recvfrom(1024)
		timeRecieved=float(str(datetime.datetime.now())[17:])
		timeSent=float(starttime)
		flag = 1
		if timeRecieved - timeSent>=1:
			delay =  1000
		else:
			delay =  timeRecieved-timeSent
	except:
		clientsocket.close()

def ping(host, timeout):			# ping implementation. pings the server 10 times in a second's interval.
    global MAXRTT
    global MINRTT
    global totalTime
    global receivedPackets
    global missedPackets
    global delayArr
    global begintime
    global flag
    global delay
    totalPackets=0

    while totalPackets!=10:
    	flag = 0
        totalPackets += 1
        try:
        	thread.start_new_thread( pingOnce, (host,timeout,))
        except:
        	print "Error: unable to start thread"
        time.sleep(1)								#stop execution for a second
        if(flag == 0):								#if there was no reply from server int the last second then timeout
        	print "REQUEST TIMED OUT"
        	delay = 2
        if(delay*1000<=timeout):					#if there was reply from the server and it was in time < 1s store the delay.
            print "64 bytes from %s: id_seq=%d ttl=%d time=%.5fms"%(host,totalPackets, 64, delay*1000)
            delayArr.append(delay)
        if (delay*1000 >= timeout) or (flag == 0): #check whether packet is missed or not
            missedPackets = missedPackets+1
        else:
            if MAXRTT is None or delay > MAXRTT:	#updating max or min delay
                MAXRTT = delay
            if MINRTT is None or delay < MINRTT:	
                MINRTT = delay
            totalTime += delay
            receivedPackets =receivedPackets+1		#updating 
    printDetails()
beginTime=time.time()
ping(host,1)
endTime=time.time()


