from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import datetime

from tools.logging import logger

from db_con import get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Send chat Handle Request")
    cur = global_db_con.cursor()
    username = request.args.get('username')
    print(username)
    message = request.args.get('message')
    print(message)

    dbCmdForNewChat = "INSERT INTO chatlog(username, message) VALUES('"
    dbCmdForNewChat += str(username)
    dbCmdForNewChat += "','"
    dbCmdForNewChat += str(message)
    dbCmdForNewChat += "');"
    print(dbCmdForNewChat)
    cur.execute(dbCmdForNewChat)
    global_db_con.commit()

    dbCmdForNewChat = "INSERT INTO chatroom(username, message) VALUES('"
    dbCmdForNewChat += str(username)
    dbCmdForNewChat += "','"
    dbCmdForNewChat += str(message)
    dbCmdForNewChat += "');"
    print(dbCmdForNewChat)
    cur.execute(dbCmdForNewChat)
    global_db_con.commit()

    cur.execute("SELECT username FROM chatroom;")
    username = cur.fetchall();
    print(username)
    print("got the usernames")

    cur.execute("SELECT message FROM chatroom;")
    message = cur.fetchall();
    print(message)
    print("got the messages")

    return json_response(token = create_token(g.jwt_data), message = message, username = username)