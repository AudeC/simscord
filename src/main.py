import discord
import time
import random
import sys
from threading import Thread
import mysql.connector as sql

# Initialisation BDD
cnx = sql.connect(user='jambot', password='5sd4f26e654zedjm5**',
                              host='mysql-jambot.alwaysdata.net',
                              database='jambot_bdd')
cursor = cnx.cursor()


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


class DatabaseManager:
    # TODO : je te laisse faire Adrien, je crée juste les méthodes dont je me sers !
    def __init__(self):
        self.db = ""
    def getBot(self, id):
        query = ("SELECT * FROM Bot WHERE discord_id="+id)
        cursor.execute(query)
        for truc in cursor:
            return truc
    # cas du bot pas dans la base de données
        return False
    def insertBot(self, name, discord_id):
        # ... insertion du bot dans la BDD
        query = "INSERT INTO Bot(discord_id, name, type) VALUES (%s, %s, 'friend')"
        cursor.execute(query, (discord_id, name))
        cnx.commit()
        print(cursor.rowcount, " record inserted.")
        return True

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
        await say(message.channel, "Je te connais, "+test.name+" !")


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
