import sqlite3
import datetime
import time
from tellcore.telldus import TelldusCore
from enum import Enum

BEDROOM = 151
BALCONY = 135
KTICHEN = 167
offset_bedroom = 0.5

core = TelldusCore()
conn = sqlite3.connect('sensordata.db')
curs = conn.cursor()

while (True):
	list_sensors = core.sensors()
	print(len(list_sensors))
	if list_sensors is not None:
		for sens in list_sensors:
			dev_id = sens.id
			temp = sens.value(1).value
			hum = sens.value(2).value
			if dev_id == BEDROOM:
				curs.execute("INSERT INTO sensor_data VALUES (datetime('now'), ?, ?,?)", (float(temp) + offset_bedroom, hum, dev_id))
				print("Added reading for bedroom, dev_id: {} temp: {}, hum: {}".format(dev_id, hum, float(temp) + offset_bedroom))
			elif dev_id == BALCONY:
				curs.execute("INSERT INTO sensor_data VALUES (datetime('now'), ?, ?,?)", (temp, hum,dev_id))
				print("Added reading for balcony, dev_id: {}, temp: {}, hum: {}".format(dev_id, hum,temp))
			elif dev_id == KTICHEN:
				curs.execute("INSERT INTO sensor_data VALUES (datetime('now'), ?, ?,?)", (temp, hum,dev_id))
				print("Added reading for kitchen, dev_id: {}, temp: {}, hum: {}".format(dev_id, hum,temp))
			else:
				print("Uknown device id: {}".format(dev_id))
	conn.commit()
	print("New data detected")
	time.sleep(60)



conn.close()






