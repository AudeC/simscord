from db import DatabaseManager


class Bot:
    def __init__(self, did):
        self.discord_id = did
        self.db = DatabaseManager()
        self.infos = {}
        self.defined = self.load()

    def load(self):
        b = self.db.getBot(self.discord_id)
        print("Bot.load ::")
        print(b)
        if b is False:
            return False
            
        self.name = b[2]
        self.id = b[0]
        self.type = b[3]
        self.infos = {}
        self.infos["age"] = str(b[4])
        return True

    def getInfo(self, field):
        return self.infos[field]

    def update(self, field, val):
        if self.db.updateBot(self.id, field, val) is True:
            self.infos[field] = str(val)
            return True
