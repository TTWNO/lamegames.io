const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const RPSSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    + '/rps/'
    + ROOM_ID
);
const STATUS_BOX = document.getElementById("logbox");

const write_message = (mess) => {
    STATUS_BOX.innerHTML += mess + "<br>";
    STATUS_BOX.scrollTop = STATUS_BOX.scrollHeight;
}
const clear_statusbox = () => {
    STATUS_BOX.innerHTML = '';
    write_message('<i>Status Cleared</i>');
}

RPSSocket.onmessage = function(e) {
    console.log("Receiving...");
    console.log(e.data);
    console.log(JSON.parse(e.data));

    data = JSON.parse(e.data);
    message = data.message;
    if (data.event === 'warning')
    {
      write_message(message);
    } else if (data.event === 'game_over') {
      write_message("<b>" + message + "</b>");
    } else if (data.event === 'info') {
      write_message("<i>" + message + "</i>");
    }
}

for (btn of document.querySelectorAll(".rpsbtn"))
{
    btn.addEventListener('click', e => {
        write_message("You selected " + e.target.id);
        RPSSocket.send(
            JSON.stringify({
                'choice': e.target.id
            })
        );
    })
}
