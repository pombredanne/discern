=================================
Installation Overview
=================================

There are two ways to install the Discern project:

1) Manually using the following instructions
2) Automatically using the Ansible playbooks. See the configuration_ repo and ml-api branch.

.. _configuration: https://github.com/edx/configuration/tree/vik/ml-api 

This assumes that you already have git installed on your computer. The main steps are::

	$ git clone git://github.com/edx/discern.git

or if you are working with a forked copy::

	$ git clone git@github.com:<your_user_account>/discern.git
	$ xargs -a discern/apt-packages.txt apt-get install
	$ virtualenv /path/to/edx
	$ source /path/to/edx/bin/activate
	$ cd discern
	$ pip install -r pre-requirements.txt
	$ pip install -r requirements.txt
	$ python manage.py syncdb --settings=discern.settings --noinput --pythonpath=DIR WHERE YOU CLONED REPO
	Choose "no" for create superuser if syncdb prompts you for it.
	
	$ python manage.py migrate --settings=discern.settings --noinput --pythonpath=DIR WHERE YOU CLONED REPO
	$ python manage.py collectstatic -c --noinput --settings=discern.settings --pythonpath=DIR WHERE YOU CLONED REPO

See "usage" for how to run this.  You will both need to run the server and the celery tasks.

You can skip the virtualenv commands if you like, but they will be a major help in keeping the packages for this repo separate from the rest of your system.

If you get errors using the above, you may need to create a database directory one level up from where you cloned the git repo (folder named "db")

You will need to install the ease repo (https://github.com/edx/ease) in the same base directory that you installed discern in order to get all functionality.  Follow the install instructions in that repo.
