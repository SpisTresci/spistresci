import ConfigParser
import sys

from connectors import *

def main():

    GenericConnector.read_config(GenericConnector)

    konektory = [ getattr(sys.modules[__name__],connector)()
                  for connector in GenericConnector.config_object.sections() ]

    for konektor in konektory:
        konektor.fetchData()
        konektor.parse()
 
        #konektor.update()


if __name__ == '__main__':
    main()
