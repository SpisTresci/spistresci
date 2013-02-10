'''
Ligtweight meta class for implementing enums
    
Found at:
http://stackoverflow.com/questions/4472901/python-enum-class-with-tostring-fromstring
Author:
Pawel Prazak
http://stackoverflow.com/users/539481/pawel-prazak

Usage example:
class Animal(object):
  __metaclass__ = EnumMeta
    values = ['Horse','Dog','Cat']
'''
class EnumMeta(type):
    def __getattr__(self, name):
        return self.values.index(name)

    def __setattr__(self, name, value):  # this makes it read-only
        raise NotImplementedError

    def __str__(self):
        args = {'name':self.__name__, 'values':', '.join(self.values)}
        return '{name}({values})'.format(**args)

    def to_str(self, index):
        return self.values[index]


'''
Base class for enums used in konektory project
It simpe uses EnumMeta and implements int() method
'''
class Enum(object):
    __metaclass__ = EnumMeta
    values = []

    @classmethod
    def int(cls, name):
        try: 
            ind = cls.values.index(name)
        except ValueError:
            ind = -1
        finally:
            return ind
    
