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
        print("findBaseExpr ::")
        print(r)
        if len(r) > 0:
            return r[0]
        return False

    # Recherche d'une expression
    def findExpr(self, msg):
        query = ('SELECT * FROM Expression WHERE text=%s')
        self.cursor.execute(query, (msg,))
        # Pour toute expression simple trouvée
        for res in self.cursor:
            return ('simple', self.findBaseExpr(exprID=res[2]))

        # Aucune expression simple trouvée, on cherche une structure
        query = ('SELECT * FROM Expression')
        self.cursor.execute(query)
        msplit = msg.split(' ')
        # Pour toute expression
        for res in self.cursor:
            struct = res[1].split(' ')
            if len(struct) == 1:
                continue
            # recherche de si la phrase est la bonne
            sub = [item for item in struct if item not in msplit]
            if len(sub) == 1:
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
