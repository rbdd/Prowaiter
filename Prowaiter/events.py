from flask import request
from flask_socketio import emit

from .extensions import socketio

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid
    emit_user_list_update()

@socketio.on("remove_user")
def remove_user(username):
    if username in users:
        users.pop(username)
        emit_user_list_update()

def emit_user_list_update():
    user_list = list(users.keys())
    print(user_list)
    emit("user_list_update", user_list, broadcast=True)
    