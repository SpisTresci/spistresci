import ConfigParser
import sys

from connectors import *

def main():
    GenericConnector.config_file = 'conf/backup.ini'
    GenericConnector.read_config()

    konektory = [ getattr(sys.modules[__name__],connector)()
                  for connector in GenericConnector.config_object.sections() ]

    for konektor in konektory:
        konektor.fetchData()


if __name__ == '__main__':
    main()
