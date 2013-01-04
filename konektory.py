from dobryebook import DobryEbook
from koobe import Koobe
from nexto import Nexto
from virtualo import Virtualo
from wolnelektury import fetch


def main():
    konektory = [DobryEbook(),
                 Virtualo()]
    
    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
        #konektor.update()

if __name__ == '__main__':
    main()
