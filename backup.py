from bezkartek import BezKartek
from dobryebook import DobryEbook
from helion import Helion
from koobe import Koobe
from nexto import Nexto
from virtualo import Virtualo
from wolnelektury import fetch
from generic import GenericConnector
import ConfigParser

def main():
    GenericConnector.config_file = 'conf/backup.ini'
    konektory = [BezKartek(),
            DobryEbook(),
            Helion(),
            Koobe(),
            Nexto(),
            Virtualo()]


    
    for konektor in konektory:
        konektor.fetchData()


if __name__ == '__main__':
    main()
