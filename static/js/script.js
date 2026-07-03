console.log("Connected!");
const socket = io();
// send a message to the server
// socket.emit("chat", "Hello server"); if i add this to this page it doesnt work console logging it works 

  // listen for messages from the server
socket.on("chat", (msg) => {
    console.log("Message from server:", msg);
});