import ceilomarius
from datetime import datetime

#class Paginator:
#    def __init__(self):

def main():
    now = "{:%Y-%m-%dT%H:%M:%S.%f}".format(datetime.now())
    print(now)

if __name__ == "__main__":
    main()
