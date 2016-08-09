#!/usr/bin/env python

import socket, threading
import MySQLdb


class ClientThread(threading.Thread):

    def __init__(self,data, addr):
        threading.Thread.__init__(self)
	print data
	zz =data.split("#")
	self.hash=zz[1]
        self.data = zz[0]
        self.addr = addr
        print "[+] New thread started for "+self.addr[0]


    def run(self):    
        print "received message:", self.data
        print "address : ",self.addr[0]
    
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="md7x518c",  # your password
                         db="sigfoxdb")        # name of the data base
        
        
        cur = db.cursor()
        cur.execute(" select count(*) from ipinfo where mac like '"+self.data+"'")
        c = cur.fetchone()[0]
        if (c==0):
            cur.execute(" insert into ipinfo (ip,mac,cle,date) values ('"+self.addr[0]+"','"+self.data+"','"+self.hash+"',NOW())")
                         
        if(c==1):
            cur.execute(" update ipinfo set ip = '"+self.addr[0]+"',cle='"+self.hash+"',date=NOW() where mac like '"+self.data+"' ")
    
    
        db.commit();
        db.close()

UDP_IP = ""
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

threads = []

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if data.find("#") != -1 :
    	newthread = ClientThread(data, addr)
    	newthread.start()

