from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('landing.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')