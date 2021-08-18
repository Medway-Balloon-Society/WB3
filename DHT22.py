import time
import board
import adafruit_dht
import datetime as dt
import csv

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D27)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

def sensor_write(Shumidity):
  with open ('Readings/humidity.csv', 'a') as log:
    data = [Shumidity]
    log_writer = csv.writer(log)
    log_writer.writerow(data)

file = open("Readings/humidity.csv", "r+")
file.truncate(1)
file.close()

start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 10:
    try:
        humidity = dhtDevice.humidity
        print("Humidity: {}% ".format(humidity))
        sensor_write(humidity)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
print('DHT22 is done')
quit()
