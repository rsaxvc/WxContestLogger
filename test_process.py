#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paths

os.remove( paths.dbdir + 'contacts.db' )

from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer
from localtimeutil import local8601

def countContacts(db):
	count = 0
	for r in db.search(db_manager.filter()):
		count = count + 1
	return count

db = db_manager()
s = settings_manager()

f = {}
f['uuid'] = s.get( 'uuid' )
f['type'] = framer.typeDbUpsert
f['dt'] = local8601()
f['rec'] = 1
f['seq'] = 1
f['band'] = "20m"
f['mode'] = "phone"
f['mycall'] = "KD0LIX"
f['theircall'] = "KD0IXY"
f['class'] = "1A"
f['section'] = "KS"

#test insert
db.insert_frames( [ f ] )
db.process_new_frames()
if( countContacts( db ) == 1 ):
	print "success"
else:
	print "failureA"

#test second insert
f['rec'] = 2
f['seq'] = 2
db.insert_frames( [ f ] )
db.process_new_frames()
if( countContacts( db ) == 2 ):
	print "success"
else:
	print "failureB: RecordCount:", countContacts( db )

#Test upsert
f['rec'] = 2
f['seq'] = 3
db.insert_frames( [ f ] )
db.process_new_frames()
if( countContacts( db ) == 2 ):
	print "success"
else:
	print "failureC: RecordCount:", countContacts( db )

#Test delete
f = {}
f['uuid'] = s.get( 'uuid' )
f['type'] = framer.typeDbDelete
f['rec'] = 2
f['seq'] = 4
db.insert_frames( [ f ] )
db.process_new_frames()
if( countContacts( db ) == 1 ):
	print "success"
else:
	print "failureD: RecordCount:", countContacts( db )
