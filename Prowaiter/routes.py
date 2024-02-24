from flask import Blueprint, render_template
from .events import users


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", users = users)