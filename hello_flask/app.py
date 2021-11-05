from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    #dont use below, got from hannah but doesnt work for me
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['password'],  'utf-8' )  , salted ))
    
    cur = global_db_con.cursor()
    cur.execute("select * from books;")
    bookList = '{"books":['
    while True:
        book = cur.fetchone()
        if book is None:
            break
        else:
            bookList += ", "
            bookId=str(book[0])
            bookName=str(book[1])
            bookDescription=str(book[2])
            bookList += '{"bookId": "'+ bookId + '", "bookName": "' + bookName + '", "bookDescription": "' + bookDescription + '"}'
    bookList +=']}'
    
    return json_respone(data=bookList)

@app.route('/getBooksOldVersion', methods=['POST']) #endpoint dont use this jp, dont be a dumb dumb
def getBooks():
    cur = global_db_con.cursor()
    cur.execute('SELECT bookName FROM books;')
    bookNames = cur.fetchall()
    print(bookNames)
    cur.execute('SELECT bookId FROM books;')
    booksID = cur.fetchall()
    print(booksID)

    return json_response(bookNames=bookNames,booksID=booksID)


@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()), hello= "JP")

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")



#Assingment 3



@app.route('/getBooks', methods = ['GET']) #endpoint
def retrieveBooks():
    #print("getting books")
    cur = global_db_con.cursor()
    cur.execute("SELECT bookName FROM books;")
    name = cur.fetchall();
    #print("got the book names")
    cur.execute("SELECT bookPrice FROM books;")
    price = cur.fetchall();
    #print("got the book prices")
    return json_response(name = name, price = price)


@app.route('/userAuth', methods = ['POST']) #endpoint
def userAuth():
    #print(request.form)
    cur = global_db_con.cursor()
    dbCmdForGettingPass = "SELECT password FROM users WHERE username ='"
    dbCmdForGettingPass += request.form['username']
    dbCmdForGettingPass += "';"
    #print(dbCmdForGettingPass)
    cur.execute(dbCmdForGettingPass)
    userPassword = cur.fetchone();
    #print(userPassword[0])
    #below needed because we can have more then one use with same name
    #fix this in the static page
    userPass = str(userPassword[0])
    if bcrypt.checkpw( bytes(request.form['password'], 'utf-8'), userPass.encode('utf-8')):
        return "VALID"
    return "INVALID"


@app.route('/createNewUser', methods = ['POST']) #endpoint
def createNewUser():
    #print(request.form)
    newUser = request.form['username']
    #print(newUser)
    newPassword = request.form['password']
    #print(newPass)
    saltedPassword = bcrypt.hashpw(bytes(newPassword, 'utf-8'), bcrypt.gensalt(10))
    dbCmdForNewUser = "INSERT INTO users(username, password) VALUES('"
    dbCmdForNewUser += str(newUser)
    dbCmdForNewUser += "','"
    dbCmdForNewUser += str(saltedPassword.decode('utf-8'))
    dbCmdForNewUser += "');"
    #print(dbCmdForNewUser)
    cur = global_db_con.cursor()
    cur.execute(dbCmdForNewUser)
    global_db_con.commit()
    return "VALID"
    #should add way to return if there was an issue adding user to db, different then form check

@app.route('/purchaseBook', methods = ['POST']) #endpoint
def purchaseBook():
##note to self, the commented out code below does not help secuirty but does work, ask cary why

#    print(request.form)
#    cur = global_db_con.cursor()
#    dbCmdForValidatingUser = "SELECT password FROM users WHERE username ='"
#    dbCmdForValidatingUser += request.form['username']
#    dbCmdForValidatingUser += "';"
#    #print(dbCmdForValidatingUser)
#    cur.execute(dbCmdForValidatingUser)
#    userPassword = cur.fetchone();
#    #print(userPassword[0])
#    userPass = str(UserPassword[0])
#    if bcrypt.checkpw( bytes(request.form['password'], 'utf-8'), userPass.encode('utf-8')):
    #print("buying book")
    cur = global_db_con.cursor()
    bookName = request.form['book']
    #print(bookName)
    timeOfPurchase = datetime.datetime.now()
    #print(timeOfPurchase)
    dbCmdForBuyingBook = "INSERT INTO booksBought(bookName, time) VALUES('"
    dbCmdForBuyingBook += str(bookName)
    dbCmdForBuyingBook += "','"
    dbCmdForBuyingBook += str(timeOfPurchase)
    dbCmdForBuyingBook += "');"
    #print(dbCmdForBuyingBook)
    cur.execute(dbCmdForBuyingBook)
    global_db_con.commit()
    return "Book Bought!"
#    return "book not bought!"
# should add a way to add a user to this as well

app.run(host='0.0.0.0', port=80)

