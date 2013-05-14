import socket
import time
import random

import dbframe

UDP_IP = "127.0.0.1"
UDP_PORT = 32250

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


id = 0
while True:
	record = (id, "KD0LIX", random.randrange(100), "20 Meter Band", "Digital")
	message = dbframe.frame()
	message.my_callsign = "KD0LIX"
	message.their_callsign = "KD0IXY"
	message.type = dbframe.frame.dbTypeInsert

	# Pickle dictionary using protocol 0.
	sock.sendto(message.pack(), (UDP_IP, UDP_PORT))
	time.sleep(1)
