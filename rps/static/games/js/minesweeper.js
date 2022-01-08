/* TODO: remove hardcoded values */
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

const say_pos = () => {
    big = LATEST_BUTTON.id.split('-').pop()
    x = big % 10;
    y = Math.floor(big / 10);
    write_message(x + ',' + y);
};

const btn_clear = (btn) => {
    btn.innerHTML = '';    
    btn.setAttribute('bombs', '');
    btn.classList.remove('showing');
};
const make_btn_bomb = (btn) => {
    btn_clear(btn);
    btn.innerHTML = BOMB_UNICODE;
    btn.classList.add('showing');
};
const make_btn_bombnum = (btn, bn) => {
    btn_clear(btn);
    btn.innerHTML = bn;
    btn.setAttribute('bombs', bn);
    btn.classList.add('showing');
};
const btn_flag = (btn) => {
    btn_clear(btn);
    btn.innerHTML = RED_FLAG_UNICODE;
};
const btn_unflag = (btn) => {
    btn_clear(btn);
    btn.innerHTML = '';
};

const help_menu = () => {
    write_message("h: This help menu.<br>\
    n: New game.<br>\
    f: Toggle flag on current tile.<br>\
    c: Read current position.<br>\
    Space/Enter: Expose current tile.<br>\
    w/a/s/d: up/left/down/right.");
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
                btn_flag(LATEST_BUTTON);
                write_message("Flagged " + (bid % 10) + "," + Math.floor(bid / 10));
            } else {
                btn_unflag(LATEST_BUTTON);
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
    console.log(bid, event_type);
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
    if (e.key === 'c') {
        say_pos();
    }
    /* if no last button: do not change */
    if (!LATEST_BUTTON)
    {
        return;
    }

    old_id = Number(LATEST_BUTTON.id.split('-').pop());
    old_x = old_id % 10;
    old_y = Math.floor(old_id / 10);
    new_x = old_x;
    new_y = old_y;
    console.log("OID: " + old_id);
    if (e.key === 'w') {
        new_y -= 1;
    } else if (e.key === 'a') {
        new_x -= 1;
    } else if (e.key === 's') {
        new_y += 1
    } else if (e.key === 'd') {
        new_x += 1;
    }
    /* if new cord over/under limit: stop */
    if (new_x < 0 || new_x > 9 ||
        new_y < 0 || new_y > 9)
    {
        return;
    }

    new_id = (new_y*10) + new_x;

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

const change_board = (board_parts) => {
    let shown_tiles = 0;
    for (cell of board_parts)
    {
        i = (cell.y*10) + cell.x;
        console.log("mscell-" + i)
        btn = document.getElementById("mscell-" + i);
        if (cell.bombs_next >= 0) {
            make_btn_bombnum(btn, cell.bombs_next);
        }
        if (cell.flagged)
        {
            btn_flag(btn);
        }
        if (cell.bomb) {
            make_btn_bomb(btn, BOMB_UNICODE);
        }
        shown_tiles++;
    }
    write_message("You have exposed " + shown_tiles + " tiles");
};


MSSocket.onmessage = (e) => {
    console.log(e.data);
    console.log(JSON.parse(e.data));
    data = JSON.parse(e.data);

    if (data.type === 'change-board') {
        change_board(data.payload);
    } else if (data.type === 'game_over') {
        MSSocket.send(JSON.stringify({
            'type': 'full_board'
        }));
    } else if (data.type === 'new_board') {
        for (btn of document.getElementsByClassName("cell"))
        {
            btn_clear(btn);
        }
    } else if (data.type === 'message') {
        write_message(data.payload);
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