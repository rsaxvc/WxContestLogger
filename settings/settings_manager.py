from uuid import uuid4
import os

import settings_io

class settings_manager:
	"a non-volatile key-value store"
	def __init__(_self):
		"open settings file and create a default if needed"
		dirpath = os.path.expanduser("~")+"/.wxlogger/"
		_self.configpath = dirpath + "config"
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		_self.settings = settings_io.settings_io()
		try:
			_self.settings.load( _self.configpath )
		except IOError:
			pass
		if( _self.settings.get( "uuid" ) == "" ):
			_self.settings.put( "uuid", uuid4() )
			_self.settings.save( _self.configpath )

	def save( _self ):
		_self.settings.save( _self.configpath )

	def get( _self, key ):
		return _self.settings.get( key )

	def put( _self, key, value ):
		_self.settings.put( key, value )
