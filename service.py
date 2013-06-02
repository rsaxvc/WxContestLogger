import time
import socket
import pickle
import uuid

import dbframe
import contactdb
from settings_manager import settings_manager

def process_database_changes():
	pass

def request_missing_changes():
	pass

def send_periodic_packets():
	global id

	s = settings_manager()
	uuid = s.get( "uuid" )

	messages = dbframe.framer()
	messages.frame_upsert( uuid, id, 3, "Wednesday", "KD0LIX", "KD0IXY" )
	id = id + 1
	messages.frame_delete( uuid, id, 3 )
	id = id + 1

	packets = messages.pack( 1200 )
	for p in packets:
		sock.sendto( p, (UDP_IP, UDP_PORT) )

def send_hello():
	#broadcast a hello packet
	pass

def send_goodbye():
	#broadcast a goodbye packet
	pass

def handle_frame_hello(frame):
	print "hello"

def handle_frame_upsert(frame):
    print "upsert"

def handle_frame_delete(frame):
    print "delete"

def handle_frame_req_client_list(frame):
	print "req_client_list"

def handle_frame_client_list(frame):
	print "client_list"

def handle_frame_req_client_updates(frame):
	print "req_client_updates"

def handle_frame( frame ):
	handlers={
		dbframe.framer.typeDbUpsert:handle_frame_upsert,
		dbframe.framer.typeDbDelete:handle_frame_delete,
		dbframe.framer.typeNetHello:handle_frame_hello,
		dbframe.framer.typeNetReqClientList:handle_frame_req_client_list,
		dbframe.framer.typeNetClientList:handle_frame_client_list,
		dbframe.framer.typeNetReqClientUpdates:handle_frame_req_client_updates,
		}
	try:
		handlers[frame['type']](frame)
	except KeyError:
		print "unknown frame type:",frame.type


myid = uuid.uuid4()

UDP_IP = "127.0.0.1"
UDP_PORT = 32250

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.settimeout(1.0) # block up to 1 second waiting for data
sock.bind((UDP_IP, UDP_PORT))

id = 0

send_hello()
while True:
	#handle all receivable packets
	while True:
		try:
			blob1, addr = sock.recvfrom(2048)
			frame = dbframe.framer()
			frames = frame.unpack( blob1 )
			for f in frames:
				print "received ", len( blob1 ), " byte message"
				handle_frame( f )
		except socket.timeout:
			break;

	process_database_changes()
	request_missing_changes()
	send_periodic_packets()
send_goodbye()

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
