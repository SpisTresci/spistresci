from virtualo.Virtualo import Virtualo
from dobryebook.DobryEbook import DobryEbook


def main():
    konektory = [DobryEbook(),
                 Virtualo()]
    
    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
        #konektor.update()

if __name__ == '__main__':
    main()