# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela
#! /usr/bin/env python

import sys, select
from socket import *

ECHO_PORT = 5000
BUFSIZE = 1024
CLIENTS = []

def main():
	if len(sys.argv) < 2:
		usage()
	if sys.argv[1] == '-s':
		server()
	elif sys.argv[1] == '-c':
		client()
	else:
		usage()

def usage():
	sys.stdout = sys.stderr
	print 'Usage: udpecho -s [port]   	(server)'
	print 'or:    udpecho -c [IP] 		(client)'
	sys.exit(2)

def server():
	if len(sys.argv) > 2:
		port = eval(sys.argv[2])
	else:
		port = ECHO_PORT
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', port))
	print 'Server Preparat.'
	while 1:
		data, addr = s.recvfrom(BUFSIZE)
		if addr not in CLIENTS:
			CLIENTS.append(addr)
		print 'Client received from', addr, "->", data
		for i in range(len(CLIENTS)):
			if CLIENTS[i] != addr:
				s.sendto(str(addr)+':'+data, CLIENTS[i])

def client():
	if len(sys.argv) < 3:
		usage()
	host = sys.argv[2]
	
	port = ECHO_PORT
	addr = host, port
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	print 'Client preparat.'

	while 1:
		read, _, _ = select.select([sys.stdin, s], [], [])
		if read[0] == sys.stdin:
			txt = sys.stdin.readline()
			if ("Help" in txt) or ("help" in txt):
				print "Clients-> ",t, "\nEscriure un msg de la forma-> Client:Missatge \nPavel Adria."
			
			else:
				s.sendto(txt, addr)
		elif read[0] == s:
			txt, addr = s.recvfrom(BUFSIZE)
			i=0
			for e in txt:
				if e == ':':
					break
				i+=1
			print txt[:i], "->", txt[i+1:]
        
main()
