const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const RPSSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    + '/rps/'
);

RPSSocket.onmessage = function(e) {
    console.log("Receiving...");
    console.log(JSON.parse(e.data));
}