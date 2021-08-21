import gpiozero
from subprocess import call

button = gpiozero.Button(26)

if(button.is_pressed):
  call('sudo python3 BMP388.py & sudo python3 camera.py & python3 DHT22.py & sudo python3 DS18B20.py & sudo python3 co2.py & sudo python3 fan.py', shell = False) 
