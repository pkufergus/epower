#encoding=utf-8
import urllib, urllib2, json 
import cookielib
from util import *
from Redis import * 
import sys
import datetime,time
import string
from threading import Thread
import socket 
from MysqlFuncs import *
from threadpool import ThreadPool
from work import *
from DBUtils import PooledDB
import MySQLdb

class Spider:
	f = open("res.txt", "w")
	conn = None
	maxInterval=330
	count=0

	def __init__(self, country='USA', url_type="traveltochina", limit=1, threadnum=100):
		self.host = "127.0.0.1"
		self.db_user = "root"
		self.db_passwd = getPasswd()
		self.mysqlPool = PooledDB.PooledDB(MySQLdb,100,200,100,200,True, host=self.host,user=self.db_user,passwd=self.db_passwd,db='mysql', charset='utf8') 
		self.threadnum=int(threadnum)
		self.pool = ThreadPool(self.threadnum)
		self.stat_list=[0,0,0]; #total, normal, error
		self.lock = threading.Lock()
		self.max_interval_months = 10
		self.country=country
		self.url_type=url_type
		self.redisdb = Redis(country=self.country, url_type=self.url_type)
		self.limit=int(limit)
		self.show_params()

	def show_params(self):
		print "Spider %s" % self
		print "country=%s, url_type=%s, limit=%s, threadnum=%s" % (self.country, self.url_type, self.limit, self.threadnum)


	def getMysqlDB():
		self.conn = ConnectDB(self.host, self.db_user, self.db_passwd)
		return self.conn
		
	def run(self):
		self.conn = self.mysqlPool.connection()
		cityPairs = GetCityPairs(self.conn)
		interval_days = (14, 28, 91, 182)
		now = datetime.datetime.now()
		for cp in cityPairs:
			print "%s --> %s" % (cp['DepartureCode'], cp['DestinationCode'])
			DepartCity = cp['DepartureCode']
			DestCity =  cp['DestinationCode']
			country = cp['country']
			if country != self.country :
				continue;
			DepartTime = now
			DepartTime = DepartTime + datetime.timedelta(days=2)
			interval_months = 0
			thisMonth=string.atoi(now.strftime("%m"))
			while interval_months < self.max_interval_months :
				print "Depart time=", DepartTime.strftime("%Y-%m-%d")
				ReturnTimeList = []
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=14))
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=28))
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=91))
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=182))
				dayOfWeek = datetime.datetime.now().weekday()
				# only on sunday we obtain the price of half year
				#if dayOfWeek == 0:
				#	ReturnTimeList.append(DepartTime + datetime.timedelta(days=182))
				for returnTime in ReturnTimeList:
					print "\treturn time=", returnTime.strftime("%Y-%m-%d") 
					interval_days = (returnTime - now).days
					if interval_days >= self.maxInterval:
						print "the interval to long"
						continue;
					item_url=""
					root_url=GetRootURL(country,self.url_type)
					search_url="#AdtCount=1&Culture=zh-CN&ManualCostAmount=&ManualCostType=none&Method=Search&Page=Home"
					search_url = search_url + """&From=%s&DepartureDate=%s&To=%s&ReturnDate=%s&QFrom=C&QTo=C""" % (DepartCity, DepartTime.strftime("%m/%d/%Y"), DestCity, returnTime.strftime("%m/%d/%Y"))
					item_url=root_url+search_url
					print "url = [%s]" % item_url
					#self.f.write("0=%s --> %s  \n url %s\n" % (DepartCity, DestCity, item_url))
					item = {}
					item['DepartureDate'] = DepartTime.strftime("%Y-%m-%d");
					item['ReturnDate'] = returnTime.strftime("%Y-%m-%d");
					item['DepartureCity'] = DepartCity;
					item['ArrivalCity'] = DestCity;
					item['URL'] = item_url;
					item['SearchURL'] = search_url;
					item['redisdb'] = self.redisdb;
					item['FlightURL'] = root_url+"FlightService/FlightRunSearch" 
					item['MysqlPool'] = self.mysqlPool
					item['lock'] = self.lock
					item['flag'] = 0
					self.stat_list[0]+=1
					#yield Request(url=item_url, meta={'item': item}, callback=self.parse_item)
					self.pool.add_task(do_work, self.stat_list, item)
					time.sleep(0.1)
					self.count+=1
					print "self count=%s limt=%s" % (self.count,self.limit)
					if self.count >= self.limit:
						print "self count=%s" % self.count
						break;
				
				DepartTime = DepartTime + datetime.timedelta(days=1)
				DepartMonth = string.atoi(DepartTime.strftime("%m"))
				if DepartMonth < thisMonth:
					DepartMonth += 12
				interval_months = DepartMonth - thisMonth 
				if self.count >= self.limit:
					print "self count=%s limt=%s" % (self.count,self.limit)
					break;
			if self.count >= self.limit:
				print "self count=%s limt=%s" % (self.count,self.limit)
				break;
		self.pool.destroy()
		self.outStatistic()
	
	def outStatistic(self):
		print "total num=%s, nomal num=%s, except num=%s" % (self.stat_list[0], self.stat_list[1], self.stat_list[2])

	def run_book(self):
		self.conn = self.mysqlPool.connection()
		cityPairs = GetBookCityPairs(self.conn)
		now = datetime.datetime.now()
		for cp in cityPairs:
			DepartCity = cp['leave_city']
			DestCity =  cp['dest_city']
			print "%s --> %s" % (DepartCity, DestCity)
                        country=self.country
			#if country != self.country :
			#	continue;
			DepartTime = StringToDatetime(cp['leave_date'])
                        returnTime = StringToDatetime(cp['back_date'])
                        print "Depart time=", DepartTime.strftime("%Y-%m-%d")
			print "\treturn time=", returnTime.strftime("%Y-%m-%d") 
			interval_days = (returnTime - now).days
                        print "interval days ",interval_days
			if interval_days >= self.maxInterval:
				print "the interval to long"
				continue
			interval_days = (DepartTime - now).days
                        print "interval days ",interval_days
			if interval_days <= 2 :
				print "the departtime is old"
				continue
			item_url=""
			print "root url = [%s,%s]" % (self.url_type, country)
			root_url=GetRootURL(country,self.url_type)
			print "root url = [%s]" % ('123')
			search_url="#AdtCount=1&Culture=zh-CN&ManualCostAmount=&ManualCostType=none&Method=Search&Page=Home"
			search_url = search_url + """&From=%s&DepartureDate=%s&To=%s&ReturnDate=%s&QFrom=C&QTo=C""" % (DepartCity, DepartTime.strftime("%m/%d/%Y"), DestCity, returnTime.strftime("%m/%d/%Y"))
			item_url=root_url+search_url
			print "url = [%s]" % item_url
			#self.f.write("0=%s --> %s  \n url %s\n" % (DepartCity, DestCity, item_url))
			item = {}
			item['DepartureDate'] = DepartTime.strftime("%Y-%m-%d");
			item['ReturnDate'] = returnTime.strftime("%Y-%m-%d");
			item['DepartureCity'] = DepartCity;
			item['ArrivalCity'] = DestCity;
			item['URL'] = item_url;
			item['SearchURL'] = search_url;
			item['redisdb'] = self.redisdb;
			item['FlightURL'] = root_url+"FlightService/FlightRunSearch" 
			item['MysqlPool'] = self.mysqlPool
			item['lock'] = self.lock
			item['flag'] = 0
			self.stat_list[0]+=1
			#yield Request(url=item_url, meta={'item': item}, callback=self.parse_item)
			self.pool.add_task(do_work, self.stat_list, item)
			time.sleep(0.1)
			self.count+=1
			print "self count=%s limt=%s" % (self.count,self.limit)
			if self.count >= self.limit:
				print "self count=%s" % self.count
				break;
				
		self.pool.destroy()
		self.outStatistic()
