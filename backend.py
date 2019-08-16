import requests as req
import bs4
import sqlite3

def qotd():
	res = req.get("https://www.brainyquote.com/quote_of_the_day.html")
	soup = bs4.BeautifulSoup(res.text,'lxml')
	quote = soup.find('img',{"class":"p-qotd"})['alt']
	return quote

def city():
	res = req.get("https://ipinfo.io/")
	data = res.json()
	city_name = data['city']
	return city_name

def temp():
	res = req.get("https://ipinfo.io/")
	data = res.json()
	city = data['city']
	api_address="http://api.openweathermap.org/data/2.5/weather?units=metric&q="+city+"&appid=4696af6bd32e24c5282995d2a7aa12d7"
	res1=req.get(api_address)
	wdata=res1.json()
	if 'city not found' in wdata.values():
		return "Temperature for your city is not available.\nSorry for the Inconvenience."
	else:
		t=wdata['main']
		temperature=t['temp']
		return temperature

def connect():
	conn=sqlite3.connect("students.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS student (rno TEXT PRIMARY KEY, name TEXT)")
	conn.commit()
	conn.close()

def insert(rno, name):
	conn=sqlite3.connect("students.db")
	cur=conn.cursor()
	cur.execute("INSERT INTO student VALUES (?,?)",(rno, name))
	conn.commit()
	conn.close()

def view():
	conn=sqlite3.connect("students.db")
	cur=conn.cursor()
	cur.execute("SELECT * FROM student")
	rows=cur.fetchall()
	conn.close()
	return rows

def delete(rno):
	conn=sqlite3.connect("students.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM student WHERE rno=?",(rno,))
	conn.commit()
	conn.close()

def update(rno, name):
	conn=sqlite3.connect("students.db")
	cur=conn.cursor()
	cur.execute("UPDATE student SET name=? WHERE rno=?",(name, rno))
	conn.commit()
	conn.close()


connect()