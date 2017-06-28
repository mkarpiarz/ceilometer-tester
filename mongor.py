import config
import pymongo

class Mongor:
    def __init__(self):
        self.conf = config.Config()
        self.connect()

    def connect(self):
        self.client = pymongo.MongoClient(host = self.conf.host, port = int(self.conf.port))

def main():
    mongor = Mongor()
    print( mongor.client.server_info() )

if __name__ == "__main__":
    main()
