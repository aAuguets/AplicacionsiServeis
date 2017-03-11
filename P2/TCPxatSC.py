# -*- coding: utf-8 -*-

# Xat usant TCP
# Adria Auguets i Pavel Macutela

import socket, sys, select, struct, signal
port = 5000         #per defecte.
host = '127.0.0.1'  #per defecte.    #'10.192.225.4'#'10.192.33.172'#'10.192.107.42'
dClients = {}
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
    read, _ , _ = select.select(data, [], [])
    if read[0] == data[0]: #nou client
        socketc, addr = data[0].accept()
        dClients["Client"+str(nclients)]=socketc
        print "Conexio realitzada amb :", addr, "correctament.\nAssignat com a Client", nclients
        nclients +=1
    
    elif read[0] == data[1]: #teclat
        msg = sys.stdin.readline()
        toClient = msg.split(':')
        if len(toClient)==1:
            print "Err: Format-> ClientNUM:MSG"
        else:
            if toClient[0] in dClients.keys():
                dClients[toClient[0]].send(toClient[1])
            else:
                print "Client Desconegut."
    else: #msg in
        txt = read[element].recv(1024)
        num_client = posicio_dClients(dClients, read)
        if txt == '':
            print "Client", num_client, "Desconectat."
            del dClients[num_client]
            read.close()
        else:
            print "Client", num_client, ":", txt
            

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
    List = []
    setupServer(port, host)
    List += [sys.stdin]
    while(True):
        selectServer(List)
else:
    print "Servidor: $python TCPxatSC.py -s [host] [port]"
    print "Client: $python TCPxatSC.py -c [host] [port]"
