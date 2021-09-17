#!/usr/bin/python
import targetTemp
import duration
import time
import board
import busio
import adafruit_bmp3xx
import adafruit_dht
import csv
from picamera import PiCamera, Color
from subprocess import call
import datetime as dt
from gpiozero import Button, LED
import os
from pathlib import Path
from time import sleep
from gpiozero import LED
from w1thermsensor import W1ThermSensor
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D27)
sensor = W1ThermSensor()
fet = LED(22)
lled = LED(13)
button = Button(26)

lled.on()
time.sleep(1)
lled.off()
time.sleep(1)
lled.on()
time.sleep(1)
lled.off()

print('on')

temp = 50
heat = 0
tempInternal = 74

i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, address=0x76)
bmp.sea_level_pressure = int(bmp.pressure)
ads = ADS.ADS1115(i2c)
sensorValue = AnalogIn(ads, ADS.P0)
ads.mode = Mode.CONTINUOUS

humidity = 50
altitude = 5
pressure = 4
temp = 7

camera = PiCamera()

lled.on()
time.sleep(1)
lled.off()

#while True:
 # if(button.is_pressed):
  #  for x in range(3):
   #   lled.on()
    #  time.sleep(0.5)
     # lled.off()
#      time.sleep(0.5)
 #   afterButton()
  #  break

def sensor_write(Saltitude, Spressure, Stemp, Shumidity, StempInternal, Sheat, Sco2, SrawCO2, SrawVolts):
    with open ('Readings/alt.csv', 'a') as log:
        dataAlt = [Saltitude, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(dataAlt)
        
    with open ('Readings/press.csv', 'a') as log:
        dataPress = [Spressure, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(dataPress)
        
    with open ('Readings/temp.csv', 'a') as log:
        dataTemp = [Stemp, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(dataTemp)
        
    with open ('Readings/humidity.csv', 'a') as log:
        data = [Shumidity, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(data)
        
    with open ('Readings/status.csv', 'a') as log:
        statusData = [heat, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(statusData)
        
    with open ('Readings/tempDS.csv', 'a') as log:
        tempData = [StempInternal, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(tempData)
        
    with open ('Readings/status.csv', 'a') as log:
        statusData = [Sheat, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(statusData)
        
    with open('Readings/co2.csv', "a") as log:
        data = [Sco2, SrawCO2, SrawVolts, (dt.datetime.now() - start).seconds]
        log_writer = csv.writer(log)
        log_writer.writerow(data)
       
file = open("Readings/alt.csv", "r+")     
file.truncate(0)
file.close

file = open("Readings/press.csv", "r+")
file.truncate(0)
file.close

file = open("Readings/temp.csv", "r+")
file.truncate(0)
file.close

with open("Readings/humidity.csv", "r+") as file:
    file.truncate(0)

file = open("Readings/status.csv", "r+")
file.truncate(0)
file.close

file = open("Readings/tempDS.csv", "r+")
file.truncate(0)
file.close

file = open("Readings/co2.csv", "r+")
file.truncate(0)
file.close

camera.resolution = (1920, 1080)
camera.framerate = 24
camera.awb_mode = 'sunlight'
camera.start_recording('Videos/dianeistheimpostor.h264', quality = 20, bitrate = 750000)

#def afterButton():
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < duration.time:
    print("--------------")
    lled.on()
    time.sleep(1)
    lled.off()

    #DHT22    
    try:
        testhumidity = dhtDevice.humidity
        if (testhumidity == None):
             print("Humidity did not read")
        else:
             humidity = testhumidity
             print(f"Humidity: {humidity}% ")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        continue
    except Exception as error:
        #dhtDevice.exit()
       # raise error
        continue
    try:
        print('before temp read')
        tempInternal = sensor.get_temperature()
          print('temp declared')
        #continue
    except IndexError:
        #time.sleep(0.1)
        print ("Internal temp - tom servo timed out")
       # for x in range(3):
      #      try:
     #           tempInternal = int((sensor.get_temperature() * 1.8) + 32)
    #        except IndexError:
   #             if x == 3:
  #                  print ("Internal temp - TIME OUT")
 #               else:
#                    time.sleep(0.1)
    print('starting readings')
    altitude = int(bmp.altitude)
    pressure = int(bmp.pressure)
    temp = int((bmp.temperature * 1.8) + 32)
    rawCO2 = sensorValue.value
    rawVolts = sensorValue.voltage
    voltage_difference = (sensorValue.voltage*1000) - 400
    concentration = voltage_difference * 50.0/16.0
    print('finished readingsssnake')
    sensor_write(altitude, pressure, temp, humidity, tempInternal, heat, concentration, rawCO2, rawVolts)
    print('finished sensor write')
#    camera.annotate_text = str(temp) + ' F' + '                                  ' + str(altitude) + ' m' + '                                   ' + str(pressure) + ' hpa'
 #   camera.annotate_foreground = Color('white')
  #  camera.annotate_text_size = 40
    print('starting heater control code')
    #Heater Control 
    if(tempInternal < targetTemp.thresh):
        fet.on()
        heat = 1
    else:
        fet.off()
        heat = 0
    print('finished heater control')
    print('Internal temp: {}'.format(tempInternal))
    print('Heater: {}'.format(heat))
    print('Co2 is {} ppm'.format(concentration))
    print('Seconds since start {}'.format((dt.datetime.now() - start).seconds))
    # print('voltage is {} mv'.format(sensorValue.voltage))
    # print('raw value: {}'.format(sensorValue.value))
    # print('raw voltage: {}'.format(sensorValue.voltage))

        
camera.wait_recording(0.2)
	
camera.close()
print('Main code is done')
lled.on()
time.sleep(5)
lled.off()
#  call('sudo shutdown -h now', shell = True)
quit()
