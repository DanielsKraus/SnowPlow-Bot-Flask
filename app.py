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

@app.route('/forward/', methods=['POST'])
def forward():
    action = "forward"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/backward/', methods=['POST'])  
def backward():
    action = "backward"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/left/', methods=['POST'])
def left():
    action = "left"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)
    
@app.route('/right/', methods=['POST'])
def right():
    action = "right"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/stop/', methods=['POST'])
def stop():
    action = "stop"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/plowup/', methods=['POST'])
def plowUp():
    action = "plowUp"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/plowdown/', methods=['POST'])
def plowDown():
    action = "plowDown"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/plowleft/', methods=['POST'])
def plowLeft():
    action = "plowLeft"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/plowright/', methods=['POST'])
def plowRight():
    action = "plowRight"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)

@app.route('/plowcenter/', methods=['POST'])
def plowCenter():
    action = "plowCenter"
    print(action)
    ser.write(action + '\n'.encode('ascii'))
    return render_template("main.html", forward_message = action)


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
