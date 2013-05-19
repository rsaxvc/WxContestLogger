from uuid import uuid4
import os

import settings_io

class settings_manager:
	"a non-volatile key-value store"
	def __init__(_self):
		"open settings file and create a default if needed"
		_self.filename = os.path.expanduser("~")+"/.wxlogger"
		_self.settings = settings_io.settings_io()
		try:
			_self.settings.load( _self.filename )
		except IOError:
			pass
		if( _self.settings.get( "uuid" ) == "" ):
			_self.settings.put( "uuid", uuid4() )
			_self.settings.save( _self.filename )

	def save( _self ):
		_self.settings.save( _self.filename )

	def get( _self, key ):
		return _self.settings.get( key )

	def put( _self, key, value ):
		_self.settings.put( key, value )
