#!/usr/bin/python
# -*- coding: utf-8 -*-

from settings_manager import settings_manager

s = settings_manager()
s.put( "A", "1" )
s.put( "B", "Two" )
s.put( "C", "3" )
s.put( "B", "2" )
s.save()
