#!/usr/bin/python
# -*- coding: utf-8 -*-

from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer

db = db_manager()
s = settings_manager()
uuid = s.get( "uuid" )
db.insert_local_contact( uuid, "somedate.sometime", "KD0LIX", "KC5YTI" )
