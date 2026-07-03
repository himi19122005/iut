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

socket.on("device_update", (devices) => {

    for (const deviceName in devices) {
        const status = devices[deviceName].status;
        console.log(status)
        const card = document.getElementById(deviceName);

        if (!card) continue;
        card.textContent = status.toUpperCase(); //this only changes the display to uppercase

        if (status === "on") {
            card.style.backgroundColor = "#daa671";
        } else {
            card.style.backgroundColor = "#c55113";
        }
    }

});