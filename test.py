#!/usr/bin/env python
#coding=utf8

import httplib, urllib
import json
import urllib2

httpClient = None
try:
	data="""{"p_RQ":{"Itineraries":[{"FromValue":"NYC","AirportCityQualifierForFrom":"C","ToValue":"BJS","AirportCityQualifierForTo":"C","DepartureDate":"2015-08-10T00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""},{"ToValue":"NYC","AirportCityQualifierForTo":"C","FromValue":"BJS","AirportCityQualifierForFrom":"C","DepartureDate":"2015-08-17T00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""}],"FlightType":"RoundTrip","SearchPassengers":[{"PassengerType":"ADT","PassengerCount":"1"}],"FamilyDiscount":0,"FamilyCardDiscount":0,"IsCalendarSearch":0,"RefundableFlight":0,"IsMajorCabin":0,"DirectFlightsOnly":0,"CabinClass":"Y","ManualCostAmount":null,"ManualCostType":null,"PreferredAirlines":[],"SearchKey":"{Itineraries:[{FromValue:NYC,AirportCityQualifierForFrom:C,ToValue:BJS,AirportCityQualifierForTo:C,DepartureDate:2015-08-10T00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:},{ToValue:NYC,AirportCityQualifierForTo:C,FromValue:BJS,AirportCityQualifierForFrom:C,DepartureDate:2015-08-17T00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:}],FlightType:RoundTrip,SearchPassengers:[{PassengerType:ADT,PassengerCount:1}],FamilyDiscount:0,FamilyCardDiscount:0,IsCalendarSearch:0,RefundableFlight:0,IsMajorCabin:0,DirectFlightsOnly:0,CabinClass:Y,ManualCostAmount:null,ManualCostType:null,PreferredAirlines:[]}","SearchUrl":"#AdtCount=1&Culture=zh-CN&DepartureDate=08/10/2015&From=NYC&ManualCostAmount=&ManualCostType=none&Method=Search&QFrom=C&QTo=C&ReturnDate=08/17/2015&To=BJS"}}"""
	#params = urllib.urlencode(data)
	jdata = json.dumps(data)
	headers = {"Content-type": "application/json", "Accept": "application/json","Cookie":"FakeCookie=1; ASP.NET_SessionId=l3myqiqihgx3nt34omf04hnu; Ticket=PortalCode=traveltochina&UserName=&ClientIP=114.245.34.223&IsB2BCSubAgencyHostAdmin=&UICustomizationRights=&FileManagerThemeAdmin=&RootFolder=&DefaultCulture=en-US&ApiUrlBase=http%3a%2f%2fstaging.epower.amadeus.com%2fNEWUI.FMGR%2fapi&PortalURL=&FileManagerConnectionStringKey=&UrlReferrer=&CultureListStr=&TimeTicket=08%2f09%2f2015+10%3a46%3a58&Hash=oEKXAd1GqbrfkEhlamF%2fTNQWxz%2bm2ewy4ljTJB57kFc%3d"}

	url="https://staging.epower.amadeus.com/traveltochina/FlightService/FlightRunSearch"
	httpClient = httplib.HTTPSConnection("https://staging.epower.amadeus.com", 80, timeout=30)
	print "%s" % url
	params=data
	params=json.loads(data)
	print "%s" % params
	urlpath="/traveltochina/FlightService/FlightRunSearch"
	#headers=json.loads(headers)
	print "%s" % headers
	httpClient.request("POST", urlpath, params, headers)
	print "%s" % url

	response = httpClient.getresponse()
	#url="https://staging.epower.amadeus.com/traveltochina/FlightService/FlightRunSearch"
	#url="https://staging.epower.amadeus.com/traveltochina/#AdtCount=1&Culture=en-US&DepartureDate=08/31/2015&From=NYC&ManualCostAmount=&ManualCostType=none&Method=Search&Page=Result&QFrom=C&QTo=C&ReturnDate=09/07/2015&To=BJS"
	#value=urllib.urlencode(data)
	#print value
	#print jdata
	#req = urllib2.Request(url, "")
	#response = urllib2.urlopen(req)
	#print response.status
	#print response.reason
	print response.read()
	#print response.getheaders() #获取头信息
except Exception, e:
	print e
finally:
	if httpClient:
		httpClient.close()
