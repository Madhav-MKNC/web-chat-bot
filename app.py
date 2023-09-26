#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, redirect, url_for, session, jsonify

import json
import hashlib
from functools import wraps

from utils import *
import chatbot

import os
from dotenv import load_dotenv
load_dotenv()


# Initialzing flask app
app = Flask(__name__)

# secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Change this to a strong random key in a production environment

# for verifying if the user is logged in 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


"""
Routes below:
/                   => chatbot login page
/chat               => chatbot page
/get_chat_response  => get chatbot response
/logout             => user logout
"""

# index -> login
@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('authenticated'):
        return redirect(url_for("chat"))
    
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

# get response from chatbot
@app.route('/get_chat_response', methods=['POST'])
def get_chat_response():
    user_input = request.json['message']
    chat_history = request.json['conversationHistory']

    # truncate the chat_history
    chat_history.reverse()
    conversation = []
    for chat in chat_history:
        if len(str(conversation)) > 2000: # 2000 characters is the currect limit
            break 
        conversation.append(chat)
    chat_history = conversation[::-1]
    # for i in chat_history:
    #     print(i)

    response = chatbot.get_response(query=user_input, chat_history=chat_history)
    return jsonify({'message': response})

# logout
@app.route('/logout')
def logout():
    # Clear the authenticated status from the session
    session.pop('authenticated', None)
    return redirect(url_for('login'))



# run server
def start_chat_server():
    app.run(host="0.0.0.0", port=8081, debug=True)


if __name__ == '__main__':
    start_chat_server()
