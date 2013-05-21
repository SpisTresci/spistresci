#!/usr/bin/python

#MasterTableChecker
from sqlwrapper import *
from Master import *

def main():

    SqlWrapper.password = ""
    SqlWrapper.username = "root"
    SqlWrapper.host = "127.0.0.1"
    SqlWrapper.scheme = "mysql"
    SqlWrapper.database = "master2"
    SqlWrapper.echo = False

    Session = sessionmaker(bind = SqlWrapper.getEngine())
    session = Session()

    #session.query(func.count(User.id)).group_by(User.name)

    #session.query(User).join((Group, User.groups)).join((Department, Group.departments)).filter(Department.name == 'R&D')

    masters = session.query(MasterAuthor).join(MiniAuthor, MasterAuthor.miniAuthor).all()
    m_dict = {}
    for m in masters:
        m_dict[m.name] = set()
        for miniAuthor in m.miniAuthor:
            m_dict[m.name].add(miniAuthor.name)

        m_dict[m.name].remove(m.name)

        if len(m_dict[m.name]) > 0:
            print "#" + m.name
            for s in m_dict[m.name]:
                print ">" + s
            print "\n"

    print "siedze na koniu"


if __name__ == '__main__':
    main()
