from flask import Flask, request, jsonify, render_template, session, g, redirect, url_for, abort, flash, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
import os
import mysql.connector
from mysql.connector import Error

mysql = MySQL()
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jimi1310'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def post(self):
    if request.method == 'POST':

        return jsonify(status='success')
    else:
        return jsonify(result="Nah", code="404")

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"

class CreateUser(Resource):
    def post(self):
        return{'status':'success'}
api.add_resource(CreateUser, '/CreateUser')

if __name__ == "__main__":
    app.run()