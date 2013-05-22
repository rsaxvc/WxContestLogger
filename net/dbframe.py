class frame:
	"""This is a container for network frames"""
	dbTypeUpsert=0
	dbTypeDelete=1
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
		if( self.type == self.dbTypeUpsert ):
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
		if( self.type == self.dbTypeUpsert ):
			self.my_callsign = d['call0']
			self.their_callsign = d['call1']
			self.datetime = d['dt']

	def default(self):
		pass
