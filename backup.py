from afiliant import Audiobook,Audioteka,Legimi
from bezkartek import BezKartek
from dobryebook import DobryEbook
from helion import Helion
from koobe import Koobe
from nexto import Nexto
from rw2010 import RW2010
from virtualo import Virtualo
#from wolnelektury import fetch
from generic import GenericConnector
import ConfigParser

def main():
    konektory = [ 
    Audiobook(),
    Audioteka(),
    BezKartek(),
    DobryEbook(),
    Helion(),
    Legimi(),
    Koobe(),
    Legimi(),
    Nexto(),
    RW2010(),
    Virtualo(),]

    for konektor in konektory:
        konektor.fetchData()


if __name__ == '__main__':
    main()
