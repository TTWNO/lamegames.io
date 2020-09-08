const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const RPSSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    + '/rps/'
    + ROOM_ID
);

const create_status = () => {
    var status = document.createElement("p");
    status.id = "status";
    wrp = document.getElementById("wrapper");
    wrp.appendChild(status);
}

const write_message = (mess) => {
    let status = document.getElementById("status");
    if (!status)
    {
        create_status();
        status = document.getElementById("status");
    }
    status.innerHTML = mess;
    status.focus(); 
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
    } else if (data.event == 'game_over') {
        if (message === 'tie')
        {
            write_message('Tie!')
        } else {
            write_message("The winner is: " + message.winner);
        }
    }
}

for (btn of document.querySelectorAll(".rpsbtn"))
{
    btn.addEventListener('click', e => {
        create_status();
        let status = document.getElementById("status");
        status.innerHTML = "You pressed " + e.target.id;
        status.focus();
        RPSSocket.send(
            JSON.stringify({
                'choice': e.target.id
            })
        );
    })
}
