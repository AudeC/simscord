import discord
import time
import random
import sys
from threading import Thread
from db import DatabaseManager

# Initialisation discord.py
TOKEN = "NDYzNjk0ODI4NzI3ODI4NTEx.Dh0I-Q.PzRrOSBecr9sSeDZdGHVWly5IlA"  # Get at discordapp.com/developers/applications/me
client = discord.Client()

# Classes utiles
# TODO : Déplacer dans un autre fichier
class Bot:
    def __init__(self, did):
        self.discord_id = did
        self.load()

    def load(self):
        b = db.getBot(self.discord_id)
        self.name = b[2]
        self.id = b[0]
        self.type = b[3]
        self.age = b[4]

class Conversation(Thread):

    # interlocutor : objet de type Bot
    def __init__(self, interlocutor):
        Thread.__init__(self)
        self.interlocutor = interlocutor
        self.paused = False


# Variables utiles
db = DatabaseManager()
activeConversations = []
endedConversation = []

# Fonctions utiles
async def say(channel, msg):
    # Temps d'écriture implanté "artificiellement"
    await client.send_typing(channel)
    time.sleep(random.choice((1, 2, 3, 4)))
    await client.send_message(channel, msg)

def interpret(msg):
    expr = db.findExpr(msg)
    return expr

@client.event
async def on_message(message):
    '''
        RECEPTION D'UN MESSAGE
    '''
    # Le bot ne se répond pas lui-même
    # TODO : après la phase de test, décommenter
    #if message.author == client.user:
    #    return

    # Le bot ne se répond pas lui-même
    if message.author == client.user:
        return

    # Message d'un bot
    bot = db.getBot(message.author.id)
    if bot is False:
        # Bot inconnu
        db.insertBot(message.author.name, message.author.id)
        await say(message.channel, "Enchanté !")
    else:
        # Bot reconnu
        print(bot)
        test = Bot(message.author.id)
        #await say(message.channel, "Je te connais, "+test.name+" !")
        e = interpret(message.content)
        if e is False:
            await say(message.channel, "Je n'ai rien compris.")
        else: 
            await say(message.channel, test.name+", tu m'as dit "+e[1])

@client.event
async def on_ready():
    '''
        BOT PRÊT
    '''

    # jeu
    await client.change_presence(game=discord.Game(name="parler (un peu)"))
    print(client.user.name)
    print(client.user.id)

client.run(TOKEN)
