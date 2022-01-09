# New games

Here is how to create a new game.

## Step 1

Remove the comments next to the text "NOTE: uncomment this to create a new game" in `lamegames/settings.py`
Once logged in, this will allow you to see "Skeleton Game" as an option.

## Step 2

Before making any changes, try to understand the structure of `/skel/`.
Here is what you need to know in simple terms; check out each individual file for more information on how each component works:

1. URLs are defined in `skel/urls.py`, this includes HTTP urls as well as WebSocket connection points.
  * HTTP responses return from `skel/views.py`.
  * WebSocket requests return from `skel/consumers.py`.
2. WebSockets are connected to from the client in `skel/static/games/skel.js`.
3. Models are defined in `skel/models.py`. None are included by default, but check out the [Django documentation](https://docs.djangoproject.com/en/4.0/topics/db/models/) for further information on how these work.
4. The HTML template used for the game is defined in `skel/templates/games/skel.html`.

## Step 3

Let's create a brand new game, disconnected from our "skel" fake game.
For the purposes of this guide `xyz` will be the name of our new game.
To create a new game, run the command `python manage.py newgame xyz` a new game called `xyz` will now be created; change two things to show your game in action:

1. Add `xyz` to the `INSTALLED_APPS` list in `lamegames/settings.py`.
2. Add `xyz` to the `GAMES` list in `lamegames/settings.py`.

For 2, check the syntax of how other apps/games are added for an idea of how to do so.

## Step 4

Have fun! Look at django guides as well as examples we have created:

* `rps/` is for Rock-Paper-Scissors
* `minesweeper/` is for Minesweeper
* `chat/` is for a simple, open-air chat room defined by a room id.

Check how these examples work for more information, and look into how Django, Django channels and Django models work to create more advanced games.
Some games (like rock-paper-scissors) will not need such advanced features as models, but they do require knowledge of channels.
Others (like Minesweeper) require little knowledge of channels due to their single-player nature, but do require some more models so a game may be saved for a user when they come back.

## Step 5

Be creative!

I want to see the following games eventually make it into lamegames:

* Malcana,
* (simple) Chess,
* Card games: blackjack, poker and "Uno"-like games.
* Chinese Chess (where the knight moves 2+2 instead of 2+1).
* etc.

Make it happen, and be the next contributer!
