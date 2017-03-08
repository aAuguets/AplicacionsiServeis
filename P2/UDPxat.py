# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela

import socket, select, sys, signal, struct

S_HOST = ''
C_HOST = '10.60.128.147'#UPCeduroam'10.192.107.42'#Local'127.0.0.1' #adreça de la maquina que controlara els msg que li arriben.
PORT = 5000 
t = [5000]
n='1234567890'


def s_exit(signal, frame):
	s.close()
	sys.exit(0)

def _select(data, port):
	read, _, _ = select.select(data, [], [])
	if read[0] == data[0]:
		txt = sys.stdin.readline()
		if ("Help" in txt) or ("help" in txt):
			print "Clients-> ",t, "\nEscriure un msg de la forma-> Client:Missatge \nPavel Adria."
		elif len(port)==1:
			data[1].sendto(txt, (C_HOST, int(port[0])))
		else:
			if txt[0] in n:
				data[1].sendto(txt[2:], (C_HOST, int(port[int(txt[0])])))
			else:
				print "Format d'enviament es CLIENT:MSG"
	elif read[0] == data[1]:
		txt, addr = data[1].recvfrom(1024)
		print addr, "->", txt
		return addr[1]


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	signal.signal(signal.SIGINT, s_exit)
	if sys.argv[1]=='0':
		s.bind((S_HOST, PORT))
		
		print "S"

	while 1:
		p=_select([sys.stdin, s],t)
		if (p not in t) and p != None:
			t.append(p)



main()
