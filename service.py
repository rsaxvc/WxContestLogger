import time
import socket
import pickle
import uuid
import random

import dbframe
from db_manager import db_manager
from settings_manager import settings_manager

class service:
	def __init__( _self ):
		"""hook up database, framer, and bind UDP"""
		_self.db = db_manager()

		settings = settings_manager()

		_self.my_uuid = settings.get( "uuid" )
		_self.my_last_seq = _self.db.get_seq_from_uuid( _self.my_uuid )

		_self.handlers={
			dbframe.framer.typeDbUpsert:_self.handle_frame_upsert,
			dbframe.framer.typeDbDelete:_self.handle_frame_delete,
			dbframe.framer.typeNetHello:_self.handle_frame_hello,
			dbframe.framer.typeNetReqClientList:_self.handle_frame_req_client_list,
			dbframe.framer.typeNetClientList:_self.handle_frame_client_list,
			dbframe.framer.typeNetReqClientUpdates:_self.handle_frame_req_client_updates,
			}

		_self.framer = dbframe.framer()

		#broadcast to everybody.
		#Should be able to programatically
		#compute local broadcast address
		#but also seems that most routers drop these
		#so this should work fine
		_self.UDP_IP = "255.255.255.255"
		_self.UDP_PORT = 32250

		_self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		_self.sock.bind((_self.UDP_IP, _self.UDP_PORT))
		if hasattr(socket,'SO_BROADCAST'):
			#add broadcast abilities
			_self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	def process_incoming_packets( _self ):
		"""receive and handle new packets, for 8 to 10 seconds"""
		timeout = 8.0 + random.uniform(0,2)
		stop_time = time.time() + timeout
		while( timeout > 0.0 ):
			_self.sock.settimeout(timeout)
			try:
				blob1, addr = _self.sock.recvfrom(2048)
				print "received ", len( blob1 ), " byte message from ", addr
				frame = dbframe.framer()
				frames = frame.unpack( blob1 )
				for f in frames:
					_self.handle_frame( f )
			except socket.timeout:
				break;
			timeout = stop_time - time.time()

		#restore socket back to blocking
		_self.sock.settimeout(None)

	def process_database_changes( _self ):
		"""apply differences to contacts"""
		_self.db.process_new_frames()

	def queue_requests_for_missing_changes( _self ):
		"""search database for holes in seq numbers, and queue requests for them"""
		pass

	def queue_periodic_packets( _self ):
		"""queue timed packets"""
		crnt_seq = _self.db.get_seq_from_uuid( _self.my_uuid )

		#add a hello frame
		_self.framer.frame_hello( _self.my_uuid, crnt_seq )

		#add any new frames generated that haven't been sent at least once
		if( crnt_seq != _self.my_last_seq ):
			for packet in _self.db.get_packets( _self.my_uuid, _self.my_last_seq, crnt_seq ):
				_self.framer.frame_raw( packet )
			_self.my_last_seq = crnt_seq;

	def send_queued_packets( _self ):
		"""pops messages from queue and sends them over UDP"""
		packets = _self.framer.pack( 1200 )
		for p in packets:
			_self.sock.sendto( p, (_self.UDP_IP, _self.UDP_PORT) )

	def queue_goodbye( _self ):
		"""queue a goodbye frame"""
		_self.framer.frame_goodbye( _self.my_uuid )

	def handle_frame_hello( _self, frame ):
		print "hello from ", frame['uuid'], " seq:", frame['seq']

	def handle_frame_upsert( _self, frame ):
		print "upsert"
		_self.db.insert_frames( [frame] )

	def handle_frame_delete( _self, frame ):
		print "delete"
		db = db_manager()
		_self.db.insert_frames( [frame] )

	def handle_frame_req_client_list( _self, frame ):
		print "req_client_list"

	def handle_frame_client_list( _self, frame ):
		print "client_list"

	def handle_frame_req_client_updates( _self, frame ):
		print "req_client_updates"

	def handle_frame( _self, frame ):
		if( frame['uuid'] != _self.my_uuid ):
			try:
				_self.handlers[frame['type']](frame)
			except KeyError:
				print "unknown frame type:",frame.type



s = service();

while True:
	s.queue_periodic_packets()
	s.send_queued_packets()
	s.process_incoming_packets()
	s.process_database_changes()
	s.queue_requests_for_missing_changes()
send_goodbye()
