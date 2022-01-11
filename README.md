# Lamegames

This is my lamegames repository.
It has a lot of lame games, lol!

## Run Locally

To run a local instance, you will need to run the following commands after `cd`ing yourself into the lamegames repo; $ represents a command, # is a comment:

```bash
# create a virtual environment (aka install dependencies locally, instaed of system-wide)
$ python -m venv env
# activate virtual environment (use local dependencies instaed of system-wide dependencies)
$ source env/bin/activate
# install dependencies
$ pip install -r requirements.txt
# run django migrations (setup database)
$ python manage.py makemigrations
$ python manage.py migrate
# start redis (install it first, if you don't have it)
$ systemctl start redis
# start django app
$ python manage.py runserver
# now access at http://localhost:8000/ woot woot!
```

## How to add a game:

See `/skel/README.md`
