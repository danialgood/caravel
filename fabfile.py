from contextlib import contextmanager as _contextmanager

from fabric.context_managers import cd, prefix, lcd
from fabric.operations import local, run
from fabric.state import env

from fabric.contrib.project import rsync_project

from superset import app
config = app.config

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

env.hosts = ['139.59.179.46']
env.user = 'caravel'
env.directory = 'caravel'
env.activate = 'source ~/caravelforkenv/bin/activate'
env.gpid = config.get("SUPERSET_GUNICORN_PID_DIR")

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def clear_cached_files():
    run('find . -name "*.pyc" -delete')

# Not Fucking Working Apparantly
def start():
    with virtualenv():
        clear_cached_files()
        print('starting Superset...')
        run('superset runserver -p 8088')


def stop():
    with virtualenv():
        print('Stopping Superset Server...')
        run('kill -QUIT $(cat %s)' % env.gpid)


def reload():
    with virtualenv():
        print('Restarting Superset Server...')
        run('kill -HUP $(cat %s)' % env.gpid)


def pull():
    with cd(env.directory):
        print('\npull..')
        run('git pull')


def migrate():
    print('\nmigrate')
    run('python manage.py migrate')


def collect_static():
    print('\ncollect static')
    run('python manage.py collectstatic')


def install_dependencies():
    with cd(env.directory):
        print('\ninstalling dependencies')
        run('pip3 install -r ./requirements.txt')

def rebuild():
    with virtualenv():
        print('\nrebuilding app')
        run('python3 setup.py install')

def push():
    print('\npush..')
    local('git push -u origin master')

def build_frontend():
    print('\nbuilding frontend app')
    with lcd(os.path.join(BASE_DIR, 'superset/assets')):
        local('npm run prod')


def rsync_frontend():
    print('\n rsyncing frontend app')
    rsync_project(remote_dir="caravel/superset/assets/dist/", local_dir="assets/dist/")


def collect():
    with virtualenv():
        collect_static()

def bdeploy():
    push()
    with virtualenv():
        pull()
        clear_cached_files()
        install_dependencies()
        rebuild()
        reload()

def deploy():
    push()
    build_frontend()
    rsync_frontend()
    with virtualenv():
        pull()
        clear_cached_files()
        install_dependencies()
        rebuild()
        reload()
