from flask import Flask, render_template,url_for, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import random
import time 
from devices import devices ,RATE, WATTAGE

app = Flask(__name__)
socketio = SocketIO(app)

def calculate_usage():
    now = time.time()
    total_kwh = 0
    current_watts = 0

    for device in devices.values():
        wattage = WATTAGE[device["type"]]

        if device["status"] == "on":
            current_watts += wattage

        effective_total_seconds = device["total_on_seconds"]
        if device["status"] == "on":
            effective_total_seconds += now - device["last_changed"]

        kwh = (wattage * effective_total_seconds / 3600) / 1000
        total_kwh += kwh

    estimated_cost = total_kwh * RATE

    return {
        "current_watts": current_watts,
        "total_kwh": round(total_kwh, 6),
        "estimated_cost": round(estimated_cost, 2)
    }

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/devices")
def get_devices():
    return jsonify(devices)

@app.route("/api/usage")
def get_usage():
    now = time.time()
    total_kwh = 0
    for device in devices.values():
        wattage = WATTAGE[device["type"]]
        effective_total_seconds = device["total_on_seconds"]
        if device["status"] == "on":
            effective_total_seconds += now - device["last_changed"]
        kwh = (wattage * effective_total_seconds / 3600) / 1000
        total_kwh += kwh
    estimated_cost = total_kwh * RATE
    current_watts = sum(WATTAGE[d["type"]] for d in devices.values() if d["status"] == "on")
    return jsonify({
        "total_kwh": round(total_kwh, 6),
        "estimated_cost": round(estimated_cost, 2),
        "current_watts": current_watts
    })

@socketio.on("chat")
def handle_message(data):
    print("Received:", data)

    emit("chat", f"Server received: {data}") #message is the event name it could be anything else


def ticker():
    while True:
        for device_id in devices:
            if random.random() < 0.15:
                old_status = devices[device_id]["status"]
                new_status = "off" if old_status == "on" else "on"

                if old_status == "on" and new_status == "off":
                    elapsed = time.time() - devices[device_id]["last_changed"]
                    devices[device_id]["total_on_seconds"] += elapsed

                devices[device_id]["status"] = new_status
                devices[device_id]["last_changed"] = time.time()

        socketio.emit("device_update", devices)
        socketio.emit("usage_update", calculate_usage())
        socketio.sleep(3)


if __name__ == "__main__":
    socketio.start_background_task(ticker)
    app.run(debug=True)