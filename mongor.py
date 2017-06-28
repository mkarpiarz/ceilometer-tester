import config
import pymongo

class Mongor:
    def __init__(self):
        self.conf = config.Config()
        self.connect()

    def connect(self):
        self.client = pymongo.MongoClient(host = self.conf.host, port = int(self.conf.port))
        db = self.client[self.conf.database]
        db.authenticate(name=self.conf.username, password=self.conf.password, source=self.conf.database)
        print( db.collection_names() )

def main():
    mongor = Mongor()

if __name__ == "__main__":
    main()
