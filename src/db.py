# TODO : je te laisse faire Adrien, je crée juste les méthodes dont je me sers !
import mysql.connector as sql

class DatabaseManager:
    def __init__(self):
        # Initialisation BDD
        self.cnx = sql.connect(user='jambot', password='5sd4f26e654zedjm5**',
                                      host='mysql-jambot.alwaysdata.net',
                                      database='jambot_bdd')
        self.cursor = self.cnx.cursor()

    def getBot(self, id):
        query = ("SELECT * FROM Bot WHERE discord_id="+id)
        self.cursor.execute(query)
        for truc in self.cursor:
            return truc
        # cas du bot pas dans la base de données
        return False

    def insertBot(self, name, discord_id):
        # ... insertion du bot dans la BDD
        query = "INSERT INTO Bot(discord_id, name, type) VALUES (%s, %s, 'friend')"
        self.cursor.execute(query, (discord_id, name))
        self.cnx.commit()
        print(self.cursor.rowcount, " record inserted.")
        return True

    def findExpr(self, msg):
        query = ('SELECT * FROM Expression WHERE `text`="'+msg+'"')
        self.cursor.execute(query)
        for res in self.cursor:
            query = ('SELECT * FROM Base_expression WHERE id='+str(res[2]))
            self.cursor.execute(query)
            for r in self.cursor:
                return r
        return False
