#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from env import calendar_id,calendar_url

###DB
from db_utils import db_connect
mycursor = db_connect.cursor()


games_sql_table = """
CREATE TABLE IF NOT EXISTS games (
    id CHAR(50) NOT NULL,
    competition text NOT NULL,
    teama text NOT NULL,
    teamb text NOT NULL,
    date text NOT NULL,
    PRIMARY KEY (id)
	)
    """
#Create table if not exists
mycursor.execute(games_sql_table)


#soccerway.com requires headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
URL = calendar_url #URL to fetch Maccabi Haifa games
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(class_="table-container redesign")
#print(results.prettify()) for debugging

job_elements = results.find_all("tr") #Each game is tr

#Add only games which not exists - by id
mySql_insert_query = """INSERT IGNORE INTO games (id, competition, teama, teamb, date,calendarid)
                                VALUES (%s, %s, %s, %s, %s,"false") """


for element in job_elements:
    competition = element.find("td", class_="competition")
    competition = str(competition)
    competition = ' '.join(BeautifulSoup(competition, "html.parser").stripped_strings)
    
    #Ignore if not a game
    if "None" in competition:
        continue

    teama = element.find("td", class_="team-a")
    teama= str(teama)
    teama = ' '.join(BeautifulSoup(teama, "html.parser").stripped_strings)

    teamb = element.find("td", class_="team-b")
    teamb= str(teamb)
    teamb = ' '.join(BeautifulSoup(teamb, "html.parser").stripped_strings)

    date = element.find("span", class_="timestamp")
    date = str(date)
    start = 'data-value="'
    end = '">'
    date = (date.split(start))[1].split(end)[0]

    id = str(element)
    start = 'data-event-id="'
    end = '" data-expand='
    id = (id.split(start))[1].split(end)[0]

    record = (id, competition, teama, teamb, date)
    mycursor.execute(mySql_insert_query, record)
#Add changes to DB
db_connect.commit()


#print Database
# sql = "SELECT * FROM games"
# mycursor.execute(sql)
# results = mycursor.fetchall()
#Print Table
# for row in results:
#     print("Id = ", row[0], )
#     print("competition = ", row[1])
#     print("teama  = ", row[2])
#     print("teamb  = ", row[3])
#     print("date  = ", row[4], "\n")


#find games which not commited to DB
sql = "SELECT * FROM games WHERE calendarid='false'"
mycursor.execute(sql)
results = mycursor.fetchall()


###For calendar
from gcsa.google_calendar import GoogleCalendar
from gcsa.serializers.event_serializer import EventSerializer
calendar = GoogleCalendar(calendar_id,credentials_path='credentials.json')
from gcsa.event import Event
from datetime import datetime
from beautiful_date import minutes
# for event in calendar:
#     print(event)


#Print Table
for row in results:
    id = row[0]
    competition = row[1]
    teama  = row[2]
    teamb  = row[3]
    date  = int(row[4])
    # print("Id = ", row[0], )
    # print("competition = ", row[1])
    # print("teama  = ", row[2])
    # print("teamb  = ", row[3])
    # print("date  = ", row[4], "\n")


    event = Event(teama +" vs "+ teamb,
                start=datetime.fromtimestamp(date),
                end=datetime.fromtimestamp(date) + 105 * minutes)

    add_event=calendar.add_event(event)
    # print(EventSerializer.to_json(add_event)['id'])
    mySql_update_query = """UPDATE games SET calendarid=\'true\' WHERE id = %s"""
    mycursor.execute(mySql_update_query, (id,))
    db_connect.commit()


#Close connection to db if still active
if db_connect.is_connected():
  mycursor.close()
  db_connect.close()
  #print("MySQL connection is closed")
