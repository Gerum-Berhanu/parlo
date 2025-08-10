import sqlite3
from scripts import *
from ast import literal_eval
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit, leave_room, join_room

conn = sqlite3.connect("database.db")
app = Flask(__name__)
app.config["SECRET_KEY"] = "13m22U18r5E7g"
socket = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    if "id" in session and "room" in session:
        s_id = session["id"]
        s_rm = session["room"]
        roomMembers = executeSql("SELECT room_members FROM rooms WHERE room_code = ?", [s_rm], True)
        if roomMembers:
            membersList = literal_eval(roomMembers[0][0])
            membersList.remove(s_id)
            membersList = str(membersList)
            if membersList == "[]":
                executeSql("DELETE FROM rooms WHERE room_code = ?", [s_rm])
            else:
                executeSql("UPDATE rooms SET room_members = ? WHERE room_code = ?", [membersList, s_rm])
    session.clear()
        
    if request.method == "POST":
        nick = request.form.get("nick")
        room = request.form.get("room")
        mode = request.form.get("mode").lower()
        
        if check_empty([nick, room, mode]): return json_response(400, "Bad Request", "Invalid form! Check your nickname or room code and try again.")
        if not check_mode(mode): return json_response(400, "Bad Request", "Invalid form submission! Refresh the page and try again.")
        if check_nick(nick) != 1: return json_response(400, "Bad Request", check_nick(nick))
        if check_room(room) != 1: return json_response(400, "Bad Request", check_room(nick))

        session_id = session_id_generator(nick)

        fromDb = executeSql("SELECT room_code FROM rooms WHERE room_code = ?", [room], response=True)
        if mode == "create":
            if fromDb:
                return json_response(403, "Forbidden", "Room already exists.")
            executeSql("INSERT INTO rooms (room_code) VALUES (?)", [room])
            executeSql("UPDATE rooms SET room_members = ? WHERE room_code = ?", [f'["{session_id}"]', room])
        if mode == "join":
            if not fromDb:
                return json_response(403, "Forbidden", "Room doesn't exist.")
            
            roomMembers = executeSql("SELECT room_members FROM rooms WHERE room_code = ?", [room], True)
            membersList = literal_eval(roomMembers[0][0])
            membersList.append(session_id)
            membersList = str(membersList)
            executeSql("UPDATE rooms SET room_members = ? WHERE room_code = ?", [membersList, room])

        session["id"] = session_id
        session["nick"] = nick
        session["room"] = room
        return json_response(302, "Moved Temporarily", "/room")
    return render_template("home.html")

@app.route("/room")
def room():
    if "id" not in session and "room" not in session:
        # return json_response(301, "Moved Permanently", "/")
        return redirect(url_for("home"))
    room_chats = executeSql("SELECT room_chats FROM rooms WHERE room_code = ?", [session["room"]], True)
    if room_chats and room_chats[0]:
        chats_list = literal_eval(room_chats[0][0])
    return render_template("room.html", chats=chats_list, room=session["room"], members=count_members(session["room"]))

@socket.on("connect")
def on_connect():
    if "id" not in session or "room" not in session: return
    s_id = session["id"]
    s_nk = session["nick"]
    s_rm = session["room"]
    rm_code = executeSql("SELECT room_code FROM rooms WHERE room_code = ?", [s_rm], True)
    if not rm_code:
        leave_room(s_rm)
        return
    
    room_members = executeSql("SELECT room_members FROM rooms WHERE room_code = ?", [s_rm], True)
    if room_members and room_members[0]:
        members_list = literal_eval(room_members[0][0])
        if s_id not in members_list:
            members_list.append(s_id)
        members_list = str(members_list)
        executeSql("UPDATE rooms SET room_members = ? WHERE room_code = ?", [members_list, s_rm])
            
    join_room(s_rm)
    send({"name": s_nk, "message": "has entered the room.", "members": count_members(session['room'])}, to=s_rm)
    # emit('notification', {"name": s_nk, "message": "has entered the room."}, broadcast=True)
    print(f"{s_nk} joined room {s_rm}\n  Members ~ {count_members(session['room'])}")

@socket.on("disconnect")
def on_disconnect():
    if "id" in session and "room" in session:
        s_id, s_nk, s_rm = session["id"], session["nick"], session["room"]
        room_members = executeSql("SELECT room_members FROM rooms WHERE room_code = ?", [s_rm], True)
        if room_members and room_members[0]:
            members_list = literal_eval(room_members[0][0])
            if s_id in members_list:
                members_list.remove(s_id)
            members_list = str(members_list)
            executeSql("UPDATE rooms SET room_members = ? WHERE room_code = ?", [members_list, s_rm])
        leave_room(s_rm)
        send({"name": s_nk, "message": "has left the room.", "members": count_members(session["room"])}, to=s_rm)
        # emit('notification', {"name": s_nk, "message": "has left the room."}, broadcast=True)
    print(f"{session['nick']} has disconnected!")

@socket.on("message")
def on_message(data):
    if "id" not in session or "room" not in session: return
    content = {
        "name": session["nick"],
        "message": data["data"],
        "members": count_members(session["room"])
        }
    room_chats = executeSql("SELECT room_chats FROM rooms WHERE room_code = ?", [session["room"]], True)
    if room_chats and room_chats[0]:
        chat_list = literal_eval(room_chats[0][0])
        chat_list.append(content)
        chat_list = str(chat_list)
        executeSql("UPDATE rooms SET room_chats = ? WHERE room_code = ?", [chat_list, session["room"]])
    send(content, to=session["room"])
    emit('notification', {"name": session["nick"], "message": data["data"]}, broadcast=True, include_self=False)
    print(f"{session['nick']} said ~ {data['data']}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)