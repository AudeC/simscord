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
        self.infos = {}
        self.infos["age"] = b[4]

    def getInfo(self, field):
        return self.infos[field]

    def update(self, field, val):
        if db.updateBot(self.id, field, val) is True:
            self.infos[field] = val
            return True

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
    expr = db.findExpr(msg) # parsing et récupération de l'expression de base
    # TODO : Analyser les retombées d'une expression
    return expr

@client.event
async def on_message(message):
    '''
        RECEPTION D'UN MESSAGE
    '''
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
        test = Bot(message.author.id)
        e = interpret(message.content) # Analyse de l'expression
        print(e)
        if e is False:
            await say(message.channel, "Je n'ai rien compris.")
        else:
            if e[0] == "struct":
                await say(message.channel, test.name+", tu m'as parlé de "+e[1][3]+" et tu m'as dit "+e[2])
                if e[1][3].startswith("r_"):
                    # Si on nous donne une information
                    info = test.getInfo(e[1][3][2:])
                    print(info)
                    if info is None:
                        # Si on a aucune info, on enregistre
                        test.update(e[1][3][2:], e[2])
                    elif info == e[2]:
                         await say(message.channel, "Je le sais déjà...")
                    else:
                        await say(message.channel, "Menteur ! La vraie valeur est "+str(info))
            else:
                await say(message.channel, test.name+", tu m'as dit "+e[1][1])

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
