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

@app.route('/chat')
def index():
    return render_template('index2.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    message = Message(request.form)
    print(message)

    # On voit si on reconnaît l'auteur
    a = message.author
    if a.id not in clients:
        clients[a.id] = BotClient(a.id, a.name)

    # TRAITEMENT DU MESSAGE
    rep = clients[a.id].on_message(message)

    # POST-PROCESSING : ajouter éventuellement de la ponctuation
    rep = rep.strip()
    print(rep[-1:])
    if rep[-1:] not in ['!', '.', '?']:
        rep = rep+'.'

    # Envoi de la réponse
    response_text = { "message":  rep,  "affect": clients[a.id].interlocutor.affect}
    time.sleep(random.choice((0, 1)))
    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run()
