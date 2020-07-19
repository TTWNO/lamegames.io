from flask import (
    Flask, Blueprint
)

sbp = Blueprint("sub", __name__, url_prefix="/sub")

@sbp.route("/")
def index():
    return "Index of sub"

@sbp.route("/test")
def test():
    return "We are the tester, my friend!"
