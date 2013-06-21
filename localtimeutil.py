def local8601():
	import datetime
	import time
	import dateutil.tz
	localtz = dateutil.tz.tzlocal()
	return datetime.datetime.fromtimestamp(time.time(),localtz).isoformat()
