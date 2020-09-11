const WSProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const MSSocket = new WebSocket(
    WSProtocol
    + '://'
    + window.location.host
    + '/minesweeper/'
);

const RED_FLAG_UNICODE = '🚩';
const BOMB_UNICODE = '💣';

/* TODO: remove global variable */
let LATEST_BUTTON;

const help_menu = () => {
    write_message("h: Help menu")
    write_message("n: New game");
    write_message("f: Toggle flag on current tile");
    write_message("Space/Enter: Expose current tile");
    write_message("w/a/s/d: up/left/down/right");
};

const change_aria = (el, rep, new_l) => {
    el.setAttribute('aria-label', el.getAttribute('aria-label').replace(rep, new_l));
};

const send_click = (e, event_type) => {
    LATEST_BUTTON = e.target;
    bid = Number(LATEST_BUTTON.id.split('-').pop());
    if (event_type === 'flagged')
    {
        // if is number, meaning: already shown
        if (/[0-9]/.test(LATEST_BUTTON.innerHTML))
        {
            write_message("<i>You cannot flag a square that is already showing</i>");
        } else {
            if (LATEST_BUTTON.innerHTML !== RED_FLAG_UNICODE)
            {
                LATEST_BUTTON.innerHTML = RED_FLAG_UNICODE;
                change_aria(LATEST_BUTTON, /^[0-9]/, 'F $&');
                write_message("Flagged " + (bid % 10) + "," + Math.floor(bid / 10));
            } else {
                LATEST_BUTTON.innerHTML = '';
                change_aria(LATEST_BUTTON, /^F\ /, '');
                write_message("Unflagged " + (bid % 10) + "," + Math.floor(bid / 10));
            }
        }
    } else if (event_type === 'clicked') {
        // if flagged
        if (LATEST_BUTTON.innerHTML === RED_FLAG_UNICODE)
        {
            write_message('<i>You cannot click on a flagged element!</i>')
            return;
        }
        if (/[0-9]/.test(LATEST_BUTTON.innerHTML))
        {
            write_message('<i>You have already exposed this peice!</i>');
            return;
        }
    }
    console.log(bid)
    MSSocket.send(JSON.stringify(
        {
            'type': event_type,
            'button_id': bid
        }
    ));
};

const moving_key_handler = (e) => {
    if (e.key === 'f') {
        send_click(e, 'flagged');
    }
    /* if no last button: do not change */
    if (!LATEST_BUTTON)
    {
        return;
    }

    old_id = Number(LATEST_BUTTON.id.split('-').pop());
    console.log("OID: " + old_id);
    /* TODO: remove hardcoded values */
    if (e.key === 'w') {
        new_id = old_id -= 10;
    } else if (e.key === 'a') {
        new_id = old_id -= 1;
    } else if (e.key === 's') {
        new_id = old_id += 10;
    } else if (e.key === 'd') {
        new_id = old_id += 1;
    }

    /* if new ID over/under limit: stop */
    /* TODO: remove hardcoded values */
    if (new_id > 99 || new_id < 0)
    {
        return;
    }

    console.log("NID: " + new_id);
    /* focus on new button ID */
    document.getElementById("mscell-" + new_id).focus();
};

const gen_new_board = () => {
    write_message("<i>Generating new board...</i>")
    MSSocket.send(JSON.stringify({
        'type': 'generate'
    }));
};

const global_key_handler = (e) => {
    console.log(e.key);
    if (e.key === 'n') {
        gen_new_board();
    } else if (e.key === 'h') {
        help_menu();
    }
};


MSSocket.onmessage = (e) => {
    console.log(e.data);
    console.log(JSON.parse(e.data));
    data = JSON.parse(e.data);

    if (data.type === 'display') {
        let shown_tiles = 0;
        for (cell of data.partial_board)
        {
            i = (cell.y*10) + cell.x;
            console.log("mscell-" + i)
            btn = document.getElementById("mscell-" + i);
            btn.innerHTML = cell.bombs_next;
            change_aria(btn, /^([F]\ )?/, cell.bombs_next + ' $&');
            shown_tiles++;
        }
        if (data.flagged)
        {
            for (cell of data.flagged)
            {
                i = (cell.y*10) + cell.x;
                btn = document.getElementById("mscell-" + i);
                btn.innerHTML = RED_FLAG_UNICODE; 
                change_aria(btn, /^[0-9]/, 'F $&');
            }
        }
        write_message("You have exposed " + shown_tiles + " tiles");
    } else if (data.type === 'display_full') {
        for (cell of data.full_board)
        {
            i = (cell.y*10) + cell.x;
            btn = document.getElementById("mscell-" + i);
            if (cell.bomb) {
                btn.innerHTML = BOMB_UNICODE;
                change_aria(btn, /^([F]\ )?([0-8]\ )?/, BOMB_UNICODE + ' ')
            } else {
                btn.innerHTML = cell.bombs_next;
                change_aria(btn, /^([F]\ )?([0-8]\ )?/, cell.bombs_next + ' ');
            }
        }
    } else if (data.type === 'game_over') {
        MSSocket.send(JSON.stringify({
            'type': 'full_board'
        }));
    } else if (data.type === 'new_board') {
        for (btn of document.getElementsByClassName("cell"))
        {
            btn.innerHTML = '';
            change_aria(btn, /^([F]\ )?([0-8]\ )?/, '');
        }
    } else if (data.type === 'message') {
        write_message(data.message);
    }
};

/* TODO: remove hardcoded "clicked"/"flagged" Low-Priority */
for (cell of document.getElementsByClassName("cell")) {
    cell.addEventListener('keydown', moving_key_handler);
    cell.addEventListener('click', (e) => {
        send_click(e, 'clicked');
    });
    cell.addEventListener('contextmenu', (e) => {
        send_click(e, 'flagged');
    });
    cell.addEventListener('focus', (e) => {
        LATEST_BUTTON = e.target;
    });
}

document.addEventListener('keypress', global_key_handler);
help_menu();