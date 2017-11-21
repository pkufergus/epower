import urllib, urllib2, json 
import cookielib
import datetime,time
import types

def GetRootURL(country="USA", url_type="traveltochina"):
	api = "https://www-amer.epower.amadeus.com/traveltochina/"
        print 'api',api
	if country == "CA" :
		api = "https://www-amer.epower.amadeus.com/"+url_type+"/" 
	else :
		api = "https://www-amer.epower.amadeus.com/"+url_type+"/"
	return api;

def GetCookieSession(country="USA", url_type="traveltochina", culture="zh-CN"):
	root_url=GetRootURL(country, url_type)
	api=root_url+"#Culture=%s" % culture
	print "api=%s" % api
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	opener.addheaders=[
	('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
	('Accept-Encoding', 'gzip, deflate, sdch'),
	('Accept-Language', 'zh-CN,zh;q=0.8'),
	('Cache-Control','max-age=0'),
	('Connection', 'keep-alive'),
	('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'),
    ]
	response = opener.open(api)  
	sid=""
	tid=""
	print "resp=",response
	for item in cookie:  
		print 'Name = '+item.name  
		print 'Value = '+item.value  
		if item.name == 'ASP.NET_SessionId' :
			sid=item.value
		if item.name == 'Ticket' :
			tid=item.value
	url=root_url+"GeneralService/GeneralInformationInit"
	AccessURL(url,"",sid, tid)
	url=root_url+"GeneralService/ChangeCulture"
	payload="""{"Culture":"%s"}""" % (culture)
	AccessURL(url,payload,sid, tid)
	return (sid, tid)

def AccessURL(url, payload, sid, tid):
	print "access url=[%s] sid=[%s] tid=[%s]" % (url, sid, tid)
	if payload != None and payload != "" :
		data_dict=json.loads(payload)
		data = json.dumps(data_dict) 
	else : 
		data = ""
	req = urllib2.Request(url) 
	req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
	req.add_header('Content-Type', 'application/json; charset=UTF-8')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	print "sid =", sid
	print "tid =", tid
	#tid="PortalCode=traveltochina&UserName=&ClientIP=111.202.176.55&IsB2BCSubAgencyHostAdmin=&UICustomizationRights=&FileManagerThemeAdmin=&RootFolder=&DefaultCulture=en-US&ApiUrlBase=http%3a%2f%2fstaging.epower.amadeus.com%2fNEWUI.FMGR%2fapi&PortalURL=&FileManagerConnectionStringKey=&UrlReferrer=&CultureListStr=&TimeTicket=08%2f09%2f2015+14%3a36%3a32&Hash=ujmsPniJPAOJBSc7Urinxdonq3lOLXIHD4fjSDNm%2f7s%3d"
	#tid="PortalCode=traveltochina&UserName=&ClientIP=222.129.49.83&IsB2BCSubAgencyHostAdmin=&UICustomizationRights=&FileManagerThemeAdmin=&RootFolder=&DefaultCulture=zh-CN&ApiUrlBase=http%3a%2f%2fwww.epower.amadeus.com%2fNEWUI.FMGR%2fapi&PortalURL=&FileManagerConnectionStringKey=&UrlReferrer=&CultureListStr=&TimeTicket=08%2f12%2f2015+15%3a45%3a58&Hash=5V%2f56ZJ0WZ1bxpCVpRjpHb1ftgGQgdI6XO62snYzrIY%3d"
	cookie="""FakeCookie=1; ASP.NET_SessionId=%s; Ticket=%s;""" % (sid, tid)
	req.add_header('Cookie', cookie)
	ret=""
	res_code=200
	try:
		res = urllib2.urlopen(req, data,timeout=600) 
		res_code = res.getcode()
		print "first respone code=",res_code
		ret = res.read()
	except  urllib2.HTTPError, e:
		print "error code=", e.code
		print "error %s" % e
		res_code=e.code
		return (res_code, ret)
	print "ret="
	print ret[-1000:-1]
	print "ret full="
	#print ret
	return (res_code, ret)

def AutoComplete(prefix,sid, tid):
	url=GetRootURL()+"FlightService/AutoComplete/"
	payload="""{"startsWith":"%s","showAllText":true}""" % (prefix)
	(code, content) =  AccessURL(url,payload,sid, tid)
	return content

def AutoCompleteAirline(prefix,sid, tid):
	url=GetRootURL()+"FlightService/AutoCompleteAirline"
	payload="""{"startsWith":"%s"}""" % (prefix)
	(code, content) =  AccessURL(url,payload,sid, tid)
	return content

def StringToDatetime(date_str):
        if type(date_str) is types.StringType: 
                return datetime.datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S')
        else:
                return date_str
