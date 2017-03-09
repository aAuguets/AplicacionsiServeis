# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela
import socket, select, sys, signal, struct
HOST=''
PORT=5000
List_conection=[]
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))
server_socket.listen(1)
List_conection.append(server_socket)
print "Chat started"
while 1:
    read_socket,_,_ = select.select(List_conection,[],[])
    print read_socket

    for sock in read_socket:
    	#se ha producido una nueva connecion
    	print sock
    	if sock== server_socket:
    		socket_direc,addr=server_socket.accept()
    		print socket_direc
    		List_conection.append(socket_direc)
    		print "Se ha establecido connecion con:" +str(addr)
    	#si algo viene de un cliente
       	else:
       		try:
       			#recibimos un dato
       			data=socket_direc.recv(1024)
       			print data
       			#aqui debemos enviar el mensaje a donde queramos
       		except:
       			print ("Client"+str(addr)+"is offline")
       			sock.close()
       			List_conection.remove(sock)
       			continue
server_socket.close()

