from dobryebook import DobryEbook
from koobe import Koobe
from nexto import Nexto
from virtualo import Virtualo
from wolnelektury import fetch
from helion import Helion
import ConfigParser

def main():
    konektory = [DobryEbook(),
                 Virtualo(),Helion(),Koobe(),Nexto()]
#    konektory = [Nexto()]
    
    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
        #konektor.update()


if __name__ == '__main__':
    main()
