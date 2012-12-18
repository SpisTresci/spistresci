from generic import  GenericConnector
from generic import XMLConnector
from virtualo import Virtualo


def main():
    konektory = [Virtualo()]
    
    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
        konektor.update()

if __name__ == '__main__':
    main()