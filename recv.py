import socket
import pickle
import uuid

import dbframe
import contactdb

myid = uuid.uuid4()

UDP_IP = "127.0.0.1"
UDP_PORT = 32250

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    blob1, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    frame = dbframe.frame()
    frame.unpack( blob1 )
    print "received ", len( blob1 ), " byte message from:", frame.their_callsign
    print "type:", frame.type
