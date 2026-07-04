import time

WATTAGE = {"fan": 60, "light": 15}
RATE=5


devices = {
    "drawingroom_fan1": {
        "status": "off",
        "type": "fan",
        "room": "drawingroom",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "drawingroom_fan2": {
        "status": "off",
        "type": "fan",
        "room": "drawingroom",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "drawingroom_light1": {
        "status": "off",
        "type": "light",
        "room": "drawingroom",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "drawingroom_light2": {
        "status": "off",
        "type": "light",
        "room": "drawingroom",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "drawingroom_light3": {
        "status": "off",
        "type": "light",
        "room": "drawingroom",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },

    "workroom1_fan1": {
        "status": "off",
        "type": "fan",
        "room": "workroom1",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom1_fan2": {
        "status": "off",
        "type": "fan",
        "room": "workroom1",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom1_light1": {
        "status": "off",
        "type": "light",
        "room": "workroom1",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom1_light2": {
        "status": "off",
        "type": "light",
        "room": "workroom1",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom1_light3": {
        "status": "off",
        "type": "light",
        "room": "workroom1",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },

    "workroom2_fan1": {
        "status": "off",
        "type": "fan",
        "room": "workroom2",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom2_fan2": {
        "status": "off",
        "type": "fan",
        "room": "workroom2",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom2_light1": {
        "status": "off",
        "type": "light",
        "room": "workroom2",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom2_light2": {
        "status": "off",
        "type": "light",
        "room": "workroom2",
        "last_changed": time.time(),
        "total_on_seconds": 0
    },
    "workroom2_light3": {
        "status": "off",
        "type": "light",
        "room": "workroom2",
        "last_changed": time.time(),
        "total_on_seconds": 0
    }
}