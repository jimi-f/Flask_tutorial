from flask import Flask, request, jsonify, render_template, session, g, redirect, url_for, abort, flash, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
api = Api(app)

#parser = reqparse.RequestParser()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jimi1310'
app.config['MYSQL_DATABASE_DB'] = 'List'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#app.config.from_object(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

@app.route("/main")
def main():
    return render_template('index.html')

@app.route("/showSignIn")
def showSignIn():
    return render_template('signin.html')

@app.route("/signUp", methods=['POST'])
def signUp():
    try:
    # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

    # validate the received values
        if _name and _email and _password:
            conn = mysql.connect("localhost", "root", "jimi1310", "List")
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})

    finally:
        cursor.close()
        conn.close()


#@app.route('/login', methods=['GET', 'POST'])
#def post(self):
    #if request.method == 'POST':

        #return jsonify(status='success')
    #else:
        #return jsonify(result="Nah", code="404")

#@app.route("/Authenticate")
#def Authenticate():
    #username = request.args.get('UserName')
    #password = request.args.get('Password')
    #cursor = mysql.connect().cursor()
    #cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    #data = cursor.fetchone()
    #if data is None:
        #return "Username or Password is wrong"
    #else:
        #return "Logged in successfully"

#class CreateUser(Resource):
    #def post(self):
        #return{'status':'success'}
#api.add_resource(CreateUser, '/CreateUser')

if __name__ == "__main__":
    app.run()