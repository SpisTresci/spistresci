from fabric.api import *

env.hosts=['solr1.spistresci.pl']
env.user='root'
env.port=1337

collections = [
    {
        'collection':'masterbook_latest',
    },
    {
        'collection':'masterbook_latest_bis',
    },
    {
        'collection':'masterbook_with_description_latest',
    },
    {
        'collection':'bookstore_latest',
    },
    {
        'collection':'bookstore_latest_bis',
    },
]


def deploy():

    with cd('/opt/solr'):

	with cd('configs/'):
            run('git pull')

        run('/usr/share/zookeeper/bin/zkServer.sh status')

        for dic in collections:
            run('bin/zkcli.sh -zkhost localhost:2181 -cmd upconfig -confdir /opt/solr/configs/%(collection)s/conf -confname %(collection)s' % dic)
            run('bin/zkcli.sh -zkhost localhost:2181 -cmd linkconfig -collection %(collection)s -confname %(collection)s' % dic)

    sudo('sudo service tomcat7 restart', pty=False)

