class frame:
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

	client_uuid="00000000-0000-0000-0000-000000000000"
	type=0
	sequence_number=-1
	affected_record=-1
	datetime=""
	my_callsign=""
	their_callsign=""
	text_blob=""

	def pack( self ):
		"convert class to packet"
		d={}
		d['cid']=self.client_uuid
		d['type']=self.type
		d['seq'] = self.sequence_number
		d['rec'] = self.affected_record
		if( self.type == self.typeDbUpsert ):
			d['dt']=self.datetime
			d['call0']=self.my_callsign
			d['call1']=self.their_callsign
		import json
		import zlib
		return zlib.compress( json.dumps( d ) )

	def unpack( self, blob ):
		"convert packet to class"
		import json
		import zlib
		d = json.loads( zlib.decompress( blob ) )
		self.client_uuid=d['cid']
		self.type = d['type']
		self.sequence_number = d['seq']
		self.affected_record = d['rec']
		if( self.type == self.typeDbUpsert ):
			self.my_callsign = d['call0']
			self.their_callsign = d['call1']
			self.datetime = d['dt']

	def default(self):
		pass
