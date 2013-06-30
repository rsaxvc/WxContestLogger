class framer:
	"""This is a container for network frames"""

	#commands that modify database state
	typeDbUpsert=0#update or insert
	typeDbDelete=1#delete by uuid+rowid

	#commands that affect network
	typeNetHello=256            #initiates communication, usually broadcast on startup+periodically
	typeNetGoodbye=257          #user closes program
	typeNetReqClientList=258    #asks to enumerate clients
	typeNetClientList=259		#list of clients w/uuid and current sequence number, response to 258
	typeNetReqClientUpdates=260 #asks to list all upserts+deletes for specific UUID and list of seq ranges

	_frames=[]

	def frame_request_client_updates( self, uuid, start, end ):
		d={}
		d['type']=self.typeReqClientUpdates
		d['uuid']=str(uuid)
		d['seq_start']=start
		d['seq_end']=end
		self._frames.append( d )

	def frame_raw( self, frame ):
		self._frames.append( frame )

	def frame_hello( self, uuid, seq ):
		"convert class to packet"
		d={}
		d['type']=self.typeNetHello
		d['uuid']=str(uuid)
		d['seq']=seq
		self._frames.append( d )

	def frame_goodbye( self, uuid ):
		"convert class to packet"
		d={}
		d['type']=self.typeNetHello
		d['uuid']=str(uuid)
		self._frames.append( d )

	def frame_upsert( self, uuid, sequence_number, affected_record, datetime, mycall, theircall, band, mode ):
		d={}
		d['type']     = self.typeDbUpsert
		d['uuid']     = str(uuid)
		d['seq']      = sequence_number
		d['rec']      = affected_record
		d['dt']       = datetime
		d['mycall']   = mycall
		d['theircall']= theircall
		d['band']     =band
		d['mode']     =mode
		self._frames.append( d )

	def frame_delete( self, uuid, sequence_number, affected_record ):
		d={}
		d['type'] = self.typeDbDelete
		d['uuid'] = str(uuid)
		d['seq']  = sequence_number
		d['rec']  = affected_record
		self._frames.append( d )

	def pack( self, mtu ):
		"return a list of packets and clean the frame list"
		import json
		import zlib

		packets = []

		#so, frames are pretty small, and on many
		#networks we can fit multiple frames per packet
		frames_so_far = 0
		while( frames_so_far != len( self._frames ) ):
			#However, we also need to split packets along frame boundaries
			#this scope emits one packet with one or more frames per execution
			frames_in_packet = len( self._frames ) - frames_so_far
			while( True ):
				p = zlib.compress( json.dumps( self._frames[frames_so_far:frames_so_far+frames_in_packet] ) )
				if( frames_in_packet == 1 ):
					#if only one frame is left then just send it.
					#however, this also handles a frame > packet, which
					#is just going to fragment :(
					break
				elif( len( p ) <= mtu ):
					#found the right number of frames
					#to pack into this packet
					break
				else:
					#the packed data is too large, try again with
					#fewer frames in this packet
					frames_in_packet = frames_in_packet - 1

			frames_so_far = frames_so_far + frames_in_packet
			packets.append( p )
		self._frames[:] = []
		return packets

	def pop_tail( self ):
		"return newest frame and remove from the frame list"
		return self._frames.pop()

	def unpack( self, blob ):
		"convert packet to class"
		import json
		import zlib
		f = json.loads( zlib.decompress( blob ) )
		return f

	def default(self):
		pass
