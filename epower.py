#encoding=utf-8
import urllib, urllib2, json 
import cookielib
from util import *
from Redis import * 
import sys
from threading import Thread
import socket 
from MysqlFuncs import *
from Spider import *
import getopt

def thread_run(num, redisdb, url, data):
	print "num = %s start ..." % num
	(sid, tid) = redisdb.getSession()
	print "sid=[%s] tid=[%s]" % (sid, tid)
	AccessURL(url, data,sid, tid)
	print "thread num=[%s] end" % num

def Run(argv):
	start = time.time()
	print "==========begin to crawl[%s]==================================" % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
	try:
		opts, args = getopt.getopt(argv[1:], 'vm:', ['country=', 'platform=', 'limit=', 'threadnum=', 'type='])
	except getopt.GetoptError, err:
		print str(err)
		print "parameter error"
		sys.exit(2)
	
	if len(opts) < 2:
		print "parameter numbers error [%s]" % len(opts)
		sys.exit(2)
	
	country="USA"
	url_type="traveltochina"
	limit=10000
	threadnum=100
        run_type='normal'
	for option, arg in opts:
		if option in ('--country'):
			country = arg 
		elif option in ('--platform'):
			url_type = arg 
		elif option in ('--limit'):
			limit = arg 
		elif option in ('--threadnum'):
			threadnum = arg 
		elif option in ('--type'):
                        run_type=arg
		else :
			print 'unhandled option'
	  		sys.exit(3)

	print "country=%s, url_type=%s, limit=%s, threadnum=%s" % (country, url_type, limit, threadnum) 
	spider = Spider(country=country, url_type=url_type, limit=limit, threadnum=threadnum)
        if run_type == 'normal':
                spider.run()
        else:
                spider.run_book()
	end = time.time()
	elapse = end - start
	print "=========end crawl[%s],elapse[%s]============================" % ((time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), elapse)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	socket.setdefaulttimeout(600) 
	Run(sys.argv)
