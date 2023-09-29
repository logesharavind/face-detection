from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io
from PIL import Image
import base64
import cv2
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
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
    # Encode the processed frame and send it back to the client
    _, buffer = cv2.imencode('.jpg', frame)
    data_image = base64.b64encode(buffer).decode('utf-8')
    emit('response_back', data_image)

if __name__ == '__main__':
    socketio.run(app, debug=True)
