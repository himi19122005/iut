console.log("Connected!");
const socket = io();

// send a message to the server
// socket.emit("chat", "Hello server"); 

  // listen for messages from the server
socket.on("chat", (msg) => {
    console.log("Message from server:", msg);
});

// socket.on("tick", (data) => {
//     document.getElementById("clock").textContent = data.time;
//     console.log(data);
// }); delete this 

function renderDevices(devices) {
    for (const deviceName in devices) {
        const status = devices[deviceName].status;
        const card = document.getElementById(deviceName);
        if (!card) continue;
        card.textContent = status.toUpperCase();
        if (status === "on") {
            card.style.backgroundColor = "#98b13b";
        } else {
            card.style.backgroundColor = "#c55113";
        }
    }
}

function fetchDevices() {
    fetch("/api/devices")
        .then(res => res.json())
        .then(data => renderDevices(data));
}

socket.on("device_update", (devices) => {
    renderDevices(devices);
});




function renderUsage(data) {
    document.getElementById("total-kwh").textContent = data.total_kwh;
    document.getElementById("estimated-cost").textContent = data.estimated_cost + " Tk";
    document.getElementById("current-watts").textContent = data.current_watts + " W";
}

function fetchUsage() {
    fetch("/api/usage")
        .then(res => res.json())
        .then(data => renderUsage(data));
}

socket.on("usage_update", (data) => {
    renderUsage(data);
});

// call once on page load
fetchUsage();
fetchDevices();