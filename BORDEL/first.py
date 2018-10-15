import mysql.connector as sql

cnx = sql.connect(user='jambot', password='5sd4f26e654zedjm5**',
                              host='mysql-jambot.alwaysdata.net',
                              database='jambot_bdd')

cursor = cnx.cursor()

query = ("SELECT name FROM Bot WHERE id=1")

cursor.execute(query)

for truc in cursor:
    print(truc)

cnx.close()
