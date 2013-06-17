#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paths

os.remove( paths.dbdir + 'contacts.db' )

from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer

db = db_manager()
s = settings_manager()

f = {}
f['uuid'] = s.get( 'uuid' )
f['type'] = framer.typeDbUpsert
f['rec'] = 1
f['seq'] = 1
f['mycall'] = "KD0LIX"
f['theircall'] = "KD0IXY"
db.insert_frames( [ f ] )

db.process_new_frames()
count = 0
filt = db_manager.filter()
filt.contains=""
for r in db.search(filt):
	count = count + 1
if( count == 1 ):
	print "success"
else:
	print "failure"
