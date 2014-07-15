#TODO: In my opinion list of classes to import from GenericConnector should be managed in that file
# using __all__ attribute, and the only think here should be 
#from GenericConnector import *
from GenericConnector import GenericConnector
from GenericConnector import GenericBook
from GenericConnector import GenericISBN
from GenericConnector import GenericAuthor
from GenericConnector import GenericBookPrice
from GenericConnector import GenericBooksAuthors
from GenericConnector import GenericBase
from GenericConnector import WrongConnectorModeException

from XMLConnector import XMLConnector

from ReferenceConnector import ReferenceConnector

from MARCConnector import MARCConnector

from JSONConnector import JSONConnector

from OAIConnector import OAIConnector
