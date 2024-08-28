from picamera2 import Picamera2
import cv2
from flask import Flask, Response

app = Flask(__name__)

camera = Picamera2()
config = camera.create_video_configuration(main={"size": (1640, 1232)})  # A resolution close to full but optimized for better frame rates
camera.configure(config)
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'f--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)