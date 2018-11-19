from db import DatabaseManager


class Bot:
    def __init__(self, did):
        self.discord_id = did
        self.db = DatabaseManager()
        self.infos = {}
        self.defined = self.load()
        self.affect = 0

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
        self.infos["couleur"] = str(b[5])
        self.infos["emploi"] = str(b[6])
        self.infos["ville"] = str(b[7])

        if self.type != 'self':
            self.affect = self.db.getBotAffect(self.id, 'bot')

        return True

    def getInfo(self, field):
        return self.infos[field]

    def update(self, field, val):
        if self.db.updateBot(self.id, field, val) is True:
            self.infos[field] = str(val)
            return True
        return False

    def changeAffect(self, source, val):
        if self.db.changeAffectOfBot(self.id, 'bot', val, source) is True:
            self.affect += val
            return self.affect
        return False
