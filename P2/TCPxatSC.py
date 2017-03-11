# -*- coding: utf-8 -*-

# Xat usant TCP
# Adria Auguets i Pavel Macutela

import socket, sys, select, struct, signal
port = 5000         #per defecte.
host = '127.0.0.1'  #per defecte.    #'10.192.225.4'#'10.192.33.172'#'10.192.107.42'
dClients = {}
info_clients={}
List = []
s = None 
nclients = 0
def signal_handlerClient(signal, frame):
    global s
    print '  Ctrl+c : Desconectant...'
    s.close()
    sys.exit(0)
    
def signal_handlerServer(signal, frame):
    global List
    print 'Desconectant desde el Servidor'
    for socket in List:
        socket.close()

    sys.exit(0)

def posicio_dClients(dC, read):
    for i in dC.keys():
        if dC[i] == read:
            return i


def selectClient(data):
    read, _ , _ = select.select(data, [], [])
    if read[0] == data[0]: #teclat
        txt = sys.stdin.readline()
        data[1].send(txt)
    elif read[0] == data[1]: #msg in
        txt = data[1].recv(1024)
        if txt == '':
            print "Servidor Desconectat."
            data[1].close()
            sys.exit(0)
        print "Received from Server ->", txt
        
def selectServer(data):
    global dClients
    global List
    global nclients
    read, _ , _ = select.select(data+dClients.values(), [], [])
    if read[0] == data[1]: #nou client
        socketc, addr = data[1].accept()
        dClients["Client"+str(nclients)]=socketc
        info_clients["Client"+str(nclients)]=addr
        print "NOVA Conexio realitzada...\nUsuari IP:", addr[0], "\nPORT:     ", addr[1],"\nAssignat com a Client", nclients, "\n"
        nclients +=1
    
    elif read[0] == data[0]: #teclat
        msg = sys.stdin.readline()
        if ".CLIENTS" in msg:
            for c in info_clients.keys():
                print c, "\n-------\nIP:  ", info_clients[c][0], "\nPORT:", info_clients[c][1], "\n=====================\n"
        else:
            toClient = msg.split(':')
            if len(toClient)==1:
                print "Err: Format-> ClientNUM:MSG"
            else:
                if toClient[0] in dClients.keys():
                    dClients[toClient[0]].send(toClient[1])
                else:
                    print "Client Desconegut."
    else: #msg in
        for element in range(len(read)):
            txt = read[element].recv(1024)
            nom_client = posicio_dClients(dClients, read[element])
            if txt == '':
                print nom_client, "Desconectat."
                del dClients[nom_client]
                del info_clients[nom_client]
                read[element].close()
            else:
                print "Client", nom_client, ":", txt
            

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


if (sys.argv[1] == '-c'):
    host = sys.argv[2]
    port = int(sys.argv[3])
    signal.signal(signal.SIGINT, signal_handlerClient)
    List = [sys.stdin]
    setupClient(port, host)
    while(True):
        selectClient(List)
elif (sys.argv[1] == '-s'):
    host = sys.argv[2]
    port = int(sys.argv[3])
    signal.signal(signal.SIGINT, signal_handlerServer)
    List += [sys.stdin]
    setupServer(port, host)
    while(True):
        selectServer(List)
else:
    print "Servidor: $python TCPxatSC.py -s [host] [port]"
    print "Client: $python TCPxatSC.py -c [host] [port]"
