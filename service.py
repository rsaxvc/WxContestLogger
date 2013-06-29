import time
import socket
import pickle
import uuid
import random

import dbframe
from db_manager import db_manager
from settings_manager import settings_manager

def process_incoming_packets( sock ):
	"receive and handle new packets, for 8 to 10 second"
	timeout = 8.0 + random.uniform(0,10)
	stop_time = time.time() + timeout
	while( timeout > 0.0 ):
		sock.settimeout(timeout)
		try:
			blob1, addr = sock.recvfrom(2048)
			print "received ", len( blob1 ), " byte message from ", addr
			frame = dbframe.framer()
			frames = frame.unpack( blob1 )
			for f in frames:
				handle_frame( f )
		except socket.timeout:
			break;
		timeout = stop_time - time.time()

def process_database_changes():
	db = db_manager()
	db.process_new_frames()

def request_missing_changes():
	pass

def send_periodic_packets():
	s = settings_manager()
	uuid = s.get( "uuid" )

	db = db_manager()

	messages = dbframe.framer()
	messages.frame_hello( uuid, db.get_seq_from_uuid( uuid ) )

	packets = messages.pack( 1200 )
	for p in packets:
		sock.sendto( p, (UDP_IP, UDP_PORT) )

def send_goodbye():
	#broadcast a goodbye packet
	pass

def handle_frame_hello(frame):
	print "hello from ",frame['uuid']," seq:",frame['seq']

def handle_frame_upsert(frame):
	print "upsert"
	db = db_manager()
	db.insert_frames( [frame] )

def handle_frame_delete(frame):
	print "delete"
	db = db_manager()
	db.insert_frames( [frame] )

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

UDP_IP = "255.255.255.255"
UDP_PORT = 32250

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))
if hasattr(socket,'SO_BROADCAST'):
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

id = 0

while True:
	process_incoming_packets(sock)
	process_database_changes()
	request_missing_changes()
	send_periodic_packets()
send_goodbye()
