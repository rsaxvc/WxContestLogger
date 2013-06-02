import time
import socket
import pickle
import uuid

import dbframe
import contactdb

def process_database_changes():
	pass

def request_missing_changes():
	pass

def send_periodic_packets():
	global id
	message = dbframe.frame()
	message.my_callsign = "KD0LIX"
	message.their_callsign = "KD0IXY"
	message.type = dbframe.frame.typeDbUpsert
	message.datetime = "Wednesday"
	message.sequence_number = id
	message.affected_record = 3

	sock.sendto(message.pack(), (UDP_IP, UDP_PORT))

	message = dbframe.frame()
	message.type = dbframe.frame.typeDbDelete
	message.sequence_number = id
	message.affected_record = 3
	id = id + 1

	sock.sendto(message.pack(), (UDP_IP, UDP_PORT))

def send_hello():
	pass

def send_goodbye():
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
		frame.typeDbUpsert:handle_frame_upsert,
		frame.typeDbDelete:handle_frame_delete,
		frame.typeNetHello:handle_frame_hello,
		frame.typeNetReqClientList:handle_frame_req_client_list,
		frame.typeNetClientList:handle_frame_client_list,
		frame.typeNetReqClientUpdates:handle_frame_req_client_updates,
		}
	try:
		handlers[frame.type](frame)
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
			frame = dbframe.frame()
			frame.unpack( blob1 )
			print "received ", len( blob1 ), " byte message from:", frame.their_callsign
			handle_frame( frame )
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
