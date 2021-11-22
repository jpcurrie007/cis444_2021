from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

from db_con import get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Get Books Handle Request")
    print("getting books")
    cur = global_db_con.cursor()
    cur.execute("SELECT bookName FROM books;")
    name = cur.fetchall();
    print(name)
    print("got the book names")
    cur.execute("SELECT bookPrice FROM books;")
    price = cur.fetchall();
    print(price)
    print("got the book prices")

    return json_response(token = create_token(g.jwt_data) , name = name , price = price)