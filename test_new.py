#!/usr/bin/python
# -*- coding: utf-8 -*-

from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer
from localtimeutil import local8601

db = db_manager()
s = settings_manager()
uuid = s.get( "uuid" )
db.insert_local_contact( uuid, local8601(), "KD0LIX", "KC5YTI", "80m" )
