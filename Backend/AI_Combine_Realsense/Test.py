import socketio

sio = socketio.Client()

try:
    sio.connect('http://130.216.238.175:5000')
    print('Connected')
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")
