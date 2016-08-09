#!/usr/bin/python

from socket import socket,timeout
try:
	s = socket()
	host = 'pop.free.fr'
	port = 110
	s.connect((host, port))
	resp = s.recv(1024)
	s.send('USER arnaud.vial\r\n')
        resp=s.recv(1024)
        s.send('PASS md7x518a\r\n')
	resp = s.recv(1024)
	s.send('STAT\r\n')
	resp = s.recv(100)
	nb = resp.split( )
	print nb[1]+" mail(s) dans votre boite "


	s.close()
except timeout:
	print 'timeout'
	s.close()

