# from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import BaseRunserverCommand
# from django.core.management import call_command
# from django.conf import settings
# import subprocess
# from termcolor import colored, cprint
# from time import sleep
# from threading import Thread, Lock
#
# def runsolr_(lock):
#     lock.acquire()
#     solr = subprocess.Popen(["python manage.py runsolr"],
#                 shell=True,
#                 stdin=subprocess.PIPE,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 )
#
#     while True:
#             line = solr.stdout.readline()
#             if line != '':
#                 line = line.rstrip()
#                 print colored('SOLR: ', 'yellow', attrs=['bold']), line
#                 if "Started SocketConnector" in line:
#                     host = line[line.index("@")+1:]
#                     print colored('SOLR started: ', 'yellow', attrs=['bold']), colored('http://%s/solr/' % host, 'green', attrs=['bold'])
#                     lock.release()
#             else:
#                 break
#
#

class Command(BaseRunserverCommand):

    def inner_run(self, *args, **options):
        return super(Command, self).inner_run(*args, **options)
        # lock = Lock()
        # t1 = Thread(target=runsolr_, args=(lock,))
        # t1.start()
        # static = settings.STATICFILES_DIRS[0]
        # sass = subprocess.Popen(["sass --line-numbers --watch %sscss/:%scss/" % (static, static)],
        #             shell=True,
        #             stdin=subprocess.PIPE,
        #             stdout=self.stdout,
        #             stderr=self.stderr)
        # self.stdout.write("sass --watch process on %r\n" % sass.pid)
        #
        # lock.acquire()


