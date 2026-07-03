from flask import Flask, render_template,url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template('index.html')

@socketio.on("chat")
def handle_message(data):
    print("Received:", data)

    emit("chat", f"Server received: {data}") #message is the event name it could be anything else


if __name__ == "__main__":
    app.run(debug=True)