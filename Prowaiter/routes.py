from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from .events import users

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", users=users)

@main.route("/get_username", methods=["GET"])
def get_username():
    username = session.get('username')
    return jsonify({'username': username})

@main.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return jsonify({'success': True})
