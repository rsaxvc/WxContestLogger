import sqlite3
import paths

class db_manager:
	"handles database i/o, one layer up from python/sqlite3"
	def __init__( self ):
		self.conn = sqlite3.connect(paths.dbdir+'contacts.db')

		c = self.conn.cursor()
		c.execute( "PRAGMA foreign_keys = ON" )
		#This rowid declaration is special.
		#By declaring it as Integer Primary Key, we can now use it
		#as the target of foreign key constraints
		c.execute( "CREATE TABLE IF NOT EXISTS clients( rowid INTEGER PRIMARY KEY, uuid CHAR(36) UNIQUE, seq INTEGER, name TEXT )" )
		c.execute( "CREATE TABLE IF NOT EXISTS differences( client_uuid INTEGER NOT NULL, client_seq INTEGER NOT NULL, json TEXT, FOREIGN KEY( client_uuid ) REFERENCES clients( rowid ), PRIMARY KEY( client_uuid, client_seq )  )" )
		c.execute( "CREATE TABLE IF NOT EXISTS contacts( client_uuid INTEGER NOT NULL, client_rec INTEGER NOT NULL, mycall TEXT NOT NULL, theircall TEXT NOT NULL, foreign key( client_uuid ) REFERENCES clients( rowid ), PRIMARY KEY( client_uuid, client_rec ) )" )
	class filter:
		contains=""

	class search_result:
		mycall=""
		theircall=""

	def _find_client_uuid( self, uuid ):
		c = self.conn.cursor()
		c.execute( "SELECT rowid FROM clients WHERE uuid = ?", [uuid] )
		row = c.fetchone()
		c.close()
		if row == None:
			return None
		else:
			return row[0]

	def _insert_uuid_if_needed( self, uuid ):
		"create a new client row if needed"
		c = self.conn.cursor()
		if self._find_client_uuid( uuid ) == None:
			c.execute( "INSERT INTO clients(uuid,seq,name) VALUES(?,?,?)", [uuid,0,"unnamed"] )
		c.close()
		self.conn.commit()

	def insert( self, uuid, mycall, theircall ):
		"temporary method for testing - this should be reimplemented with change frames"
		self._insert_uuid_if_needed( uuid )
		client_uuid = self._find_client_uuid( uuid )
		c = self.conn.cursor()
		c.execute( "SELECT MAX( client_rec ) FROM contacts WHERE client_uuid == ?", [ client_uuid ] )
		row = c.fetchone()
		if row == None:
			client_rec = 0
		elif row[0] == None:
			client_rec = 0
		else:
			client_rec = row[0] + 1

		c.execute( "INSERT INTO contacts VALUES(?,?,?,?)", ( client_uuid, client_rec, mycall, theircall ) )
		c.close()
		self.conn.commit()

	def search( self, f ):
		c = self.conn.cursor()
		c.execute("SELECT mycall,theircall FROM contacts WHERE theircall LIKE '%' || ? || '%' ", [ f.contains ] )
		while( True ):
			row = c.fetchone()
			if row == None:
			    break
			result = self.search_result()
			result.mycall = row[0]
			result.theircall = row[1]
			yield result

