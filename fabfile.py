"""
This fabfile currently works to deploy this repo and machine-learning to a new server.
A lot of settings and names will need to be changed around for your specific config, so
look through carefully.
"""

from __future__ import with_statement
from fabric.api import local, lcd, run, env, cd, settings, prefix, sudo, shell_env
from fabric.contrib.console import confirm
from fabric.operations import put
from fabric.contrib.files import exists

#Should be in the format user@remote_host
#env.hosts = ['vik@sandbox-service-api-001.m.edx.org']

# Deploy to Vagrant with:
# fab  -i /Users/nateaune/.rvm/gems/ruby-1.9.3-p374/gems/vagrant-1.0.7/keys/vagrant deploy

# TODO: make this configurable
env.hosts = ['vagrant@33.33.33.10']

# Usage:
# MacOSX: 
# fab -i /Applications/Vagrant/embedded/gems/gems/vagrant-1.0.3/keys/vagrant deploy
# On Nate's Mac using Homebrew:
# fab  -i /Users/nateaune/.rvm/gems/ruby-1.9.3-p374/gems/vagrant-1.0.7/keys/vagrant deploy         
# Debian/Ubuntu: 
# fab -i /opt/vagrant/embedded/gems/gems/vagrant-1.0.3/keys/vagrant deploy

#Can set this to be a path to a local keyfile if nonstandard
#env.key_filename = ''

# remote_user = 'vik'
remote_user = 'vagrant'
# local_user = 'vik'
local_user = 'nateaune'
ssh_key = 'github_rsa'

def prepare_deployment():
    #Make a local commit with latest changes if needed.
    local('git add -p && git commit')
    local("git push")

def deploy():
    #Setup needed directory paths
    #Edit if you are using this for deployment
    code_dir = '/opt/wwc/ml-service-api'
    ml_code_dir = '/opt/wwc/machine-learning'
    up_one_level_dir = '/opt/wwc'
    database_dir = '/opt/wwc/db'
    # TODO: make this configurable by the user
    # remote_ssh_dir = '/home/vik/.ssh'
    remote_ssh_dir = '/home/{0}/.ssh'.format(remote_user)
    # TODO: make this configurable by the user
    # local_dir = '/home/vik/mitx_all'
    local_dir = '/Users/nateaune/Dropbox/code/ml-service-api/ml-service-api'
    local_ssh_dir = '/Users/{0}/.ssh'.format(local_user)
    nltk_data_dir = '/usr/share/nltk_data'
    static_dir = '/opt/wwc/staticfiles'

    #this is needed for redis-server to function properly
    sudo('sysctl vm.overcommit_memory=1')
    #LCD defines the local directory

    # TODO: use ssh-add + ssh-agent to forward the Github credentials -> much SAFER!
    with lcd(local_ssh_dir), settings(warn_only=True):
        #Cd defines the remote directory
        with cd(remote_ssh_dir):
            #Move local keys that can access github to remote host
            #Highly recommend that you use a password for these!
            put(ssh_key, 'id_rsa', use_sudo=True)
            put(ssh_key + '.pub', 'id_rsa.pub', use_sudo=True)
            #Change permissions on keyfile to ensure that it can be used
            sudo('chmod 400 id_rsa')

    with settings(warn_only=True):
        #Stop services
        sudo('service celery stop')
        sudo('service ml-service-api stop')
        static_dir_exists = exists(static_dir, use_sudo=True)
        if not static_dir_exists:
            sudo('mkdir -p {0}'.format(static_dir))
        repo_exists = exists(code_dir, use_sudo=True)
        #If the repo does not exist, then it needs to be cloned
        if not repo_exists:
            sudo('apt-get install git python')
            up_one_level_exists = exists(up_one_level_dir, use_sudo=True)
            if not up_one_level_exists:
                sudo('mkdir -p {0}'.format(up_one_level_dir))
            with cd(up_one_level_dir):
                #TODO: Insert repo name here
                run('git clone git@github.com:edx/ml-service-api.git')

        sudo('chmod -R g+w {0}'.format(code_dir))

        #Check for the existence of the machine learning repo
        ml_repo_exists = exists(ml_code_dir, use_sudo=True)
        if not ml_repo_exists:
            with cd(up_one_level_dir):
                run('git clone git@github.com:edx/machine-learning.git')

        db_exists = exists(database_dir, use_sudo=True)
        if not db_exists:
            sudo('mkdir -p {0}'.format(database_dir))

        # TODO: should not be hardcoded to vik. For now, change to vagrant
        sudo('chown -R {0} {1}'.format(remote_user, up_one_level_dir))
        sudo('chmod -R g+w {0}'.format(ml_code_dir))

    with cd(ml_code_dir), settings(warn_only=True):
        #Update the ml repo
        run('git pull')

    with cd(code_dir), settings(warn_only=True):
        # With git...
        run('git pull')
        #Ensure that files are fixed
        run('sudo apt-get update')
        #This fixes an intermittent issue with compiling numpy
        run('sudo apt-get upgrade gcc')
        sudo('xargs -a apt-packages.txt apt-get install')
        #Activate your virtualenv for python
        result = run('source /opt/edx/bin/activate')
        if result.failed:
            #If you cannot activate the virtualenv, one does not exist, so make it
            sudo('apt-get install python-pip')
            sudo('pip install virtualenv')
            sudo('mkdir -p /opt/edx')
            sudo('virtualenv "/opt/edx"')
            # TODO: should not be hardcoded to vik
            sudo('chown -R {0} /opt/edx'.remote_user)

    with prefix('source /opt/edx/bin/activate'), settings(warn_only=True):
        #sudo('apt-get build-dep python-scipy')
        #Numpy and scipy are a bit special in terms of how they install
        run('pip install numpy==1.6.2')
        #This is needed to support the ml algorithm
        sudo('mkdir -p {0}'.format(nltk_data_dir))
        if not exists(nltk_data_dir):
            sudo('python -m nltk.downloader -d {0} all'.format(nltk_data_dir))
        # TODO: don't hardcode vik
        sudo('chown -R {0} {1}'.format(remote_user, nltk_data_dir))

        with cd(code_dir):
            run('pip install -r requirements.txt')

            # Sync django db and migrate it using south migrations
            run('python manage.py syncdb --noinput --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py migrate --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py createsuperuser --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py collectstatic -c --noinput --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py update_index --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            sudo('chown -R www-data {0}'.format(up_one_level_dir))

        with cd(ml_code_dir):
            sudo('xargs -a apt-packages.txt apt-get install')
            run('pip install -r pre-requirements.txt')
            run('pip install -r requirements.txt')
            run('python setup.py install')

    # with lcd(local_dir), settings(warn_only=True):
    #     with cd(up_one_level_dir):
    #         #Move env and auth.json (read by aws.py if using it instead of settings)
    #         put('service-auth.json', 'auth.json', use_sudo=True)
    #         put('service-env.json', 'env.json', use_sudo=True)
    #     with cd('/etc/init'):
    #         #Upstart tasks that start and stop the needed services
    #         put('service-celery.conf', 'celery.conf', use_sudo=True)
    #         put('service-ml-service-api.conf', 'ml-service-api.conf', use_sudo=True)
    #     with cd('/etc/nginx/sites-available'):
    #         #Modify nginx settings to pass through ml-service-api
    #         put('service-nginx', 'default', use_sudo=True)

    # #Start all services back up
    # sudo('service celery start')
    # sudo('service ml-service-api start')
    # sudo('service nginx restart')