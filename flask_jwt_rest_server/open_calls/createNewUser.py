from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt

from db_con import get_db
global_db_con = get_db()

from tools.logging import logger

def handle_request():
    logger.debug("New user Handle Request")
    print(request.form)
    newUser = request.form['username']
    print(newUser)
    newPassword = request.form['password']
    print(newPassword)
    saltedPassword = bcrypt.hashpw(bytes(newPassword, 'utf-8'), bcrypt.gensalt(10))
    dbCmdForNewUser = "INSERT INTO users(username, password) VALUES('"
    dbCmdForNewUser += str(newUser)
    dbCmdForNewUser += "','"
    dbCmdForNewUser += str(saltedPassword.decode('utf-8'))
    dbCmdForNewUser += "');"
    print(dbCmdForNewUser)
    cur = global_db_con.cursor()
    cur.execute(dbCmdForNewUser)
    global_db_con.commit()

    return json_response(status=200, message = "New User Created!")