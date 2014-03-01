import os
from datetime import datetime

from spistresci.settings import SITE_ROOT as DEV_PROJECT_ROOT
from django.conf import settings

from fabric.api import local, run, cd, lcd, env, sudo, get, parallel
from fabric.contrib.console import confirm
from fabric.decorators import runs_once


DEFAULT_DB_SETTINGS = settings.DATABASES['default']
if not DEFAULT_DB_SETTINGS['PASSWORD']:
    MYSQL_USER_PASSWD = 'mysql -u%s' % DEFAULT_DB_SETTINGS['USER']
else:
    MYSQL_USER_PASSWD = 'mysql -u%s -p\'%s\'' % (DEFAULT_DB_SETTINGS['USER'], DEFAULT_DB_SETTINGS['PASSWORD'])
MYSQL_EXEC_CMD = '%s -e' % MYSQL_USER_PASSWD

env.use_ssh_config = getattr(settings, 'FABRIC_USE_SSH_CONFIG', False)
REPOS = ["backends/spistresci", "backends/egazeciarz", "frontends/egazeciarz", 
    "frontends/spistresci", "frontends/common", "frontends/ekundelek"]

DEFAULT_SERVER_VIRTUAL_ENV_DIR = '/home/frontend/repo/'


def get_remote_mysql_pass_arg():
    """Return password argument for mysql commands (if pw is set)"""
    if env.database['PASSWORD']:
        return '-p\'%s\'' % env.database['PASSWORD']
    else:
        return ''

def staging():
    """Sets up the staging environment for fab remote commands"""
    from spistresci.settings.staging import SSH_HOSTS, DATABASES as STAGING_DATABASES
    env.user = 'root'
    env.hosts = SSH_HOSTS
    env.database = STAGING_DATABASES['default']
    env.remote_mysql_pw_arg = get_remote_mysql_pass_arg()
    env.port = 1337
    env.ENV = 'staging'
    env.CODE_DIR = DEFAULT_SERVER_VIRTUAL_ENV_DIR


def prod():
    """Sets up the prod environment for fab remote commands"""
    from spistresci.settings.prod import SSH_HOSTS, DATABASES as STAGING_DATABASES
    env.user = 'root'
    env.hosts = SSH_HOSTS
    env.database = STAGING_DATABASES['default']
    env.remote_mysql_pw_arg = get_remote_mysql_pass_arg()
    env.port = 1337
    env.ENV = 'prod'
    env.CODE_DIR = DEFAULT_SERVER_VIRTUAL_ENV_DIR



def _launch(full=False):
    """Launch new code. Does a git pull, migrate and bounce"""

    with cd(env.CODE_DIR):
        for repo in REPOS:
            path = os.path.join(env.CODE_DIR, repo)
            print path
            with cd(path):
                run('git pull')
        if full:
            run('pip install -r frontends/spistresci/requirements.pip')

        css_path = os.path.join(env.CODE_DIR, 'frontends/spistresci/static/css')
        scss_path = os.path.join(env.CODE_DIR, 'frontends/spistresci/static/scss')
        run('rm -rf %s && mkdir %s' % (css_path, css_path))
        run('sass --update %s:%s' % (css_path, scss_path))

        with cd(os.path.join(env.CODE_DIR, 'frontends')):
            run('python manage.py collectstatic --noinput')
            run('python manage.py collectstatic --noinput -i *.scss')
            run('find . -name \*.pyc -delete')
    bounce()


def quicklaunch():
    _launch(full=False)


def launch():
    _launch(full=True)


def bounce():
    sudo('sudo service apache2 restart', pty=False)
