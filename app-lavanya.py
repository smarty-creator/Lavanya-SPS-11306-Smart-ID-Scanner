from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os 
import pytesseract 
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image

project_dir =  os.path.dirname(os.path.abspath(__file__))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


app = Flask(__name__)
app.secret_key = 'a'
photos = UploadSet('photos',IMAGES)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'iCL6kK8XoN'
app.config['MYSQL_PASSWORD'] = '3r6dWefvLE'
app.config['MYSQL_DB'] = 'iCL6kK8XoN'
mysql = MySQL(app)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'images'


class GetText(object):
    
   def __init__(self , file):
       self.file = pytesseract.image_to_string(Image.open(project_dir + '/images/' + file))
       

@app.route('/')

def homer():
    return render_template('home8.html')



@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')



@app.route('/UPLOAD IMAGE',methods=['GET' , 'POST'])
def home():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'there is no photo in form'
        name = request.form['img-name'] + '.png' 
        
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOAD_FOLDER'],name)
              
        textObject = GetText(name)
        print('TEXT OBJECT' + textObject.file) 
        
        return textObject.file
    return render_template('image.html')


@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home8.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port = 8080)
                                             