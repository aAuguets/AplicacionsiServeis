# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela
#! /usr/bin/env python

# Client and server for udp (datagram) echo.
#
# Usage: udpecho -s [port]            (to start a server)
# or:    udpecho -c host [port] <file (client)

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
	print 'Usage: udpecho -s [port]            (server)'
	print 'or:    udpecho -c host [port] <file (client)'
	sys.exit(2)

def server():
	if len(sys.argv) > 2:
		port = eval(sys.argv[2])
	else:
		port = ECHO_PORT
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', port))
	print 'udp echo server ready'
	while 1:
		data, addr = s.recvfrom(BUFSIZE)
		if addr not in CLIENTS:
			CLIENTS.append(addr)
		print 'client received from', addr, "->", data
		for i in range(len(CLIENTS)):
			if CLIENTS[i] != addr:
				s.sendto(data, CLIENTS[i])

def client():
	if len(sys.argv) < 3:
		usage()
	host = sys.argv[2]
	if len(sys.argv) > 3:
		port = eval(sys.argv[3])
	else:
		port = ECHO_PORT
	addr = host, port
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 0))
	print 'udp echo client ready, reading stdin'

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
			print addr, "->", txt
        #line = sys.stdin.readline()
        #if not line:
        #    break
        #s.sendto(line, addr)
        #data, addr = s.recvfrom(BUFSIZE)
        #print 'client received from', addr, "->", data

main()
