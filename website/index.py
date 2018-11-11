 # /index.py

from flask import Flask, request, jsonify, render_template
import os
#import dialogflow
import requests
import json
import pusher
import time
import random
import asyncio

from main import BotClient

class MessageAuthor:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Message:
    def __init__(self, rq):
        self.content = rq['content']
        self.author = MessageAuthor(rq['author[id]'], rq['author[name]'])

app = Flask(__name__)
clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = Message(request.form)
    print(message)
    # On voit si on reconnaît l'auteur
    a = message.author
    if a.id not in clients:
        clients[a.id] = BotClient(a.id, a.name)

    rep = clients[a.id].on_message(message)
    response_text = { "message":  rep }
    time.sleep(random.choice((0, 1, 2, 3)))
    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run()
