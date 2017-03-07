from socket import *
from select import *

# Information of our server to connect to
HOST = "127.0.0.1"
PORT = 1993

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))

# Client loop
while(True):
    # Let the user enter some data to send
    data = input("&gt;&gt; ")
    read, write, error = select([],[sock],[],0)
    if(len(write)):
        # Send the data to the server
        b = sock.send(str.encode(data))

    # The receiving loop
    while(True):
        # When receiving, use the timeout of 1 to receive more data
        read, write, error = select([sock],[],[],1)

        # If there is data, print it
        if(len(read)):
            data = bytes.decode(sock.recv(1024))
            print(data)
        # Exit the loop if no more data
        else:
            break
