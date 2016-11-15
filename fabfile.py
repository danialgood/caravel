from contextlib import contextmanager as _contextmanager

from fabric.context_managers import cd, prefix
from fabric.operations import local, run
from fabric.state import env

from superset import app
config = app.config

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
        run('kill -QUIT -F ./gunicorn.pid')


def reload():
    run('uwsgi --reload ./uwsgi.pid')


def pull():
    print('\npull..')
    run('git pull')


def migrate():
    print('\nmigrate')
    run('python manage.py migrate')


def collect_static():
    print('\ncollect static')
    run('python manage.py collectstatic')


def install_dependencies():
    print('\ninstalling dependencies')
    run('pip install -r ./requirements.txt')


def push():
    print('\npush..')
    local('git push')


def collect():
    with virtualenv():
        collect_static()


def deploy():
    push()
    with virtualenv():
        pull()
        clear_cached_files()
        install_dependencies()
        migrate()
        reload()
