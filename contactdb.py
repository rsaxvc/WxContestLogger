class contactdb():
	def default(self):
		return 5
	c=()
	def open( conn ):
		c = conn.cursor()

	def close():
		c.close()

	def insert( id, host_uuid, host_call, other_call, datetime ):
		print "insert not implemented"

	def update( id, host_uuid, host_call, other_call, datetime ):
		print "update not implemented"

	def remove( id, host_uuid ):
		print "remove not implemented"

	def search( callsign ):
		print "search not implemented"
		return []
