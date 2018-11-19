import time
import random
import sys
import asyncio

# Classes du projet
from db import DatabaseManager
from bot import Bot


class BotClient:

    def __init__(self, interlocutor_id, interlocutor_name):

        # attitudes
        self.behaviours = {
            'bjr': self.say_same,
            'bye': self.say_same,
            'q_age': self.answer,
            'q_ville': self.answer,
            'q_couleur':self.answer,
            'q_emploi': self.answer,
            'r_age': self.acknowledge,
            'r_ville': self.acknowledge,
            'r_couleur': self.acknowledge,
            'r_emploi': self.acknowledge,
            'q_new': self.explain
        }

        self.initiativeAllowed = ['bjr', 'r_age', 'r_ville', 'r_couleur', 'r_emploi', 'q_new']

        # sentiments (modificatuers d'affects)
        self.feelings = {
            'script': self.hate,
            'misunderstand': self.hate,
            'lie': self.anger,
            'repeat': self.anger,
            'similarity': self.enjoy,
            'r_new': self.enjoy,
            'bjr': self.enjoy,
            'q_age': self.like,
            'q_ville': self.like,
            'q_emploi': self.like,
            'q_new': self.like,
            'q_couleur':self.like,
            'r_age':self.enjoy,
            'r_emploi':self.enjoy,
            'r_couleur':self.enjoy,
            'r_ville':self.enjoy
        }

        self.modificators = {
            'hate':-0.2,
            'anger': -0.1,
            'joy':0.1,
            'like':0.2
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

    def initiativeCheck(self):
        # S'il se passe 1min sans qu'on dise quoi que ce soit
        # on pose une question au hasard
        print(self.interlocutor.infos)
        for info in self.interlocutor.infos:
            if self.interlocutor.infos[info] == 'None':
                return "q_"+info
        return False

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
                return rep + ". " + self.pick("etoi")[1]
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
                self.feel('understand', explained)
                return "J'ai compris !"
            else:
                self.feel('misunderstand', explained)
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

    # réagit conformément à ses comportements connus
    def behave(self, code):
        if code in self.behaviours:
            rep = self.behaviours[code](code)
            return rep
        else:
            return 'Je ne sais pas quoi dire.'

    def anger(self, code, info):
        self.interlocutor.changeAffect(self.myself.id, self.modificators['anger'])

    def enjoy(self, code, info):
        self.interlocutor.changeAffect(self.myself.id,self.modificators['joy'])

    def like(self, code, info):
        self.interlocutor.changeAffect(self.myself.id,self.modificators['like'])

    def hate(self, code, info):
        self.interlocutor.changeAffect(self.myself.id, self.modificators['hate'])

    # réagit conformément à son caractère
    def feel(self, code, info=False):
        if code in self.feelings:
            return self.feelings[code](code, info)
        else:
            return False


    def on_message(self, message):
        '''
            RECEPTION D'UN MESSAGE
        '''

        # PREPROCESSING
        message.content = message.content.strip()
        while(message.content[-1:] in ['.', '!', ' ']):
            message.content = message.content[:-1]

        # PHASE DE COMPREHENSION
        e = self.interpret(message.content) # Analyse de l'expression
        print("compréhension !")
        print(e)

        if e is False:
            rep = self.ask(message.content)
            self.feel('misunderstand')
            return rep
        else:
            code = e[1][3]
            print("code reçu : "+code)
            if e[0] == "struct":
                if code == "r_new":
                    self.feel('understand', e)
                    return self.understand(e[2])
                elif code == "q_new":
                    self.feel(code, e)
                    return self.explain(message.content)
                elif code.startswith("r_"):
                    # Si on nous donne une information
                    info = self.interlocutor.getInfo(code[2:])
                    if info == "None":
                        # Si on a aucune info, on enregistre
                        self.interlocutor.update(code[2:], e[2])
                    # TODO: Standardiser avec des "behaviours"
                    elif info == e[2]:
                        # Si on apprend rien
                        self.feel('repeat', e)
                        return "Je savais déjà."
                    else:
                        # S'il y a contradiction avec ce qu'on savait
                        self.feel('lie', e)
                        return "Tu aurais dû dire "+str(info)
            # éventuelle réaction
            self.feel(code, e)
            # retour d'une réponse (si pas déjà fait)
            rep = self.behave(code)
            if rep[-1:] not in ['!', '.', '?']:
                rep += '.'

            if code in self.initiativeAllowed and random.random() < self.interlocutor.affect:
                initiative = self.initiativeCheck()
                if initiative is False:
                    ini = ''
                else:
                    ini = self.pick(initiative)
                    return rep + ' ' + ini[1]

            return rep


#client.loop.create_task(initiativeCheck())
