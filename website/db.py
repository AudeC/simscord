import mysql.connector as sql

class DatabaseManager:
    def __init__(self):
        # Initialisation BDD
        self.cnx = sql.connect(user='jambot', password='5sd4f26e654zedjm5**',
                                      host='mysql-jambot.alwaysdata.net',
                                      database='jambot_bdd')
        self.cursor = self.cnx.cursor(buffered=True)

    # Récupération d'un bot dans la BDD
    def getBot(self, id):
        print("getBot :: "+str(id))
        query = ('SELECT * FROM Bot WHERE discord_id="'+id+'"')
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if len(res) == 0:
            return False
        return res[0]
        # cas du bot pas dans la base de données
        #return False

    # Insertion d'un bot dans la BDD
    def insertBot(self, name, discord_id):
        query = "INSERT INTO Bot(discord_id, name, type) VALUES (%s, %s, 'friend')"
        self.cursor.execute(query, (discord_id, name))
        self.cnx.commit()
        print(self.cursor.rowcount, " record inserted.")
        return True

    def updateBot(self, id, field, val):
        query = 'UPDATE Bot SET '+field+'=%s WHERE id=%s'
        self.cursor.execute(query, (val, str(id)))
        self.cnx.commit()
        return True

    # retourne toutes les expressions avec un code donné
    def getAllExpressions(self, code):
        query = ('SELECT * FROM Base_expression WHERE code="'+code+'"')
        self.cursor.execute(query)
        base = self.cursor.fetchall()[0][0]
        print("getAllExpressions :: "+code+" "+str(base))

        query2 = ('SELECT * FROM Expression WHERE base='+str(base))
        self.cursor.execute(query2)
        return self.cursor.fetchall()

    # Renvoie l'expression de base associée à une expression
    def findBaseExpr(self, exprID=-1, text=""):
        exprID = int(exprID)
        if exprID > -1:
            query = ('SELECT * FROM Base_expression WHERE id=%s')
            param = str(exprID)
        elif text != "":
            query = ('SELECT * FROM Base_expression WHERE text=%s')
            print("param text "+text)
            param = text.replace('"', '')
        else:
            return False
        self.cursor.execute(query, (param,))
        r = self.cursor.fetchall()
        if len(r) > 0:
            return r[0]
        return False

    # Recherche d'une expression
    def findExpr(self, msg):
        query = ('SELECT * FROM Expression WHERE text=%s')
        self.cursor.execute(query, (msg,))
        # Pour toute expression simple trouvée

        res = self.cursor.fetchall()
        if len(res) > 0:
            return ('simple', self.findBaseExpr(exprID=res[0][2]))

        # Aucune expression simple trouvée, on cherche une structure
        query = ('SELECT * FROM Expression')
        self.cursor.execute(query)
        msplit = msg.split(' ')
        # Pour toute expression
        for res in self.cursor:
            # TODO : Ne pas se limiter à la première qui match,
            # toutes les tester et prendre celle où le marqueur est
            # le plus court
            struct = res[1].split(' ')
            if len(struct) == 1:
                continue
            # recherche de si la phrase est la bonne
            sub = [item for item in struct if item not in msplit]
            if len(sub) == 1 and sub[0].startswith("%"):
                # recherche du marqueur
                sub2 = [item for item in msplit if item not in struct]
                # on retourne tous les infos
                return ('struct', self.findBaseExpr(str(res[2])), ' '.join(sub2))

        # Pas de structure trouvée, l'expression est inconnue
        return False

    def learnExpression(self, new, exp):
        # TODO: 1. on cherche si on connaît pas déjà l'expression

        # 2. on cherche si on reconnaît l'expression de base
        base = self.findBaseExpr(text=exp)
        if base is False:
            print("ne correspond à aucune base")
            return False
        base = base[0]
        query = "INSERT INTO Expression(text, base) VALUES (%s, %s)"
        self.cursor.execute(query, (new, base))
        self.cnx.commit()
        print(self.cursor.rowcount, " record inserted.")
        return True

    # retourne le bot qui correspond à "soi-même"
    def getSelf(self):
        query = ('SELECT * FROM Bot WHERE type="self"')
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if len(res) == 0:
            return False
        else:
            return res[0]

    def getBotAffect(self, target, target_type, source=-1):

        # Identification de la source
        sourceid = source
        if sourceid == -1:
            myself = self.getSelf()
            if myself is False:
                return False
            else:
                sourceid = myself[0]

        # Récupération de l'arget source->target
        print("SELECT AFFECT TOWARD "+str(target))
        query = 'SELECT value FROM Affect WHERE bot=%s AND target_type=%s AND target=%s'
        self.cursor.execute(query, (sourceid, target_type, target))
        res = self.cursor.fetchall()

        if len(res) == 0:
            # target inconnu, on initialise à la valeur donnée
            print("INSERT AFFECT 0 TO "+str(target))
            query = 'INSERT INTO Affect(bot, target, target_type, value) VALUES(%s,%s,%s,%s)'
            self.cursor.execute(query, (sourceid, target, target_type, 0))
            self.cnx.commit()
            return 0
        else:
            return res[0][0]

    # change l'affect du bot envers target (qui est un target_type)
    def changeAffectOfBot(self, target, target_type, value, source=-1):
        # Deux cas : on a déjà un avis sur target, ou on en a pas
        # ces deux cas sont gérés via getBotAffect
        # puisque si on connaît pas on crée la relation d'affect, init à 0
        current_affect = self.getBotAffect(target, target_type, source)

        newaffect = current_affect + value
        print("UPDATE AFFECT VAL TO "+str(target))
        query = 'UPDATE Affect SET value=%s WHERE target=%s AND target_type=%s'
        self.cursor.execute(query, (newaffect, target, target_type))
        self.cnx.commit()

        return True
