import time
import board
import busio
import adafruit_bmp3xx
import csv
import duration
import datetime as dt
i2c = busio.I2C(board.SCL, board.SDA)
#bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, address = 0x76)
#uncomment line above if SD0 pin is connected to GND.
bmp.sea_level_pressure = int(bmp.pressure)

temp = 7

def getStuff(value):
  if(value == 'altitude'):
    return int(bmp.altitude)
  if(value == 'pressure'):
    return int(bmp.pressure)
  if(value == 'temp'):
   return int(bmp.temperature)

def sensor_write(Stemp):
  with open ('Readings/temp.csv', 'a') as log:
        log_writer = csv.writer(log)
        log_writer.writerow({Stemp})

file = open("Readings/temp.csv", "r+")
file.truncate
file.close

start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < duration.time:
    temp = int((bmp.temperature * 1.8) + 32)
    print(temp)
    sensor_write(temp)
    time.sleep(2)
print('BMP388 is done')
quit()
