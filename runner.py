from scripts import *
from ast import literal_eval

executeSql("DELETE FROM rooms")

# room_chats = executeSql("SELECT room_chats FROM rooms WHERE room_code = ?", ["C0ePi6y4"], True)
# chats_list = literal_eval(room_chats[0][0])

# if chats_list: print(chats_list)
# else: print("No chats for the moment")