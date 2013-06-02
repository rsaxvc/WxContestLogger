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

	def frame_hello( self, uuid ):
		"convert class to packet"
		d={}
		d['type']=self.typeNetHello
		d['cid']=uuid
		self._frames.append( d )

	def frame_upsert( self, uuid, sequence_number, affected_record, datetime, mycall, theircall ):
		d={}
		d['type'] = self.typeDbUpsert
		d['cid']  = uuid
		d['seq']  = sequence_number
		d['rec']  = affected_record
		d['dt']   = datetime
		d['mycall']= mycall
		d['theircall']= theircall
		self._frames.append( d )

	def frame_delete( self, uuid, sequence_number, affected_record ):
		d={}
		d['type'] = self.typeDbDelete
		d['cid']  = uuid
		d['seq']  = sequence_number
		d['rec']  = affected_record
		self._frames.append( d )

	def pack( self, mtu ):
		import json
		import zlib
		#what should happen here, is breaking the packet
		#into multiple smaller onces so it fits in the
		#mtu. Not implemented yet
		p = zlib.compress( json.dumps( self._frames ) )
		self._frames[:] = []
		packets=[p]
		return packets

	def unpack( self, blob ):
		"convert packet to class"
		import json
		import zlib
		f = json.loads( zlib.decompress( blob ) )
		return f

	def default(self):
		pass
