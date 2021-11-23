from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import datetime

from tools.logging import logger

from db_con import get_db
global_db_con = get_db()

def handle_request():
    logger.debug("Buy Book Handle Request")
    cur = global_db_con.cursor()
    book = request.args
    print(book)
    print(book[1])
    timeOfPurchase = datetime.datetime.now()
    #print(timeOfPurchase)
    dbCmdForBuyingBook = "INSERT INTO booksBought(bookName, time) VALUES('"
    dbCmdForBuyingBook += str(book)
    dbCmdForBuyingBook += "','"
    dbCmdForBuyingBook += str(timeOfPurchase)
    dbCmdForBuyingBook += "');"
    #print(dbCmdForBuyingBook)
    cur.execute(dbCmdForBuyingBook)
    global_db_con.commit()

    return json_response(token = create_token(g.jwt_data) , message = "Thank you for buying one of my books :)")