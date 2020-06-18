from flask import Flask, render_template,request, redirect, url_for
import serial  
import keyboard  
import time
import sys
import cv2
from camera import Camera

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'yourkeyhere'

#ser = serial.Serial('/dev/ttyACM1',9600) 
start = time.time()

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route("/<move>")
def action(move):
    if move=='Forward' or keyboard.is_pressed('w'):
        print("moving forward", file=sys.stderr) # displays message of action
        ser.write('forward')  # send commands as strings to mcu
    elif move=='Backward' or keyboard.is_pressed('s'):
        print("moving backwards", file=sys.stderr)
        ser.write('backward')
    elif move=='Left' or keyboard.is_pressed('a'):
        print("turning left", file=sys.stderr)
        ser.write('left')
    elif move=='Right' or keyboard.is_pressed('d'):
        print("turning right", file=sys.stderr)
        ser.write('right')
    elif move=='Stop' or keyboard.is_pressed('space'):
        print("stopping", file=sys.stderr)
        ser.write('stop')
    else:
        pass
    
    if move=='plowUp' or keyboard.is_pressed('i'):
        print("plow up", file=sys.stderr)
        ser.write('plow up')
    elif move=='plowDown' or keyboard.is_pressed('k'):
        print("plow moving downdown", file=sys.stderr)
        ser.write('plow down')
    elif move=='plowLeft' or keyboard.is_pressed('j'):
        print("plow moving left", file=sys.stderr)
        ser.write('plow left')
    elif move=='plowRight' or keyboard.is_pressed('l'):
        print("plow moving right", file=sys.stderr)
        ser.write('plow right')
    elif move=='plowCenter'or keyboard.is_pressed('c'):
        print("plow moving to center", file=sys.stderr)
        ser.write('plow center')
    else:
        pass
    
    return render_template('main.html')

# streaming video
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=False) # for development make replace False with true
