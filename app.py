from flask import Flask, render_template,url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
import random

app = Flask(__name__)
socketio = SocketIO(app)
devices = {
    "drawingroom_fan1": {"status": "off"},
    "drawingroom_fan2": {"status": "off"},
    "drawingroom_light1": {"status": "off"},
    "drawingroom_light2": {"status": "off"},
    "drawingroom_light3": {"status": "off"},

    "workroom1_fan1": {"status": "off"},
    "workroom1_fan2": {"status": "off"},
    "workroom1_light1": {"status": "off"},
    "workroom1_light2": {"status": "off"},
    "workroom1_light3": {"status": "off"},

    "workroom2_fan1": {"status": "off"},
    "workroom2_fan2": {"status": "off"},
    "workroom2_light1": {"status": "off"},
    "workroom2_light2": {"status": "off"},
    "workroom2_light3": {"status": "off"},
}

@app.route("/")
def home():
    return render_template('index.html')

@socketio.on("chat")
def handle_message(data):
    print("Received:", data)

    emit("chat", f"Server received: {data}") #message is the event name it could be anything else

# run differetn times for different rooms 
def ticker():
    while True:
        for device in devices:
            devices[device]["status"] = random.choice(["on", "off"])

        socketio.emit(
            "device_update",
            devices
        )
        socketio.sleep(5)



if __name__ == "__main__":
    socketio.start_background_task(ticker)
    app.run(debug=True)