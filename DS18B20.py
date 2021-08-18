import time
from w1thermsensor import W1ThermSensor
import csv
import datetime as dt
from gpiozero import LED

sensor = W1ThermSensor()
fet = LED(22)

temp = 7
heat = 0

def sensor_write(Stemp, heat):
  with open ('Readings/status.csv', 'a') as log:
        log_writer = csv.writer(log)
        log_writer.writerow({heat})
  with open ('Readings/tempDS.csv', 'a') as log:
        log_writer = csv.writer(log)
        log_writer.writerow({Stemp})

file = open("Readings/status.csv", "r+")
file.truncate(0)
file.close

file = open("Readings/tempDS.csv", "r+")
file.truncate(0)
file.close

start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 3600:
    temp = int((sensor.get_temperature() * 1.8) + 32)
    print(temp, heat)
    sensor_write(temp, heat)
    if(temp < 45):
        fet.on()
        heat = 1
    else:
        fet.off()
        heat = 0
print('im doneeeeeee')
quit()
