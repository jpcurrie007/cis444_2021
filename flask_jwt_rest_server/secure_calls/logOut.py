from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

from db_con import get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Log out Handle Request")

    cur = global_db_con.cursor()

    username = request.args.get('username')
    print(username)

    dbCmdFordeletingChat = "DELETE FROM chatroom WHERE username='"
    dbCmdFordeletingChat += str(username)
    dbCmdFordeletingChat += "';"
    print(dbCmdFordeletingChat)
    cur.execute(dbCmdFordeletingChat)
    global_db_con.commit()

    message = " has left the chatroom!"

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

    return json_response(token = create_token(g.jwt_data))