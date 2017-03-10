# -*- coding: utf-8 -*-

# Xat usant UDP
# Adria Auguets i Pavel Macutela

import socket, sys, select, struct, signal
port = 5000
host = '10.192.107.42'

List = []
s = None 

def signal_handlerClient(signal, frame):
    global s
    print '  Ctrl+c : Desconectant...'
    s.close()
    sys.exit(0)
    
def signal_handlerServer(signal, frame):
    global List
    print 'Desconectant desde el Servidor'
    socket.close()

    sys.exit(0)


def selectClient(data, user):
    read, _ , _ = select.select(data, [], [])
    if read[0] == data[0]:
        txt = sys.stdin.readline()
        data[1].send(user+':'+txt)
    elif read[0] == data[1]:
        txt = data[1].recv(1024)
        if '.exit' in txt:
            data[1].close()
            sys.exit(0)
        c=0
        for i in txt:
        	if i == ':':
        		break
        	else:
        		c+=1
        print "Received from", txt[0:c],"->", txt[c+1:]
        
def selectServer(data):
    global List
    read, _ , _ = select.select(data, [], [])
    if read[0] == data[0]:
        sk, addr = data[0].accept()
        if sk not in List:
        	List += [sk]
        	print "Conexio realitzada amb :", addr, "correctament."
    else:
        for element in range(len(read)):
            txt = read[element].recv(1024)
            if txt == '.exit':
                print "Client Desconectat."
                read[element].close()
                List.remove(read[element])
            for e in range(1, len(data)):
                if read[element] != data[e]: #reenviem a tots si no son el que ha enviat el msg
                    data[e].send(txt)
            

def setupServer(port, host):
    global List
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    List += [s]

def setupClient(port, host):
    global s
    global List
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    List += [s]


if (sys.argv[1] == 'c'):
    signal.signal(signal.SIGINT, signal_handlerClient)
    List = [sys.stdin]
    setupClient(port, host)
    while(True):
        selectClient(List, sys.argv[2])
elif (sys.argv[1] == 's'):
    signal.signal(signal.SIGINT, signal_handlerServer)

    List = []
    setupServer(port, host)
    while(True):
        selectServer(List)
else:
    print "Error, introdueix: $ python TCPxat.py s / c nomUsuari(nomes en client)"