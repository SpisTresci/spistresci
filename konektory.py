from bezkartek import BezKartek
from dobryebook import DobryEbook
from helion import Helion
from koobe import Koobe
from nexto import Nexto
from rw2010 import RW2010
from virtualo import Virtualo
from wolnelektury import fetch
import ConfigParser

def main():
    konektory = [BezKartek(),DobryEbook(),Helion(),Koobe(),Nexto(),RW2010(),Virtualo()]
    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
        #konektor.update()


if __name__ == '__main__':
    main()
