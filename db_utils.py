#!/usr/bin/python3
import os
import mysql.connector
from env import dbhost,dbuser,dbpassword,database

db_connect = mysql.connector.connect(
  host=dbhost,
  user=dbuser,
  password=dbpassword,
  database=database
)

mycursor = db_connect.cursor()




