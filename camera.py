from picamera import PiCamera, Color
from BMP388 import getStuff 
import datetime as dt
import duration

camera = PiCamera()
camera.reselution = (1920, 1080)
camera.framerate = 24
camera.awb_mode = 'sunlight'


start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < duration.time:

    altitude = getStuff('altitude')
    pressure = getStuff('pressure')
    temp = getStuff('temp')
            
    camera.annotate_text = str(temp) + ' F' + '                                  ' + str(altitude) + ' m' + '                                   ' + str(pressure) + ' hpa'
    camera.annotate_foreground = Color('white')
    camera.annotate_text_size = 40
camera.wait_recording(0.2)
	
camera.close()
quit()
