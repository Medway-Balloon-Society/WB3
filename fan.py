import gpiozero as gpio
import datetime as dt

fan = gpio.LED(10)

start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 10:
  fan.on()
quit()

