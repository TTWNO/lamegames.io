const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const WSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    /* Make sure that this matches a pattern specfiifed in the websocket_urlspatterns list in skel/urls.py */
    + '/skel/'
);

/* send some data to the server */
const test = () => {
    WSocket.send("Hello world!");
}

/* Print all messages from the server to the status box */
WSocket.onmessage = (e) => {
  write_message(e.data);
}
