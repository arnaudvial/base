#!/usr/bin/python

import MySQLdb
import socket
import threading


UDP_IP = "127.0.0.1"
UDP_PORT = 5005


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    print "address : ",addr[0]

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="md7x518c",  # your password
                     db="sigfoxdb")        # name of the data base


    cur = db.cursor()

    cur.execute(" select count(*) from ipinfo where mac like '"+data+"'")
    c = cur.fetchone()[0]
    if (c==0):
        cur.execute(" insert into ipinfo (ip,mac) values ('"+addr[0]+"','"+data+"')")
    
    if(c==1):
        cur.execute(" update ipinfo set ip = '"+addr[0]+"' where mac like '"+data+"' ")


    db.commit();
    db.close()





