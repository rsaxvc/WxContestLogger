class settings_io:
	def __init__(_self):
		_self.values = dict()

	def save( _self, filename ):
		f = open( filename, 'w' )
		for v in _self.values.items():
			f.write( str(v[0])+":"+str(v[1])+"\n" )
		f.close()

	def parse( _self, f ):
		while( 1 ):
			line = f.readline()
			if( line == "" ):
				break
			line = line[:-1]
			key_value_pair=line.partition(':')
			key=key_value_pair[0]
			value=key_value_pair[2]
			_self.put( key, value )

	def load( _self, filename ):
		f = open( filename, 'r' )
		_self.parse( f )
		f.close()

	def get( _self, key ):
		try:
			return _self.values[key]
		except KeyError:
			return ""

	def put( _self, key, value ):
		_self.values[ key ] = value
