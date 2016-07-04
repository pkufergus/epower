# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
import sys
import datetime,time
import string
from crawler.items import CrawlerItem

from MysqlFuncs import *

class DmozSpider(scrapy.spider.Spider):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	name = "dmoz"
	start_urls = [
	"http://127.0.0.1"
	]
	f = open("res.txt", "w")
	host = "mysql.travel.com"
	db_user = "root"
	db_passwd = "root"
	conn = None

	def __init__(self):
		scrapy.spider.Spider.__init__(self)
		self.db_passwd = getPasswd()

	def parse(self, response):
		self.conn = ConnectDB(self.host, self.db_user, self.db_passwd)
		cityPairs = GetCityPairs(self.conn)
		interval_days = (14, 28, 91, 182)
		now = datetime.datetime.now()
		for cp in cityPairs:
			print "%s --> %s" % (cp['DepartureCode'], cp['DestinationCode'])
			DepartCity = cp['DepartureCode']
			DestCity =  cp['DestinationCode']
			country = cp['country']
			DepartTime = now
			interval_months = 0
			thisMonth=string.atoi(now.strftime("%m"))
			while interval_months < 11 :
				print "Depart time=", DepartTime.strftime("%Y-%m-%d")
				ReturnTimeList = []
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=14))
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=28))
				ReturnTimeList.append(DepartTime + datetime.timedelta(days=91))
				dayOfWeek = datetime.datetime.now().weekday()
				# only on sunday we obtain the price of half year
				if dayOfWeek == 0:
					ReturnTimeList.append(DepartTime + datetime.timedelta(days=182))
				for returnTime in ReturnTimeList:
					print "\treturn time=", returnTime.strftime("%Y-%m-%d") 
					interval_days = (returnTime - now).days
					if interval_days >= 330:
						print "the interval to long"
						continue;
					item_url=""
					if country == "CA" :
						item_url="""http://wftc1.e-travel.com/AIEADRHADRH/TravelShopperAvailability.action?&SITE=ADRHADRH&LANGUAGE=US"""
					else :
						item_url="""http://wftc1.e-travel.com/AIEADBLADBL/TravelShopperAvailability.action?&SITE=ADBLADBL&LANGUAGE=US"""
					item_url = item_url + """&TRIPFLOW=YES&TRIP_TYPE=R&B_LOCATION_1=%s&B_ANY_TIME_1=TRUE&E_LOCATION_1=%s&B_ANY_TIME_2=TRUE&CABIN=E&TRAVELLER_TYPE_1=ADT&WORKFLOW_NAME=RGSIMPLE&PRODUCT_TYPE_1=STANDARD_AIR&B_DATE_1=%s&B_DATE_2=%s""" % (DepartCity, DestCity, DepartTime.strftime("%Y%m%d0000"), returnTime.strftime("%Y%m%d0000"))
					print "url = [%s]" % item_url
					#self.f.write("0=%s --> %s  \n url %s\n" % (DepartCity, DestCity, item_url))
					item = CrawlerItem()
					item['DepartureDate'] = DepartTime.strftime("%Y-%m-%d");
					item['ReturnDate'] = returnTime.strftime("%Y-%m-%d");
					item['DepartureCity'] = DepartCity;
					item['ArrivalCity'] = DestCity;
					item['URL'] = item_url;
					yield Request(url=item_url, meta={'item': item}, callback=self.parse_item)
				
				DepartTime = DepartTime + datetime.timedelta(days=1)
				DepartMonth = string.atoi(DepartTime.strftime("%m"))
				if DepartMonth < thisMonth:
					DepartMonth += 12
				interval_months = DepartMonth - thisMonth 

			

		#yield Request(url=item_url, callback=self.parse_item)
	
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		item = response.meta['item']
		DepartDay = item['DepartureDate']
		returnDay = item['ReturnDate']
		DepartCity = item['DepartureCity']
		DestCity = item['ArrivalCity']
		URL = item['URL']
		sites = hxs.select('//script/text()').extract()
		datasource=""
		pos = -1;
		isFound = 0
		for site in sites:
			pos = site.find("generatedJSon = new String")
			if pos >= 0 : 
				datasource = site[pos:]
				isFound = 1
				break;
		if isFound == 0:
			return
		datasource = datasource.split("generatedJSon = new String")[1]
		datasource = datasource.expandtabs()
		datasource = datasource.split(",")[0]
		datasource = datasource.split(":")[-1]
		self.f.write("0=%s --> %s on %s --> %s\n" % (DepartCity, DestCity, DepartDay, returnDay))
		self.f.write("2=%s\n" % datasource)
		updatePrice(self.conn, DepartCity, DestCity, DepartDay, returnDay, datasource, URL)

