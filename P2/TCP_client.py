# Client en TCP

import socket, select, sys, signal, struct
HOST='127.0.0.1'
PORT=5000


socket_client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	socket_client.connect((HOST,PORT))
except:
	print "Unable to connect"
	sys.exit()

print "Conectado al servidor remoto, comienza el chat."
while 1:
	read_socket, _,_= select.select([sys.stdin ,socket_client],[],[])	
		if read_socket[0] == socket_client[0]:
			data=socket.recv(1024)
			print "data=", str(data)
			if not data:
				print "se ha desconectado del servidor"
				sys.exit()
				sys.stdout.write(data)
			else:
				msg=sys.stdin.readline()
				socket_client.send(msg)

