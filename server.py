# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while 1:
    received, f = s.recvfrom(1024)
    print received
    send = raw_input("msg: ")
    s.sendto(send, f)
s.close()