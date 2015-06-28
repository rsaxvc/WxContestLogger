#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paths

os.remove( paths.dbdir + 'contacts.db' )

from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer
from localtimeutil import local8601

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
db.insert_frames( [ f ] )

db.process_new_frames()
count = 0
for r in db.search(db_manager.filter()):
	count = count + 1
if( count == 1 ):
	print "success"
else:
	print "failure"
