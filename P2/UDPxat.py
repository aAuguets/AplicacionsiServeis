# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela

import socket, select, sys, signal, struct

S_HOST = ''
C_HOST = '10.60.128.147'#UPCeduroam'10.192.107.42'#Local'127.0.0.1' #adreça de la maquina que controlara els msg que li arriben.
PORT = 5000 
t = [5000]


def s_exit(signal, frame):
	s.close()
	sys.exit(0)

def _select(data, port):
	read, _, _ = select.select(data, [], [])
	if read[0] == data[0]:
		txt = sys.stdin.readline()
		if len(port)==1:
			data[1].sendto(txt, (C_HOST, int(port[0])))
		else:
			client = input("client?: ")
			data[1].sendto(txt, (C_HOST, int(port[client])))
	elif read[0] == data[1]:
		txt, addr = data[1].recvfrom(1024)
		print addr, "->", txt
		return addr[1]


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	if sys.argv[1]=='0':
		s.bind((S_HOST, PORT))
		signal.signal(signal.SIGINT, s_exit)
		print "S"

	p=_select([sys.stdin, s],t)
	while 1:
		p=_select([sys.stdin, s],t)
		if (p not in t) and p != None:
			t.append(p)



main()
