class Resource:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __str__(self):
        return "ID: %s, TYPE: %s" % (self.id, self.type)

def main():
    res = Resource('test-id', 'test-type')
    print(res)

if __name__ == "__main__":
    main()
