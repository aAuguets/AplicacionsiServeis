# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela

import socket, select, sys, signal, struct

S_HOST = ''
C_HOST = '192.168.2.3' #adreça de la maquina que controlara els msg que li arriben.
PORT = 5000 



def s_exit(signal, frame):
	s.close()
	sys.exit(0)

def _select(data):
	read, _, _ = select.select(data, [], [])
	if read[0] == data[0]:
		txt = sys.stdin.readline()
		data[1].sendto(txt, (C_HOST, PORT))
	elif read[0] == data[1]:
		txt, addr = data[1].recvfrom(1024)
		print addr, "->", txt


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((S_HOST, PORT))
	signal.signal(signal.SIGINT, s_exit)

	while 1:
		_select([sys.stdin, s])

main()