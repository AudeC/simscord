import discord
import time
import random
TOKEN = "NDYzNjk0ODI4NzI3ODI4NTEx.Dh0I-Q.PzRrOSBecr9sSeDZdGHVWly5IlA"  # Get at discordapp.com/developers/applications/me
TOKEN2 = "NDYzNzEzMzQ1NTE4ODI5NTc4.Djp3TQ.51nIg9NNnhIpCA92bDslt1FI2uc"  # Get at discordapp.com/developers/applications/me

client = discord.Client()

class Friend:
    def __init__(self, user):
        self.user = user
        self.greeted = False
        self.howru = False

    def getUser(self):
        return self.user

    def howruDone(self):
        self.howru = True

async def say(channel, msg):
    await client.send_typing(channel)
    time.sleep(random.choice((1, 2, 3, 4)))
    # Après l'attente, si on voit que c'est plus nécessaire, on abandonne
    if session["interlocuteur"] != '' and amis[session["interlocuteur"]].howru == True and interpret(msg) == "Comment vas-tu ?":
        return
    await client.send_message(channel, msg)

tup_tvb = ("Comment vas-tu ?", "Ça va ?", "Comment va ?", "Bien ou bien ?")
tup_bet = ("Bien et toi ?", "Mal et toi ?", "Bof et toi ?")
tup_slt = ("Je suis parmi vous.", "Bien le bonjour !", "Salutations.", "Wesh par ici !", "Kikou.", "Hello~")
tup_tb = ("Très bien.", "Bof.", "Pas du tout..")
amis = {}
session = {}
session["interlocuteur"] = ""

# temporaire
def interpret(msg):
    if msg in tup_tvb:
        return "Comment vas-tu ?"
    if msg in tup_bet:
        return "Bien et toi ?"
    if msg in tup_tb:
        return "Très bien."

@client.event
async def on_message(message):
    '''
        RECEPTION D'UN MESSAGE
    '''
    # Le bot ne se répond pas lui-même
    if message.author == client.user:
        return
    # Message d'un bot
    elif message.author.bot:
        # Si un bot vient d'arriver
        if message.author.name not in amis:
            amis[message.author.name] = Friend(message.author)
            msg = 'Bonjour {0.author.mention} !'.format(message)
            await say(message.channel, msg)
            # pour l'instant on a que 2 bots, alors c'est pas illogique de
            # considérer tout nouvel arrivant comme interlocuteur
            session["interlocuteur"] = message.author.name
        # Si je reçois un message de mon interlocuteur
        if message.author.name == session["interlocuteur"]:
            if interpret(message.content) == "Comment vas-tu ?":
                await say(message.channel, random.choice(tup_bet))
                amis[session["interlocuteur"]].howruDone()
                return
            elif interpret(message.content) == "Bien et toi ?":
                await say(message.channel, random.choice(tup_tb))
                return
        # Cherche à continuer la conversation avec son interlocuteur
        if session["interlocuteur"] != '' and amis[session["interlocuteur"]].howru == False:
            await say(message.channel, random.choice(tup_tvb))
            amis[session["interlocuteur"]].howruDone()
            return

    # Exemple de commande
    elif message.content.startswith('!hello'):
        msg = 'Bonjour {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    '''
        BOT PRÊT
    '''
    # Dit bonjour sur le serveur de test
    hard_coded_channel = discord.Object(id="472164546769846290")
    await client.send_message(hard_coded_channel, random.choice(tup_slt))

    # jeu
    await client.change_presence(game=discord.Game(name="Phase de test"))

client.run(TOKEN)
