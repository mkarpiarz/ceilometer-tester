import ConfigParser

class Config:
    def __init__(self, filename='config.cfg'):
        config = ConfigParser.ConfigParser()
        config.readfp(open(filename))
        self.host = config.get('mongo', 'host')
        self.port = config.get('mongo', 'port')
        self.database = config.get('mongo', 'database')
        self.username = config.get('mongo', 'username')
        self.password = config.get('mongo', 'password')
        self.ceilometer_endpoint = config.get('ceilometer', 'endpoint')

def main():
    conf = Config()
    print(conf.__dict__)

if __name__ == "__main__":
    main()
