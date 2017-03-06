from fabric.api import local, run, settings, roles, abort, cd, env
from fabric.operations import get, put
from fabric.contrib.console import confirm

env.roledefs = {
    'int': ['web@astroedu.local'],
    'prod': ['web@astroedu.iau.org'],
}


def hello():
    print('Boa Tarde!')
    run('uname -a')
    # run('uname -m')  # i686 = 32bit; x86_64 = 64bit


def int():
	'''select the integration server'''
	env.hosts = env.roledefs['int']

def prod():
	'''select the production server'''
	if confirm('Deploying to the production server. Proceed?'):
		env.hosts = env.roledefs['prod']


def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm('Tests failed. Continue anyway?'):
        abort('Aborting at user request.')

def commit():
    local('git add -p && git commit')

def push():
    local('git push')

def prepare_deploy():
    test()
    commit()
    push()


def copy_secrets():
	put('astroedu/secrets.py','astroedu/astroedu/secrets.py')

def deploy():
    code_dir = '/home/web/astroedu'

    # clone git repo if not existing
    with settings(warn_only=True):
        if run('test -d %s' % code_dir).failed:
            run('git clone https://github.com/unawe/astroedu.git %s' % code_dir)

    with cd(code_dir):
    	# update code from public git repo
        run('git pull')
        # copy secrets.py
        copy_secrets()
        ## TODO: collect static
        #run('./manage.py collectstatic -v0 --noinput')
        # restart uWSGI
        run('touch app.wsgi')


@roles('prod')
def clone_db():
	# get database dump
	## TODO: force dump
	result = get('astroedu_backups/database.sql.gz', '/tmp')
	print result.succeeded
	for f in result:
		print f
	# get file uploads
	## TODO: get _latest_ backup
	result = get('astroedu_backup_archives/uploads/hourly/uploads-2014-10-14-1234.tar.gz', '/tmp')
	print result.succeeded
	for f in result:
		print f

