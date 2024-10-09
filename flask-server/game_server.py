from flask import Flask
from flask_socketio  import SocketIO
from game import GoldenBalls

app = Flask(__name__)
socketio =SocketIO(app)
game = GoldenBalls()

# Members API Route
@app.route("/members")
def members():
    return {"members": ["James", "Luke", "Emily", "Jack"]}

if __name__ == "__main__":
    app.run(debug=True)