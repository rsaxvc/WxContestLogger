import sqlite3
import paths

class db_manager:
	def __init__( self ):
		self.conn = sqlite3.connect(paths.dbdir+'contacts.db')

		c = self.conn.cursor()
		c.execute( "PRAGMA foreign_keys = ON" )
		c.execute( "CREATE TABLE IF NOT EXISTS clients( uuid CHAR(36) PRIMARY KEY ASC, seq INTEGER, name TEXT )" )
		c.execute( "CREATE TABLE IF NOT EXISTS differences( client_uuid INTEGER NOT NULL, client_seq INTEGER NOT NULL, json TEXT, FOREIGN KEY( client_uuid ) REFERENCES clients( rowid ), PRIMARY KEY( client_uuid, client_seq )  )" )
		c.execute( "CREATE TABLE IF NOT EXISTS contacts( client_uuid INTEGER NOT NULL, client_rec INTEGER, mycall TEXT, theircall TEXT, foreign key( client_uuid ) references clients( rowid ), PRIMARY KEY( client_uuid, client_rec ) )" )

	class filter:
		contains=""

	class search_result:
		mycall=""
		theircall=""

	def search( self, f ):
		c = self.conn.cursor()
		print f.contains
		c.execute("SELECT mycall,theircall FROM contacts WHERE theircall LIKE '%' || ? || '%' ", [ f.contains ] )
		while( True ):
			row = c.fetchone()
			if row == None:
			    break
			result = self.search_result()
			result.mycall = row[0]
			result.theircall = row[1]
			yield result

