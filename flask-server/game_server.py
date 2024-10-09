from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
from game import GoldenBalls 

app = Flask(__name__)

# Allow CORS for the client application
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
socketio = SocketIO(app, cors_allowed_origins="*")

# Contains a dictionary of clients that have connected: {session_id: {'username': 'some_name'}}
connected_clients = {}

@app.route('/')
def index():
    return jsonify(message="Welcome to the Golden Balls Game! Use WebSocket for communication.")

@socketio.on('connect')
def handle_connect():
    session_id = request.sid  # Get the session ID of the client
    print(f'Client {session_id} has connected.')
    connected_clients[session_id] = {}  # Add client to the dictionary (can add more client details)
    print(f"Current clients: {connected_clients}")

    if len(connected_clients) == 4:
        print("All clients connected!")
        game = GoldenBalls(socketio, connected_clients)
        game.play()


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid  # Get the session ID of the client
    if session_id in connected_clients:
        del connected_clients[session_id]  # Remove client from the dictionary when they disconnect
        print(f'Client {session_id} has disconnected.')
    print(f"Current clients: {connected_clients}")

@socketio.on('message')
def handle_message(msg):
    print(f'Received message: {msg} from {request.sid}')
    target_sid = request.sid  # You can specify another sid if you want to send to a different client
    emit('message', msg, to=target_sid)  # Send message to specific client

if __name__ == '__main__':
    socketio.run(app, debug=True)