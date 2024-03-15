from dashboard.calculation import *
import json
from flask import Flask, render_template, request, jsonify, Response, redirect
import pymysql

app = Flask(__name__)

def connect_database():
    return mysql.connect(
        host="localhost",
        user="root",
        passwd="CoolKid!23",
        database="users"
    )

@app.route('/',  methods=['GET', 'POST'])
def hello():
    return render_template('signin.html')

@app.route('/signin',  methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect('/')
    else:
        return render_template('signin.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/signin')  # Redirect to login page after successful registration

    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
