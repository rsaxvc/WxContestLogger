class frame:
	"""This is a container for network frames"""
	dbTypeUpsert=0
	dbTypeDelete=1

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
		d['type']=self.type
		d['call0']=self.my_callsign
		d['call1']=self.their_callsign
		d['dt']=self.datetime
		d['seq'] = self.sequence_number
		d['rec'] = self.affected_record
		import json
		import zlib
		return zlib.compress( json.dumps( d ) )

	def unpack( self, blob ):
		"convert packet to class"
		import json
		import zlib
		d = json.loads( zlib.decompress( blob ) )
		self.type = d['type']
		self.my_callsign = d['call0']
		self.their_callsign = d['call1']
		self.datetime = d['dt']
		self.sequence_number = d['seq']
		self.affected_record = d['rec']

	def default(self):
		pass
