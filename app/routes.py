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
    balconyHumList = []
    balconyTimeList = []
    kitchenTempList = []
    kitchenHumList = []
    kitchenTimeList = []
    bedroomTempList = []
    bedroomHumList = []
    bedroomTimeList = []
    balconyData = []
    kitchenData = []
    bedroomData = []
    legend = 'Monthly Data'
    stepSize = 1

    # setup db connection
    conn = sqlite3.connect('./sensor_reading/sensordata.db')
    curs = conn.cursor()

    balcony_select_string = ''
    kitchen_select_string = ''
    bedroom_select_string = ''
    if request.method == 'POST':
        if "1 day" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-1 Day')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-1 Day')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-1 Day')"
            stepSize = 1
        elif "2 days" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-2 Days')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-2 Days')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-2 Days')"
            stepSize = 2
        elif "4 days" in request.form['time']:
            balcony_select_string = "SELECT * FROM sensor_data WHERE device=135 AND datetime(timestamp) >=datetime('now', '-4 Days')"
            kitchen_select_string = "SELECT * FROM sensor_data WHERE device=167 AND datetime(timestamp) >=datetime('now', '-4 Days')"
            bedroom_select_string = "SELECT * FROM sensor_data WHERE device=151 AND datetime(timestamp) >=datetime('now', '-4 Days')"
            stepSize = 4
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
        balconyTimeList.append(data[0])
        balconyTempList.append(data[1])
        balconyHumList.append(data[2])
    for data in kitchenData:
        kitchenTimeList.append(data[0])
        kitchenTempList.append(data[1])
        kitchenHumList.append(data[2])
    for data in bedroomData:
        bedroomTimeList.append(data[0])
        bedroomTempList.append(data[1])
        bedroomHumList.append(data[2])
    return render_template('chart.html', balconyTempValues=balconyTempList,balconyHumValues=balconyHumList, balconyLabels=balconyTimeList,
        kitchenTempValues=kitchenTempList,kitchenHumValues = kitchenHumList, kitchenLabels=kitchenTimeList,
        bedroomTempValues=bedroomTempList, bedroomHumValues = bedroomHumList, bedroomLabels=bedroomTimeList, stepSize = stepSize,
        legend=legend)
