
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
		c.execute( "CREATE TABLE IF NOT EXISTS contacts( client_uuid INTEGER NOT NULL, client_rec INTEGER NOT NULL, mycall TEXT NOT NULL, theircall TEXT NOT NULL, band TEXT, datetime8601 TEXT, mode TEXT, class TEXT, section TEXT, foreign key( client_uuid ) REFERENCES clients( rowid ), PRIMARY KEY( client_uuid, client_rec ) )" )
	class filter:
		contains=""

	class search_result:
		mycall=""
		theircall=""
		band=""
		datetime=""
		mode=""
		class_=""
		section=""

	def _find_client_uuid( self, c, uuid ):
		c.execute( "SELECT rowid FROM clients WHERE uuid = ?", [uuid] )
		row = c.fetchone()
		if row == None:
			return None
		else:
			return row[0]

	def _insert_uuid_if_needed( self, c, uuid ):
		"create a new client row if needed"
		uuid_idx = self._find_client_uuid( c, uuid )
		if uuid_idx == None:
			c.execute( "INSERT INTO clients(uuid,seq,name) VALUES(?,?,?)", [uuid,0,"unnamed"] )
			uuid_idx = self._find_client_uuid( c, uuid )
		return uuid_idx

	def _insert_frames( self, c, frames ):
		from dbframe import framer
		for frame in frames:
			try:
				uuid = frame['uuid']
			except KeyError:
				print "no uuid"
				continue

			try:
				seq = frame['seq']
			except KeyError:
				print "no seq"
				continue

			if frame['type'] < framer.typeDbFirst:
				continue

			if frame['type'] > framer.typeDbLast:
				continue

			uuid_idx = self._insert_uuid_if_needed( c, uuid )
			import json
			c.execute( "INSERT OR IGNORE INTO differences(client_uuid,client_seq,json) VALUES(?,?,?)", [uuid_idx, seq, json.dumps( frame ) ] )

	def insert_frames( self, frames ):
		"record frames into the database, but don't process it yet"
		c = self.conn.cursor()
		self._insert_frames( c, frames )
		c.close()
		self.conn.commit()

	def _get_current_client_seq( self, c, uuid ):
		"get the latest sequence number for a client. Returns 0 if no client"
		c.execute( "SELECT seq FROM clients WHERE uuid = ?", [ uuid ] )
		row = c.fetchone()
		if row == None:
			return 0
		elif row[0] == None:
			return 0
		else:
			return row[0]

	def _set_current_client_seq( self, c, uuid, seq ):
		c.execute( "UPDATE clients SET seq = ? WHERE uuid = ?", [ seq, uuid ] )
		
	def insert_local_contact( self, uuid, datetime, mycall, theircall, band, mode, class_, section ):
		from dbframe import framer
		"store a new contact and its insert frame"
		c = self.conn.cursor()
		uuid_idx = self._insert_uuid_if_needed( c, uuid )
		c.execute( "SELECT MAX( client_rec ) FROM contacts WHERE client_uuid == ?", [ uuid_idx ] )
		row = c.fetchone()
		if row == None:
			client_rec = 0
		elif row[0] == None:
			client_rec = 0
		else:
			client_rec = row[0] + 1

		c.execute( "INSERT INTO contacts VALUES(?,?,?,?,?,?,?,?,?)", ( uuid_idx, client_rec, mycall, theircall,  band, datetime, mode, class_, section ) )
		f = framer()
		seq = self._get_current_client_seq( c, uuid ) + 1
		f.frame_upsert( uuid, seq, client_rec, datetime, mycall, theircall, band, mode )
		self._insert_frames( c, [ f.pop_tail() ] )
		self._set_current_client_seq( c, uuid, seq )
		c.close()
		self.conn.commit()

	def get_seq_from_uuid( self, uuid ):
		c = self.conn.cursor()
		result = self._get_current_client_seq( c, uuid )
		c.close()
		return result		

	def get_packets( self, uuid, min_seq, max_seq ):
		import json
		c = self.conn.cursor()
		client_uuid = self._insert_uuid_if_needed( c, uuid )
		c.execute("SELECT json FROM differences WHERE client_uuid = ? AND client_seq BETWEEN ? AND ?", ( client_uuid, min_seq + 1, max_seq ) )
		while( True ):
			row = c.fetchone()
			if row == None:
				break
			result = json.loads( row[0] )
			yield result
		c.close()

	def next_difference_seq_from_uuid( self, uuid ):
		c = self.conn.cursor()
		client_uuid = self._insert_uuid_if_needed( c, uuid )
		cur_seq = self._get_current_client_seq( c, uuid )
		next_seq = cur_seq
		c.execute("SELECT MIN( client_seq ) FROM differences WHERE client_uuid = ? AND client_seq > ?", ( client_uuid, cur_seq ) )
		row = c.fetchone()
		if row != None:
			next_seq = row[0]
		c.close()
		return next_seq

	def search_clients_with_missing_frames( self ):
		c = self.conn.cursor()
		c.execute( "SELECT uuid,seq FROM clients" )
		client_list = c.fetchall()
		result_list = []
		for client in client_list:
			uuid = client[0]
			crnt_seq = client[1]
			next_seq = self.next_difference_seq_from_uuid( uuid )
			if( crnt_seq != next_seq ):
				result_list.append(uuid)
		c.close()
		return result_list

	def search( self, f ):
		c = self.conn.cursor()
		c.execute("SELECT mycall,theircall,band,datetime8601,mode,class,section FROM contacts WHERE theircall LIKE '%' || ? || '%' order by datetime8601 DESC ", [ f.contains ] )
		while( True ):
			row = c.fetchone()
			if row == None:
				break
			result = self.search_result()
			result.mycall = row[0]
			result.theircall = row[1]
			result.band=row[2]
			result.datetime=row[3]
			result.mode=row[4]
			result.class_=row[5]
			result.section=row[6]
			yield result

	def _process_frame( self, c, f ):
		from dbframe import framer
		uuid = f['uuid']
		uuid_idx = self._insert_uuid_if_needed( c, uuid )
		if( f['type'] == framer.typeDbUpsert ):
			c.execute( "INSERT OR REPLACE INTO contacts VALUES(?,?,?,?,?,?,?)", [ uuid_idx, f['rec'], f['mycall'], f['theircall'], f['band'], f['dt'], f['mode'] ] )
		elif( f['type'] == framer.typeDbDelete ):
			c.execute( "DELETE FROM contacts WHERE client_uuid = ? AND client_rec = ?", [ uuid_idx, f['rec'] ] )
		else:
			print "unknown packet type:",f['type']
		self._set_current_client_seq( c, uuid, f['seq'] )
		pass

	def process_new_frames( self ):
		c = self.conn.cursor()
		c.execute( "SELECT rowid,seq FROM clients" )
		client_list = c.fetchall()
		for client in client_list:
			client_idx = client[0]
			next_seq = client[1] + 1
			while(True):
				c.execute( "SELECT json FROM differences WHERE client_uuid = ? AND client_seq = ?", [ client_idx, next_seq ] )
				row = c.fetchone()
				if row == None:
					break
				elif row[0] == None:
					break
				json_text = row[0]
				import json
				self._process_frame( c, json.loads( json_text ) )

		c.close()
		self.conn.commit()
