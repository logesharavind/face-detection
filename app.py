from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import io
from PIL import Image
import base64
import cv2
import numpy as np
import imutils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

def readb64(base64_string):
    idx = base64_string.find('base64,')
    base64_string = base64_string[idx+7:]

    sbuf = io.BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)

    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

@socketio.on('image')
def image(data_image):
    frame = readb64(data_image)

    # Draw a vertical blue line on the frame
    line_x = 200  # Adjust the x-coordinate as needed
    cv2.line(frame, (line_x, 0), (line_x, frame.shape[0]), (255, 0, 0), 2)

    imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)

if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)