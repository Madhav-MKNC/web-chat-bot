#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

import json
import hashlib
from functools import wraps

import os
from dotenv import load_dotenv
load_dotenv()


# Initialzing flask app
app = Flask(__name__)

# secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Change this to a strong random key in a production environment

# Load admin users from the JSON file
USERS_FILE = 'users.json'

def load_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
    return users

USERS = load_users()
def is_authenticated(username, password):
    # Check if the provided username and password match any admin user
    for user in USERS:
        if user['username'] == username and hashlib.sha256(user['password'].encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


"""
Routes below:
/           => chatbot login page
/chat       => admin dashboard

/logout     => user logout
"""

# index -> login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if is_authenticated(username, password):
            # Save the authenticated status in the session
            session['authenticated'] = True
            return redirect(url_for('chat'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# chat
@app.route('/chat')
@login_required
def chat():
    # Check if the user is authenticated in the session
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    return render_template('chat.html')

# logout
@app.route('/logout')
def logout():
    # Clear the authenticated status from the session
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# run server
def start_server():
    app.run(host="0.0.0.0", port=8081, debug=True)


if __name__ == '__main__':
    start_server()
