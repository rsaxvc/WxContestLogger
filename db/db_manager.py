import sqlite3
import paths

class db_manager:
	conn = sqlite3.connect(paths.dbdir+'contacts.db')

	"PRAGMA foreign_keys = ON;"
	"CREATE TABLE known_clients( uuid CHAR(36) PRIMARY KEY ASC, revision INTEGER);"
	"CREATE TABLE contacts( client_uuid INTEGER NOT NULL, client_rec INTEGER, mycall TEXT, theircall TEXT, foreign key( client_uuid ) references known_clients( rowid ), PRIMARY KEY( client_uuid, client_rec ) );"
