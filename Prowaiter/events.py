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

    original_username = username
    counter = 1
    while username in users:
        username = f"{original_username} ({counter})"
        counter += 1
    
    if username == "admin" and not admin_sid:
        admin_sid = request.sid
        session['admin'] = True  # Mark the session as admin
    else:
        print(f"User {username} joined!")
        users[username] = request.sid
        session['username'] = username
        session.pop('admin', None)  # Remove admin status if present

    emit('username_assigned', {'username': username}, room=request.sid)
    emit_user_list_update()

@socketio.on("reconnect")
def reconnect(username):
    global admin_sid

    if username == "admin":
        admin_sid = request.sid
        session['admin'] = True  # Mark the session as admin
    else:
        print(f"User {username} rejoined!")
        users[username] = request.sid
        session['username'] = username
        session.pop('admin', None)  # Remove admin status if present

    emit_user_list_update()

@socketio.on("remove_user")
def remove_user(username):
    if username in users:
        users.pop(username)
        session.pop('username', None)
        session.pop('admin', None)
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
