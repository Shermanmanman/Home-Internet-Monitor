#!/usr/bin/env python3

import speedtest as st
from datetime import datetime
import mysql.connector
import json

# Getting speed test results, specifically server name, ping, download, upload
def get_new_speeds():
    s = st.Speedtest()
    srvr = s.get_best_server()
    ping = s.results.ping
    download = s.download()
    upload = s.upload()
    
    # converts the download and upload to Mbps
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)
    
    # grabs the date and formats it to datetime datatype for MySQL
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # fun conversion that shouldn't have to happen. converts the server being tested against from a JSON array(?)
    # to a JSON object, then using the JSON object I can pull what I need which is the name of the server (city, really).
    js_st = json.dumps(srvr, indent = 4)
    js = json.loads(js_st)
    srv = js["name"]
    url = js["host"]
    lat = js["lat"]
    lon = js["lon"]
    
    yield srv,url,ping,download_mbs,upload_mbs,lat,lon,date

# Query to insert the collected data to MySQL
def dbUpdate(cnx,srv,url,ping,download_mbs,upload_mbs,lat,lon,date):
    cursor = cnx.cursor()
    insert = """INSERT INTO results(server,url,dl,ul,ping,lat,lon,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    values = (srv,url,download_mbs,upload_mbs,ping,lat,lon,date)
    cursor.execute(insert, values)
    cursor.close()

# Metric cleanup, retaining no more than 30 days in backend DB
def dbCleanup(cnx):
    cursor2 = cnx.cursor()
    cleanup = """DELETE FROM results WHERE timestamp < now() - interval 30 DAY """
    cursor2.execute(cleanup)
    cursor2.close()

# MySQL connection string and for loop to call the definitions and add the data to the database
cnx = mysql.connector.connect(option_files='/etc/mysql/.metric.cnf')
for srv,url,ping,download_mbs,upload_mbs,lat,lon,date in get_new_speeds():
    q1 = dbUpdate(cnx,srv,url,ping,download_mbs,upload_mbs,lat,lon,date)
    q2 = dbCleanup(cnx)
cnx.commit()
cnx.close()
