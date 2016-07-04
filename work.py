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
from DBUtils import PooledDB

def do_work(args, kwds):
	item = kwds
	DepartDay = item['DepartureDate']
	ReturnDay = item['ReturnDate']
	DepartCity = item['DepartureCity']
	DestCity = item['ArrivalCity']
	URL = item['URL']
	SearchURL=item['SearchURL']
	redisdb=item['redisdb']
	FlightURL=item['FlightURL']
	mysqlPool = item['MysqlPool']
	flag = item['flag']
	stat_list=args
	lock=item['lock']
	conn=mysqlPool.connection()
	f=open("res.txt", "a")
	code=201
	try:
		payload=create_payload(DepartCity, DestCity, DepartDay, ReturnDay, SearchURL)
		(sid, tid) = redisdb.getSession()
		(code, res) = AccessURL(FlightURL, payload, sid, tid)
		code=str(code).strip()
		retry_c = 0
		while int(code) != 200 and retry_c<10:
			print "retry error code =",code
			time.sleep(10)
			(sid, tid) = redisdb.getSession()
			(code, res) = AccessURL(FlightURL, payload, sid, tid)
			code=str(code).strip()
			retry_c+=1
			print "retry count =",retry_c
		if int(code) != 200 :
			print "access url error code=",code
		price = parse_respone(res)
		if price != None and price > 0 and int(code) == 200:
			updatePrice(conn, DepartCity, DestCity, DepartDay, ReturnDay, price, URL)
			f.write("0=%s --> %s on %s --> %s price %s [%s]\n" % (DepartCity, DestCity, DepartDay, ReturnDay, price, URL))
			lock.acquire()
			stat_list[1]+=1
			lock.release()
		else:
			print "parse error, code=",code
			raise NameError
	except Exception, exception:
		print "get price error = %s" % exception
		f.write("%s=%s --> %s on %s --> %s price %s [%s] \n" % (code, DepartCity, DestCity, DepartDay, ReturnDay, -1, URL))
		stat_list[2]+=1

def parse_respone(respone):
	if respone == None and respone == "" :
		return 0
	
	data_dict=json.loads(respone)
	recs=data_dict['Recs']
	#print "Recs=", recs
	price=recs[0]['AvaragePricePerPerson']
	#print "price=", price
	return price

def create_payload(DepartCity, DestCity, DepartDay, ReturnDay, SearchURL):
	payload="""{"p_RQ":{"Itineraries":[{"FromValue":"%s","AirportCityQualifierForFrom":"C","ToValue":"%s","AirportCityQualifierForTo":"C","DepartureDate":"%sT00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""},{"ToValue":"%s","AirportCityQualifierForTo":"C","FromValue":"%s","AirportCityQualifierForFrom":"C","DepartureDate":"%sT00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""}],"FlightType":"RoundTrip","SearchPassengers":[{"PassengerType":"ADT","PassengerCount":"1"}],"FamilyDiscount":0,"FamilyCardDiscount":0,"IsCalendarSearch":0,"RefundableFlight":0,"IsMajorCabin":0,"DirectFlightsOnly":0,"CabinClass":"Y","ManualCostAmount":null,"ManualCostType":null,"PreferredAirlines":[],""" % (DepartCity, DestCity, DepartDay, DepartCity, DestCity, ReturnDay)
	payload=payload + """"SearchKey":"{Itineraries:[{FromValue:%s,AirportCityQualifierForFrom:C,ToValue:%s,AirportCityQualifierForTo:C,DepartureDate:%sT00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:},{ToValue:%s,AirportCityQualifierForTo:C,FromValue:%s,AirportCityQualifierForFrom:C,DepartureDate:%sT00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:}],FlightType:RoundTrip,SearchPassengers:[{PassengerType:ADT,PassengerCount:1}],FamilyDiscount:0,FamilyCardDiscount:0,IsCalendarSearch:0,RefundableFlight:0,IsMajorCabin:0,DirectFlightsOnly:0,CabinClass:Y,ManualCostAmount:null,ManualCostType:null,PreferredAirlines:[]}","SearchUrl":"%s"}}""" % (DepartCity, DestCity, DepartDay, DepartCity, DestCity, ReturnDay, SearchURL)
	return payload
