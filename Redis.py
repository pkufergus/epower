import redis
import time
import random
import string
from threading import Thread
import threading

from util import *

class Redis:
	def __init__(self, host='localhost', port=6379, country='USA', url_type="etraveltochina", culture="zh-CN"):
		self.host = host
		self.port = port
		self.r =  redis.StrictRedis(self.host,self.port)
		self.country=country
		self.url_type=url_type
		self.culture=culture
		self.prefix = self.country+":"+self.url_type +":"+self.culture+":"
		self.session_num=100
		self.timeout=300
		self.lock = threading.Lock()
		self.airline_prefix="airline:"

	def assertRedis(self):
		if self.r == None :
			self.r =  redis.StrictRedis(self.host,self.port)

	def getValue(self, key):
		try:
			self.assertRedis()
			if self.r.exists(key):
				return self.r.get(key)
			return ""
		except Exception, exception:
			print exception


	def getSession(self):
		i = random.randint(0,self.session_num-1)
		print "i=%s" % i
		key=self.prefix + ("%s" % i)
		print "key=%s" % key
		self.assertRedis()

		if self.r.exists(key):
			dict_str = self.r.get(key)
			dict = eval(dict_str)
			sid=dict['sid']
			tid=dict['tid']
			return (sid, tid)
		print "retry get sid tid"
		time.sleep(0.5)
		sid=""
		tid=""
		(sid, tid) = GetCookieSession(self.country,self.url_type,self.culture)
		dict={}
		dict['sid']=sid
		dict['tid']=tid
		self.r.set(key, str(dict))
		self.r.expire(key, self.timeout)
		return (sid, tid)

	def complete(self, prefix):
		if self.r.exists(prefix):
			return self.r.get(prefix)
			
		(sid,tid)=self.getSession()
		content=AutoComplete(prefix,sid, tid)
		self.r.set(prefix,content)
		self.r.expire(prefix, 8640000) 
		return content

	def completeAirline(self, prefix):
		inner_prefix=self.airline_prefix+prefix
		if self.r.exists(inner_prefix):
			return self.r.get(inner_prefix)
			
		(sid,tid)=self.getSession()
		content=AutoCompleteAirline(prefix,sid, tid)
		self.r.set(inner_prefix,content)
		self.r.expire(inner_prefix, 8640000) 
		return content

if __name__ == '__main__':
	rdb = Redis()
	(sid,tid)=rdb.getSession()
	print "sid=%s tid=%s" % (sid, tid)
	(sid,tid)=rdb.getSession()
	print "sid=%s tid=%s" % (sid, tid)
	(sid,tid)=rdb.getSession()
	print "sid=%s tid=%s" % (sid, tid)
	(sid,tid)=rdb.getSession()
	print "sid=%s tid=%s" % (sid, tid)
