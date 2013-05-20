import sqlite3
import paths

class db_manager:
	conn = sqlite3.connect(paths.dbdir+'contacts.db')

	"PRAGMA foreign_keys = ON;"
	"CREATE TABLE clients( uuid CHAR(36) PRIMARY KEY ASC, seq INTEGER, name TEXT );"
	"CREATE TABLE differences( client_uuid INTEGER NOT NULL, client_seq INTEGER NOT NULL, json TEXT, FOREIGN KEY( client_uuid ) REFERENCES clients( rowid ), PRIMARY KEY( client_uuid, client_seq )  );"
	"CREATE TABLE contacts( client_uuid INTEGER NOT NULL, client_rec INTEGER, mycall TEXT, theircall TEXT, foreign key( client_uuid ) references clients( rowid ), PRIMARY KEY( client_uuid, client_rec ) );"
