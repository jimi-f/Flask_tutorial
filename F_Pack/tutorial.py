from flask import Flask, request, jsonify, render_template, session, g, redirect, url_for, abort, flash, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from contextlib import closing
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
os.urandom(24)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x010<!\xd5\xa2\xa0\x9fr"\xa1\xa8'
# api = Api(app)

# parser = reqparse.RequestParser()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jimi1310'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'List'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

# app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/showSignUp")
def show_sign_up():
    return render_template('signup.html')


@app.route("/main")
def main():
    return render_template('index.html')


@app.route("/showSignIn")
def show_sign_in():
    return render_template('signin.html')


@app.route("/signUp", methods=['POST', 'GET'])
def sign_up():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

    # validate the received values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': '' + _name + ' created successfully'})
                cursor.close()
                conn.close()
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/validateLogin', methods=['POST'])
def validate_login():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
                cursor.close()
                conn.close()
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/userHome')
def user_home():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/showAddWish')
def show_add_wish():
    return render_template('addWish.html')


@app.route('/addWish', methods=['POST'])
def add_wish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish', (_title, _description, _user))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('userHome')
                cursor.close()
                conn.close()
            else:
                return render_template('error.html', error='An error occurred!')
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/getWish', methods=['GET'])
def get_wish():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishByUser', (_user,))
            wishes = cursor.fetchall()
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/getTable', methods=['GET'])
def get_table():
    try:
        if request.method == 'GET':
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM tbl_user"
            cursor.execute(query)
            data = cursor.fetchall()
            if data is not None:
                return jsonify(data)
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return jsonify("Incorrect Method")
    except Exception as e:
        return jsonify('error', str(e))


@app.route('/updateTable', methods=['POST', 'GET'])
def update_table():
    try:
        if request.method == 'POST':
            input = request.get_json()
            user_name = input['user_name']
            user_password = input['user_password']
            user_username = input['user_username']
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "INSERT INTO tbl_user(user_name,user_username,user_password) VALUES(%s,%s,%s)"
            args = (user_name, user_username, user_password)
            cursor.execute(query, args)
            #print request.status_code
            data = cursor.fetchall()
            if data is not None:
                conn.commit()
                return jsonify({'code': 200, 'message': 'success'})
                cursor.close()
                conn.close()
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return jsonify("Incorrect Method")
    except Exception as e:
        return jsonify('error', str(e))


@app.route('/deleteEntry', methods=['DELETE'])
def delete_entry():
    try:
        if request.method == 'DELETE':
            input = request.get_json()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = 'DELETE FROM tbl_user WHERE user_id =' + str(input['id'])
            cursor.execute(query)
            conn.commit()
            return jsonify({'code': 200, 'message': 'success'})
        else:
            return 'you may not innit'
    except Exception as e:
        return jsonify('error', str(e))





# @app.route('/login', methods=['GET', 'POST'])
# def post(self):
    # if request.method == 'POST':
        # return jsonify(status='success')
    # else:
        # return jsonify(result="Nah", code="404")


# @app.route("/Authenticate")
# def Authenticate():
    # username = request.args.get('UserName')
    # password = request.args.get('Password')
    # cursor = mysql.connect().cursor()
    # cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    # data = cursor.fetchone()
    # if data is None:
        # return "Username or Password is wrong"
    # else:
        # return "Logged in successfully"


# class CreateUser(Resource):
    # def post(self):
        # return{'status':'success'}
# api.add_resource(CreateUser, '/CreateUser')

if __name__ == "__main__":
    app.run()
