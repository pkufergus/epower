import urllib, urllib2, json 
import cookielib
from util import *

#api = 'https://staging.epower.amadeus.com/etraveltochina/#AdtCount=1&Culture=en-US&DepartureDate=8/19/2015&From=NYC&ManualCostAmount=&ManualCostType=none&Method=Search&QFrom=C&QTo=C&ReturnDate=8/26/2015&To=BJS' 
api='https://staging.epower.amadeus.com/etraveltochina/'
data="""{"p_RQ":{"Itineraries":[{"FromValue":"NYC","AirportCityQualifierForFrom":"C","ToValue":"BJS","AirportCityQualifierForTo":"C","DepartureDate":"2015-08-19T00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""},{"ToValue":"NYC","AirportCityQualifierForTo":"C","FromValue":"BJS","AirportCityQualifierForFrom":"C","DepartureDate":"2015-08-26T00:00:00.000","DepartureTime":"00:01","FlexibleDateIndicator":""}],"FlightType":"RoundTrip","SearchPassengers":[{"PassengerType":"ADT","PassengerCount":"1"}],"FamilyDiscount":0,"FamilyCardDiscount":0,"IsCalendarSearch":0,"RefundableFlight":0,"IsMajorCabin":0,"DirectFlightsOnly":0,"CabinClass":"Y","ManualCostAmount":null,"ManualCostType":null,"PreferredAirlines":[],"SearchKey":"{Itineraries:[{FromValue:NYC,AirportCityQualifierForFrom:C,ToValue:BJS,AirportCityQualifierForTo:C,DepartureDate:2015-08-19T00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:},{ToValue:NYC,AirportCityQualifierForTo:C,FromValue:BJS,AirportCityQualifierForFrom:C,DepartureDate:2015-08-26T00:00:00.000,DepartureTime:00:01,FlexibleDateIndicator:}],FlightType:RoundTrip,SearchPassengers:[{PassengerType:ADT,PassengerCount:1}],FamilyDiscount:0,FamilyCardDiscount:0,IsCalendarSearch:0,RefundableFlight:0,IsMajorCabin:0,DirectFlightsOnly:0,CabinClass:Y,ManualCostAmount:null,ManualCostType:null,PreferredAirlines:[]}","SearchUrl":"#AdtCount=1&Culture=en-US&DepartureDate=8/19/2015&From=NYC&ManualCostAmount=&ManualCostType=none&Method=Search&QFrom=C&QTo=C&ReturnDate=8/26/2015&To=BJS"}}"""

cookie = cookielib.CookieJar()  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.addheaders=[
	('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
	('Accept-Encoding', 'gzip, deflate, sdch'),
	('Accept-Language', 'zh-CN,zh;q=0.8'),
	('Cache-Control','max-age=0'),
	('Host', 'staging.epower.amadeus.com'),
	('Connection', 'keep-alive'),
	('Referer', 'https://staging.epower.amadeus.com/etraveltochina/'),
	('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'),
    ]
response = opener.open(api)  
tid=""
print "resp=",response
for item in cookie:  
	print 'Name = '+item.name  
	print 'Value = '+item.value  
	if item.name == 'ASP.NET_SessionId' :
		sid=item.value
	if item.name == 'Ticket' :
		tid=item.value

url="https://staging.epower.amadeus.com/etraveltochina/GeneralService/GeneralInformationInit"
#AccessURL(url,"",sid, tid)

url="https://staging.epower.amadeus.com/etraveltochina/FlightService/AutoComplete"
payload="""{"startsWith":"bjs","showAllText":true}"""
AccessURL(url,payload,sid, tid)
exit(0)

url="https://staging.epower.amadeus.com/etraveltochina/FlightService/FlightRunSearch"

AccessURL(url, data,sid, tid)
exit(0)
data_dict=json.loads(data)
data = json.dumps(data_dict) 
req = urllib2.Request(url) 
req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
req.add_header('Content-Type', 'application/json; charset=UTF-8')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
#sid="jqawm1rk2i3pzo0l0qrwfk4a"
print "sid =", sid
print "tid =", tid
tid="PortalCode=etraveltochina&UserName=&ClientIP=111.202.176.55&IsB2BCSubAgencyHostAdmin=&UICustomizationRights=&FileManagerThemeAdmin=&RootFolder=&DefaultCulture=en-US&ApiUrlBase=http%3a%2f%2fstaging.epower.amadeus.com%2fNEWUI.FMGR%2fapi&PortalURL=&FileManagerConnectionStringKey=&UrlReferrer=&CultureListStr=&TimeTicket=08%2f09%2f2015+14%3a36%3a32&Hash=ujmsPniJPAOJBSc7Urinxdonq3lOLXIHD4fjSDNm%2f7s%3d"
cookie="""FakeCookie=1; ASP.NET_SessionId=%s; Ticket=%s;""" % (sid, tid)
req.add_header('Cookie', cookie)
res = urllib2.urlopen(req, data) 
print res.read() 
