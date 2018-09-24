from flask import render_template, redirect, request
from app import app
import sqlite3
import datetime
import time

BEDROOM = 151
BALCONY = 135
KTICHEN = 167


@app.route('/')
@app.route('/index')
def index():
    conn = sqlite3.connect('./sensor_reading/sensordata.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM sensor_data WHERE device=135 ORDER BY timestamp DESC LIMIT 1")
    balconyData = (curs.fetchall())
    curs.execute("SELECT * FROM sensor_data WHERE device=151 ORDER BY timestamp DESC LIMIT 1")
    bedroomData = (curs.fetchall())
    curs.execute("SELECT * FROM sensor_data WHERE device=167 ORDER BY timestamp DESC LIMIT 1")
    kitchenData = (curs.fetchall())

    # Max temperature
    curs.execute("SELECT max(temp) FROM sensor_data WHERE device = 135 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayBalconyTemp = (curs.fetchall())[0][0]
    curs.execute("SELECT max(temp) FROM sensor_data WHERE device = 151 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayBedroomTemp = (curs.fetchall())[0][0]
    curs.execute("SELECT max(temp) FROM sensor_data WHERE device = 167 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayKitchenTemp = (curs.fetchall())[0][0]
    maxTemperature = [maxTodayBalconyTemp, maxTodayBedroomTemp, maxTodayKitchenTemp]

    # Min temperture
    curs.execute("SELECT min(temp) FROM sensor_data WHERE device = 135 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayBalconyTemp = (curs.fetchall())[0][0]
    curs.execute("SELECT min(temp) FROM sensor_data WHERE device = 151 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayBedroomTemp = (curs.fetchall())[0][0]
    curs.execute("SELECT min(temp) FROM sensor_data WHERE device = 167 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayKitchenTemp = (curs.fetchall())[0][0]
    minTemperature = [minTodayBalconyTemp, minTodayBedroomTemp, minTodayKitchenTemp]

    # min humidity
    curs.execute("SELECT max(hum) FROM sensor_data WHERE device = 135 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayBalconyHum = (curs.fetchall())[0][0]
    curs.execute("SELECT max(hum) FROM sensor_data WHERE device = 151 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayBedroomHum = (curs.fetchall())[0][0]
    curs.execute("SELECT max(hum) FROM sensor_data WHERE device = 167 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    maxTodayKitchenHum = (curs.fetchall())[0][0]
    maxHumidity = [maxTodayBalconyHum, maxTodayBedroomHum, maxTodayKitchenHum]
    print("Max hums")
    print(maxHumidity)

    # Min humidity
    curs.execute("SELECT min(hum) FROM sensor_data WHERE device = 135 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayBalconyHum = (curs.fetchall())[0][0]
    curs.execute("SELECT min(hum) FROM sensor_data WHERE device = 151 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayBedroomHum = (curs.fetchall())[0][0]
    curs.execute("SELECT min(hum) FROM sensor_data WHERE device = 167 AND timestamp BETWEEN date(datetime('now')) AND date(datetime('now','+1 day','-0.001 second'))")
    minTodayKitchenHum = (curs.fetchall())[0][0]
    minHumidity = [minTodayBalconyHum, minTodayBedroomHum, minTodayKitchenHum]
    print("Min hims")
    print(minHumidity)
    conn.close()
    return render_template('index.html', title='Home', balcony_hum=balconyData[0][2], balcony_temp=balconyData[0][1],
        bedroom_hum=bedroomData[0][2], bedroom_temp=bedroomData[0][1], kitchen_hum=kitchenData[0][2], kitchen_temp=kitchenData[0][1],
        max_temps= maxTemperature, min_temps=minTemperature, max_hums=maxHumidity, min_hums= minHumidity)

@app.route("/chart", methods=['GET', 'POST'])
def chart():
    balconyTempList = []
    balconyTimeList = []
    kitchenTempList = []
    kitchenTimeList = []
    bedroomTempList = []
    bedroomTimeList = []
    balconyData = []
    kitchenData = []
    bedroomData = []
    legend = 'Monthly Data'

    # setup db connection
    conn = sqlite3.connect('./sensor_reading/sensordata.db')
    curs = conn.cursor()

    balcony_select_string = ''
    kitchen_select_string = ''
    bedroom_select_string = ''
    if request.method == 'POST':
        if "1 hours" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-1 Hour')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-1 Hour')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-1 Hour')"
        elif "2 hours" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-2 Hour')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-2 Hour')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-2 Hour')"
        elif "4 hours" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-4 Hour')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-4 Hour')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-4 Hour')"
        elif "All" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151"
        else:
            print("Unknown filed pushed")
    else:
        balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-24 Hour')"
        kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-24 Hour')"
        bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-24 Hour')"

    # DB call
    conn = sqlite3.connect('./sensor_reading/sensordata.db')
    curs = conn.cursor()
    curs.execute(balcony_select_string)
    balconyData = (curs.fetchall())
    curs.execute(kitchen_select_string)
    kitchenData = (curs.fetchall())
    curs.execute(bedroom_select_string)
    bedroomData = (curs.fetchall())
    conn.close()

    # Parse data to fit template
    for data in balconyData:
        balconyTempList.append(data[1])
        balconyTimeList.append(data[0])
    for data in kitchenData:
        kitchenTempList.append(data[1])
        kitchenTimeList.append(data[0])
    for data in bedroomData:
        bedroomTempList.append(data[1])
        bedroomTimeList.append(data[0])
    return render_template('chart.html', balconyValues=balconyTempList, balconyLabels=balconyTimeList,
        kitchenValues=kitchenTempList, kitchenLabels=kitchenTimeList,
        bedroomValues=bedroomTempList, bedroomLabels=bedroomTimeList, legend=legend)
