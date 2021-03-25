from flask import Flask, render_template,request, redirect, url_for, Response
import serial
import numpy as np
import keyboard  
import time
import sys
import os
import cv2
from camera import Camera

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# serial from usb
print("\n")
if os.path.exists('/dev/ttyACM0') == True:
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    print("Connected to ttyACM0")
elif os.path.exists('/dev/ttyACM1') == True:
    ser = serial.Serial('/dev/ttyACM1',9600,timeout=1)
    print("Connected to ttyACM1")
elif os.path.exists('/dev/ttyUSB0') == True:
    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    print("Connected to ttyUSB0")
elif os.path.exists('/dev/ttyUSB1') == True:
    ser = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
    print("Connected to ttyUSB1")
else:
    print("Serial not found")

ser.flush()
# serial from UART primary pin 8 & 10 or GPIO 14 & 15
#ser = serial.Serial('/dev/serial1',9600,timeout=1) 
start = time.time()
count = 0

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route("/<move>")
def action(move):
    if move=='Forward' or keyboard.is_pressed('w'):
        print("moving forward", file=sys.stderr) # displays message of action
        ser.write(b'forward\n')  # send commands as strings to mcu
    elif move=='Backward' or keyboard.is_pressed('s'):
        print("moving backwards", file=sys.stderr)
        ser.write(b'backward\n')
    elif move=='Left' or keyboard.is_pressed('a'):
        print("turning left", file=sys.stderr)
        ser.write(b'left\n')
    elif move=='Right' or keyboard.is_pressed('d'):
        print("turning right", file=sys.stderr)
        ser.write(b'right\n')
    elif move=='Stop' or keyboard.is_pressed('space'):
        print("stopping", file=sys.stderr)
        ser.write(b'stop\n')
    else:
        pass
    
    if move=='plowUp' or keyboard.is_pressed('i'):
        print("plow up", file=sys.stderr)
        ser.write(b'plow up\n')
    elif move=='plowDown' or keyboard.is_pressed('k'):
        print("plow moving down", file=sys.stderr)
        ser.write(b'plow down\n')
    elif move=='plowLeft' or keyboard.is_pressed('j'):
        print("plow moving left", file=sys.stderr)
        ser.write(b'plow left\n')
    elif move=='plowRight' or keyboard.is_pressed('l'):
        print("plow moving right", file=sys.stderr)
        ser.write(b'plow right\n')
    elif move=='plowCenter'or keyboard.is_pressed('c'):
        print("plow moving to center", file=sys.stderr)
        ser.write(b'plow center\n')
    else:
        pass
    
    return render_template('main.html')


# streaming video
def gen(camera):
    while True:
        frame = camera.get_frame()
        '''
        frame2 = np.copy(frame)
        scale_percent = 75
        width = int(frame2.shape[1] * scale_percent / 100)
        height = int(frame2.shape[0] * scale_percent / 100)
        
        dim_size = (width,height)
        src = cv2.resize(frame2,dim_size)
        path = "home/pi/Pictures/"
        cv2.imwrite(path + 'plowbot_' + str(count) + 'jpg',src)
        count += 1
        '''
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=False,threaded=True,use_reloader=False,host='0.0.0.0')
