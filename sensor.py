import Adafruit_BBIO.GPIO as GPIO
import Adafruit_DHT

class Sensor:
	curr_temp = 0
	curr_humi = 0

	def temp_check(self):
		global curr_temp, curr_humi

		humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, 'P8_13')

		if temperature is not None and humidity is not None:
			self.curr_temp = temperature
			self.curr_humi = humidity

	def relay_on(self):
		GPIO.output("P8_11", GPIO.HIGH)

	def relay_off(self):
		GPIO.output("P8_11", GPIO.LOW)

	def __init__(self):
		GPIO.setup("P8_11", GPIO.OUT)