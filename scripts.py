import sqlite3
import random
import json
from time import time
from ast import literal_eval
from typing import List, Any

def executeSql(sql: str, params: List[Any] = [], response: bool = False) -> Any:
    conn: str = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    if response:
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    conn.close()
    return result

def is_empty(element) -> bool:
    if not element: return True
    return False

def check_empty(array: List[Any]) -> bool:
    for element in array:
        if not str(element):
            return True
    return False

def check_mode(mode) -> bool:
    if mode.lower() != "join" and mode.lower() != "create":
        return False
    return True

def check_nick(nick) -> Any:
    if not (1 <= len(nick) <= 8): return "Nickname must be 8 characters or fewer."
    characters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    for n in nick:
        if n not in characters: return "Nickname must only contain uppercase letters, lowercase letters, or numbers."

    return 1

def check_room(code) -> Any:
    if len(code) != 8: return "Room code must be exactly 8 characters long."
    characters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    for c in code:
        if c not in characters: return "Room code must only contain uppercase letters, lowercase letters, or numbers."

    return 1

def count_members(room) -> int:
    room_members = executeSql("SELECT room_members FROM rooms WHERE room_code = ?", [room], True)
    if room_members:
        members_list = literal_eval(room_members[0][0])
        return int(len(members_list))

def session_id_generator(nickname: str) -> str:
    sessionId = ""

    # First - nickname
    sessionId += nickname

    # Second - identifier -=1%7=-
    sessionId += "-=1%7=-"

    # Third - timestamp
    tmp = str(int(time()))
    sessionId += tmp

    # Fourth - random 6 digits
    rnd = str(random.randint(100000, 999999))
    sessionId += "%" + rnd

    return sessionId

def json_response(code: int, title: str, text: Any) -> str:
    return json.dumps({"code": code, "title": title, "text": text})