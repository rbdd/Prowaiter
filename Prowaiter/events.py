from flask import request, session
from flask_socketio import emit

from .extensions import socketio

users = {}
admin_sid = None

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    global admin_sid
    if username == "admin" and not admin_sid:
        admin_sid = request.sid
    else:
        print(f"User {username} joined!")
        users[username] = request.sid
        session['username'] = username
    emit_user_list_update()

@socketio.on("remove_user")
def remove_user(username):
    if username in users:
        users.pop(username)
        emit_user_list_update()

@socketio.on("notify_user")
def get_user_sid(username):
    if username in users:
        emit("ring", room=users[username])
    
def emit_user_list_update():
    user_list = list(users.keys())

    emit("user_list_update", {"users": user_list, "isAdmin": False}, broadcast=True)

    if admin_sid:
        emit("user_list_update", {"users": user_list, "isAdmin": True}, room=admin_sid)

    for position, username in enumerate(user_list, start=1):
        emit("update_position", position, room=users[username])
