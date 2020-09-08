const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const RPSSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    + '/rps/'
    + ROOM_ID
);

RPSSocket.onmessage = function(e) {
    console.log("Receiving...");
    console.log(e.data);
    console.log(JSON.parse(e.data));

    data = JSON.parse(e.data);
    message = data.message;
    if (data.event === 'warning')
    {
        alert(message);
    } else if (data.event == 'game_over') {
        if (message === 'tie')
        {
            alert("Tie!");
        } else {
            alert("The winner is: " + message.winner);
        }
    }
}

for (btn of document.querySelectorAll(".rpsbtn"))
{
    btn.addEventListener('click', e => {
        alert("You pressed " + e.target.id);
        RPSSocket.send(
            JSON.stringify({
                'choice': e.target.id
            })
        );
    })
}
