from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit, join_room
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, logger=True)
socketio.init_app(app, cors_allowed_origins="*")

# dictionary pairing room name to admin socket id
rooms = {}

# dictionary pairing player name to socket id
names = {}

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/<room>')
def game(room):
    return render_template('play.html')

def is_admin(id, room):
    return rooms[room] == id

@socketio.on('connection')
def on_connect(socket):
    print('user connected')

@socketio.on('disconnect')
def on_admin_disconnect():
    print('user disconnected')
    # so to not change the size of dictionary during iteration
    room_to_del = None
    for room in rooms:
        if is_admin(request.sid, room):
            room_to_del = rooms[room]
    del room_to_del
    emit('leave')

@socketio.on('exists')
def exists(data):
    room = data['room']
    emit('exists', room in rooms, callback=ack)

@socketio.on('join')
def on_join(data):
    name = data['name']
    # refactor so that it is like create
    # and checks if the name is taken
    if (name in names):
        emit('name_taken', { 'name': name }, room=room)
    name = data['name']
    room = data['room']
    if not is_admin(request.sid, room):
        join_room(room)
    emit('join', data, room=room)
    print(f'{name} joined {room}')

@socketio.on('begin')
def on_begin(data):
    room = data['room']
    if is_admin(request.sid, room):
        emit('begin', room=room)

@socketio.on('resume')
def on_resume(data):
    room = data['room']
    emit('resume', room=room)

def ack():
    print('message was received!')

@socketio.on('create')
def on_create(data):
    room = data['room']
    if (room in rooms or len(room) < 3):
        emit('create', False)
        print(f'cannot create room: {room}')
    else:
        join_room(room)
        rooms[room] = request.sid
        emit('create', True, callback=ack)
        print(f'created room: {room}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')