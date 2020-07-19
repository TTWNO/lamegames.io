from flask import (
    Blueprint, Flask
)
from . import sub
app = Flask(__name__)
app.register_blueprint(sub.sbp)

@app.route('/')
def hello_word():
    return 'Hello world!'

