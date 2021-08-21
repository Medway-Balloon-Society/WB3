import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import time
import csv
import datetime as dt
import duration

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
sensorValue = AnalogIn(ads, ADS.P0)
ads.mode = Mode.CONTINUOUS

def sensor_write(Sco2):
  with open('Readings/co2.csv') as log:
    log_writer = csv.writer(log)
    log_writer.writerow({Sco2})

with open('Readings/co2.csv'):
  file.truncate


start = dt.datetime.now
while (start - start).seconds < duration.time:
  voltage_difference = (sensorValue.voltage*1000) - 400
  concentration = voltage_difference * 50.0/16.0
  print('voltage is {} mv'.format(sensorValue.voltage))
  print('Co2 is {} ppm'.format(concentration))
  print('raw value: {}'.format(sensorValue.value))
  print('raw voltage: {}'.format(sensorValue.voltage))
  sensor_write(concentration)
quit()
