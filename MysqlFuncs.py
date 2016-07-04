import sys
import MySQLdb as mysql
import datetime,time

def ConnectDB(host, user, passwd):
	return mysql.connect(host=host, db='mysql', user=user, passwd=passwd, charset="utf8")

def GetCityPairs(conn, src_db="aie_v2"):
	c = conn.cursor(mysql.cursors.DictCursor)
	sql = """ select DepartureCode, DestinationCode, country
		from %s.aie_citypair
		where Undone='TRUE' """ % (src_db)
	print "sql = [%s]" % sql
	c.execute(sql)
	return c.fetchall()

def GetBookCityPairs(conn, src_db="aie_v2"):
	c = conn.cursor(mysql.cursors.DictCursor)
	sql = """ select leave_date, back_date, leave_city,dest_city 
		from %s.mail_order
		""" % (src_db)
	print "sql = [%s]" % sql
	c.execute(sql)
	return c.fetchall()

def getPasswd():
	return "root"

def updatePrice(conn, DepartCity, DestCity, DepartDay, returnDay, datasource, URL):
	c = conn.cursor(mysql.cursors.DictCursor)
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	sql = """ replace into aie_v2.aie_masterdata
		(DepartureDate, ReturnDate, DepartureCity, ArrivalCity, Price, Stops, AirlineCode,AirlineName,  WebLink, Undone, updated, UpdatedDate) 
		values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s')
		""" % (DepartDay, returnDay, DepartCity, DestCity, datasource, '0', '0', '0', URL, 'TRUE', '1', now)
	print "sql = [%s]" % sql
	c.execute(sql)
	conn.commit()

