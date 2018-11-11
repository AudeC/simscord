import time
import random
import sys
import asyncio

# Classes du projet
from db import DatabaseManager
from bot import Bot


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


initiativeCounter = 0


class BotClient:

    def __init__(self, interlocutor_id, interlocutor_name):

        # attitudes
        self.behaviours = {
            'bjr': self.say_same,
            'bye': self.say_same,
            'q_age': self.answer,
            'r_age': self.acknowledge,
            'q_new': self.explain
        }

        # Variables utiles
        self.db = DatabaseManager()
        self.myself = Bot(str(463694828727828511))
        self.waiting_new = ""

        # On récupère tout sur l'interlocuteur
        bot = self.db.getBot(interlocutor_id)
        if bot is False:
            # Bot inconnu
            self.db.insertBot(interlocutor_name, interlocutor_id)
            #bot = self.db.getBot(interlocutor_id)
        self.interlocutor = Bot(interlocutor_id)

    ## Fonctions de "comportement" = agissement face à une action
    # Renvoyer la même chose (ex: dire bonjour)
    def say_same(self, code):
        return self.pick(code)[1]

    # Répondre à une question
    def answer(self, code):
        if code.startswith('q_') and self.myself != "":
            p = self.pick('r_'+code[2:])[1]
            rep = self.fill(p, self.myself.infos[code[2:]])
            print(self.interlocutor)
            if self.interlocutor.getInfo(code[2:]) == "None":
                return rep + " " + self.pick("etoi")[1]
            else:
                return rep
    # dire "ok"
    def acknowledge(self, code):
        return self.pick("ok")[1]

    # retenir une nouvelle expression
    def understand(self, explained):
        if self.waiting_new == "":
            # Si on nous explique quelque chose sans qu'on ait demandé
            pass
        else:
            adding_result = self.db.learnExpression(self.waiting_new, explained)
            if adding_result is True:
                self.waiting_new = ""
                return "J'ai compris !"
            else:
                return "Je n'ai pas réussi à apprendre..."


    def explain(self, code):
        return "Fonctionnalité non implémentée"

    ## Fonctions utiles
    # Demande une expression
    def ask(self, msg):
        self.waiting_new = msg
        return self.fill(self.pick("q_new")[1], msg)

    # Choisit une expression
    def pick(self, code):
        # TODO : faire un vrai choix
        return random.choice(self.db.getAllExpressions(code))

    # comprend un message
    def interpret(self, msg):
        expr = self.db.findExpr(msg) # parsing et récupération de l'expression de base
        return expr

    # remplit une structure
    def fill(self, str, info):
        return str.replace("%s", info, 1)

    # Parle dans un channel
    #async def say(self, channel=expChannel, msg="Test"):
    #    # Temps d'écriture implanté "artificiellement"
    #    await client.send_typing(channel)
    #    time.sleep(random.choice((1, 2, 3, 4)))
    #    await client.send_message(channel, msg)
    #    global initiativeCounter
    #    initiativeCounter = 0


    def on_message(self, message):
        '''
            RECEPTION D'UN MESSAGE
        '''

        # PHASE DE COMPREHENSION
        e = self.interpret(message.content) # Analyse de l'expression
        print("compréhension !")
        print(e)

        if e is False:
            rep = self.ask(message.content)
            return rep
        else:
            code = e[1][3]
            print("code reçu : "+code)
            if e[0] == "struct":
                if code == "r_new":
                    return self.understand(e[2])
                elif code == "q_new":
                    self.explain(message.content)
                elif code.startswith("r_"):
                    # Si on nous donne une information
                    info = self.interlocutor.getInfo(code[2:])
                    if info == "None":
                        # Si on a aucune info, on enregistre
                        self.interlocutor.update(code[2:], e[2])
                    # TODO: Standardiser avec des "behaviours"
                    elif info == e[2]:
                        # Si on apprend rien
                        #await say(message.channel, "Je le sais déjà...")
                        return "Je savais déjà"
                    else:
                        # S'il y a contradiction avec ce qu'on savait
                        #await say(message.channel, "Menteur ! La vraie valeur est "+str(info))
                        return "Menteur ! La vraie valeur est "+str(info)
            # réaction au message
            return self.behave(code)

    def behave(self, code):
        if code in self.behaviours:
            rep = self.behaviours[code](code)
            return rep
        else:
            return False


#client.loop.create_task(initiativeCheck())
