#encoding=utf-8
import urllib, urllib2, json 
import cookielib
from util import *
from Redis import * 
import sys
from threading import Thread
import getopt

def Run(argv):
	try:
		opts, args = getopt.getopt(argv[1:], 'vm:', ['prefix=', 'mode=', 'culture='])
	except getopt.GetoptError, err:
		print str(err)
		print "parameter error"
		sys.exit(2)
	
	if len(opts) < 1:
		print "parameter numbers error [%s]" % len(opts)
		sys.exit(2)
	
	prefix=""
	mode=""
	culture="zh-CN"
	for option, arg in opts:
		if option in ('--prefix'):
			prefix = arg 
		elif option in ('--mode'):
			mode = arg 
		elif option in ('--culture'):
			culture = arg 
		else :
			print 'unhandled option'
	  		sys.exit(3)

	country="USA"
	url_type="etraveltochina"
	print "prefix=%s, mode=%s, culture=%s" % (prefix, mode, culture)
	redisdb=Redis(country=country, url_type=url_type, culture=culture)

	ret=""
	if mode == "airline" :
		ret = redisdb.completeAirline(prefix)
	elif mode == "city" :
		ret = redisdb.complete(prefix)
	else :
		ret = redisdb.complete(prefix)
	print "result=%s" % ret

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	Run(sys.argv)
