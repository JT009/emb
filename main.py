from flask import Flask, render_template
from sensor import Sensor
import threading
import time
import datetime
import sys

app = Flask(__name__)

list_temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
list_humi = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

set_humidity = 60

@app.route("/", methods=['POST'])
def test():
	global set_humidity
	set_humidity = int(request.form['data'])

	return "success"

@app.route("/")
def root():
	"""
	client accesses root url
	:return: index.html
	"""
	global list_temp, list_humi	

	data_temp= [('-23h', list_temp[0]), ('-22h', list_temp[1]), ('-21h', list_temp[2]), ('-20h', list_temp[3]), ('-19h', list_temp[4]), ('-18h', list_temp[5]), ('-17h', list_temp[6]), ('-16h', list_temp[7]), ('-15h', list_temp[8]), ('-14h', list_temp[9]), ('-13h', list_temp[10]), ('-12h', list_temp[11]), ('-11h', list_temp[12]), ('-10h', list_temp[13]), ('-9h', list_temp[14]), ('-8h', list_temp[15]), ('-7h', list_temp[16]), ('-6h', list_temp[17]), ('-5h', list_temp[18]), ('-4h', list_temp[19]), ('-3h', list_temp[20]), ('-2h', list_temp[21]), ('-1h', list_temp[22]), ('-0h', list_temp[23])]

	data_humi= [('-23h', list_humi[0]), ('-22h', list_humi[1]), ('-21h', list_humi[2]), ('-20h', list_humi[3]), ('-19h', list_humi[4]), ('-18h', list_humi[5]), ('-17h', list_humi[6]), ('-16h', list_humi[7]), ('-15h', list_humi[8]), ('-14h', list_humi[9]), ('-13h', list_humi[10]), ('-12h', list_humi[11]), ('-11h', list_humi[12]), ('-10h', list_humi[13]), ('-9h', list_humi[14]), ('-8h', list_humi[15]), ('-7h', list_humi[16]), ('-6h', list_humi[17]), ('-5h', list_humi[18]), ('-4h', list_humi[19]), ('-3h', list_humi[20]), ('-2h', list_humi[21]), ('-1h', list_humi[22]), ('-0h', list_humi[23])]
	
	return render_template('index.html', data_temp = data_temp, data_humi = data_humi)

def run():
	global list_temp, list_humi, set_humidity
	
	while True :
		sec = datetime.datetime.now().strftime('%S')
		sensor.temp_check()

		print "setting humidity : " + set_humidity
	
		if sec[1:] == '0' :
			for i in range(0,23):
				list_temp[i] = list_temp[i+1]
				list_humi[i] = list_humi[i+1]	
		
			list_temp[23] = sensor.curr_temp
			list_humi[23] = sensor.curr_humi
			time.sleep(1)
	
		if sensor.curr_humi < set_humidity :
			sensor.relay_on()
		else :
			sensor.relay_off()


if __name__ == "__main__":
	sensor = Sensor()

	run_thread = threading.Thread(target=run)
	run_thread.start()

	app.run(host='0.0.0.0', port=2229, debug=False)
	
