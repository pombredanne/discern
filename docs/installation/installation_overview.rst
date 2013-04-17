=================================
Installation Overview
=================================
Looking at fabfile.py is also a good idea of how to install this.  The commands in fabfile will take a system
from a fresh start to a fully working install.
The main steps are:

1. apt-get install git python
2. git clone git@github.com:edx/ml-service-api.git
3. git clone git clone git@github.com:edx/machine-learning.git
4. xargs -a apt-packages.txt apt-get install
5. apt-get install python-pip
6. pip install virtualenv
7. mkdir /opt/edx
8. virtualenv "/opt/edx"
9. source /opt/edx/bin/activate
10. cd machine-learning
11. pip install -r pre-requirements.txt
12. pip install -r requirements.txt
13. cd ml-service-api
14. pip install -r pre-requirements.txt
15. pip install -r requirements.txt
16. python manage.py syncdb --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO
17. python manage.py migrate --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO
18. python manage.py collectstatic -c --noinput --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO

You can skip the virtualenv commands if you like, but they will be a major help in keeping the packages
for this repo separate from the rest of your system.

If you get errors using the above, you may need to create a database directory one level up from where you cloned
the git repo (folder named "db")