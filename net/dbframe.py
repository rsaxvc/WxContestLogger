class frame:
	"""This is a container for network frames"""
	dbTypeInsert=0
	dbTypeUpdate=1
	dbTypeDelete=2

	type=dbTypeInsert
	source=""
	sequence_number=-1
	affected_record=-1
	datetime=-1
	my_callsign=""
	their_callsign=""
	text_blob=""
	def pack( self ):
		import pickle
		import zlib
		return zlib.compress( pickle.dumps( self ) )
	def unpack( self, blob ):
		import pickle
		import zlib
		p = pickle.loads( zlib.decompress( blob ) )
		self.type = p.type
		self.my_callsign = p.my_callsign
		self.their_callsign = p.their_callsign
		self.datetime = p.datetime
		self.source = p.source
		self.sequence_number = p.sequence_number
		self.affected_record = p.affected_record
		self.source = p.source
	def default(self):
		pass
