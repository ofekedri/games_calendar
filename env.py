#!/usr/bin/python3
import os
#DB
dbhost=os.getenv("DATABASE_HOST")
dbuser=os.getenv("DATABASE_USER")
dbpassword=os.getenv("DATABASE_PASSWORD")
database=os.getenv("DATABASE_NAME")
calendar_id=os.getenv("calendar_id")
calendar_url=os.getenv("calendar_url")