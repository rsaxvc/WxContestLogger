import os

configdir = os.path.expanduser("~")+"/.wxlogger/"
dbdir = configdir

if not os.path.exists(configdir):
	os.makedirs(configdir)

if not os.path.exists(dbdir):
	os.makedirs(dbdir)
