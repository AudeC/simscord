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
        query = ("SELECT * FROM Bot WHERE discord_id="+id)
        self.cursor.execute(query)
        for truc in self.cursor:
            return truc
        # cas du bot pas dans la base de données
        return False

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
        query2 = ('SELECT * FROM Expression WHERE id='+base)
        self.cursor.execute(query2)
        return self.cursor.fetchall()

    # Renvoie l'expression de base associée à une expression
    def findBaseExpr(self, exprID=0, text=""):
        if exprID > 0:
            query = ('SELECT * FROM Base_expression WHERE id='+str(exprID))
        elif text != "":
            query = ('SELECT * FROM Base_expression WHERE `text`="'+text+'"')
        else:
            return False
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Recherche d'une expression
    def findExpr(self, msg):
        query = ('SELECT * FROM Expression WHERE `text`="'+msg+'"')
        self.cursor.execute(query)
        # Pour toute expression simple trouvée
        for res in self.cursor:
            return ('simple', self.findBaseExpr(str(res[2])))

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
        base = findBaseExpr(text=exp)
