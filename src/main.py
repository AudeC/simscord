import discord
import time
import random
import sys
import asyncio

# Classes du projet
from db import DatabaseManager
from bot import Bot

# Initialisation discord.py
TOKEN = "NDYzNjk0ODI4NzI3ODI4NTEx.Dh0I-Q.PzRrOSBecr9sSeDZdGHVWly5IlA"  # Get at discordapp.com/developers/applications/me
client = discord.Client()

async def initiativeCheck():
    # S'il se passe 1min sans qu'on dise quoi que ce soit
    # on pose une question au hasard
    await client.wait_until_ready()
    global currentChannel
    global interlocutor
    global initiativeCounter
    while not client.is_closed:
        initiativeCounter +=1
        if initiativeCounter >= 60 and interlocutor != "":
            for info in interlocutor.infos:
                if interlocutor.infos[info] is None:
                    expr = pick("q_"+info)
                    print(expr)
                    await say(currentChannel, expr[1])
                    break
        await asyncio.sleep(1)

# Variables utiles
db = DatabaseManager()
activeConversations = []
endedConversation = []
interlocutor = ""
currentChannel = None
expChannel = discord.Object(id='463696422756155413')
initiativeCounter = 0
myself = ""


## Fonctions de "comportement" = agissement face à une action
# Renvoyer la même chose (ex: dire bonjour)
async def say_same(code):
    global currentChannel
    p = pick(code)[1]
    await say(currentChannel,p)

# Répondre à une question
async def answer(code):
    global currentChannel
    global interlocutor
    if code.startswith('q_') and myself != "":
        p = pick('r_'+code[2:])[1]
        rep = fill(p, myself.infos[code[2:]])
        await say(currentChannel,rep)
        if interlocutor.getInfo(code[2:]) == "None":
            await say(currentChannel, pick("etoi")[1])
# dire "ok"
async def acknowledge(code):
    global currentChannel
    p = pick("ok")[1]
    await say(currentChannel,p)

behaviours = {
    'bjr': say_same,
    'q_age': answer,
    'r_age': acknowledge
}


# Fonctions utiles
## Parle dans un channel
async def say(channel=expChannel, msg="Test"):
    # Temps d'écriture implanté "artificiellement"
    await client.send_typing(channel)
    time.sleep(random.choice((1, 2, 3, 4)))
    await client.send_message(channel, msg)
    global initiativeCounter
    initiativeCounter = 0

## Choisit une expression
def pick(code):
    # TODO : faire un vrai choix
    return random.choice(db.getAllExpressions(code))

## comprend un message
def interpret(msg):
    expr = db.findExpr(msg) # parsing et récupération de l'expression de base
    # TODO : Analyser les retombées d'une expression
    # (implique probablement de déplacer ce qui est actuellement dans
    # on_message(). )
    return expr

## remplit une structure
def fill(str, info):
    return str.replace("%s", info, 1)

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
        return

    global interlocutor
    global currentChannel

    # Bot reconnu
    # PHASE DE COMPREHENSION
    if interlocutor == "":
        # pas encore d'interlocuteur
        interlocutor = Bot(message.author.id)
        currentChannel = message.channel
    elif interlocutor.discord_id != message.author.id:
        # interlocuteur différent
        # pour l'instant on ignore, donc le bot ne parle qu'à la première
        # personne qui lui adresse la parole
        return

    e = interpret(message.content) # Analyse de l'expression
    print(e)
    if e is False:
        await say(message.channel, "Je n'ai rien compris.")
    else:
        code = e[1][3]
        if e[0] == "struct":
            if code.startswith("r_"):
                # Si on nous donne une information
                info = interlocutor.getInfo(code[2:])
                if info == "None":
                    # Si on a aucune info, on enregistre
                    interlocutor.update(code[2:], e[2])
                # TODO: Standardiser avec des "behaviours"
                elif info == e[2]:
                    # Si on apprend rien
                    await say(message.channel, "Je le sais déjà...")
                else:
                    # S'il y a contradiction avec ce qu'on savait
                    await say(message.channel, "Menteur ! La vraie valeur est "+str(info))
        # réaction au message
        if code in behaviours:
            await behaviours[code](code)

@client.event
async def on_ready():
    '''
        BOT PRÊT
    '''

    # jeu
    await client.change_presence(game=discord.Game(name="parler (un peu)"))
    print(client.user.name)
    print(client.user.id)

    global myself
    myself = Bot(client.user.id)

client.loop.create_task(initiativeCheck())

client.run(TOKEN)
