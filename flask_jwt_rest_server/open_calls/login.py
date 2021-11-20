from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt

from db_con import get_db
global_db_con = get_db()

from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    cur = g.cursor()
    cur = global_db_con.cursor()
    dbCmdForGettingPass = "SELECT password FROM users WHERE username ='"
    dbCmdForGettingPass += request.form['username']
    dbCmdForGettingPass += "';"
    print(dbCmdForGettingPass)
    cur.execute(dbCmdForGettingPass)
    userPassword = cur.fetchone();
    print(userPassword[0])
    #below needed because we can have more then one use with same name
    #this needs fixing in the index.html page
    userPass = str(userPassword[0])
    password_from_user_form = request.form['password']
    if bcrypt.checkpw( bytes(password_from_user_form, 'utf-8'), userPass.encode('utf-8')):
        user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
        return json_response( token = create_token(user) , authenticated = True)
    return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )