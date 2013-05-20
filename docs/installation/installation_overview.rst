=================================
Installation Overview
=================================
Looking at fabfile.py is also a good idea of how to install this.  The commands in fabfile will take a system
from a fresh start to a fully working install.
The main steps are:

1. apt-get install git python
2. git clone git@github.com:edx/discern.git
3. xargs -a apt-packages.txt apt-get install
4. apt-get install python-pip
5. pip install virtualenv
6. virtualenv /opt/edx
7. source /opt/edx/bin/activate
8. cd discern
9. pip install -r pre-requirements.txt
10. pip install -r requirements.txt
11. python manage.py syncdb --settings=discern.settings --noinput --pythonpath=DIR WHERE YOU CLONED REPO
12. Choose "no" for create superuser if syncdb prompts you for it.
13. python manage.py migrate --settings=discern.settings --noinput --pythonpath=DIR WHERE YOU CLONED REPO
14. python manage.py collectstatic -c --noinput --settings=discern.settings --pythonpath=DIR WHERE YOU CLONED REPO

See :doc:`usage` for how to run this.  You will both need to run the server and the celery tasks.

You can skip the virtualenv commands if you like, but they will be a major help in keeping the packages
for this repo separate from the rest of your system.

If all has gone well, you see a database directory called db. An sqlite3 database was created in it. The sqlite3 
command can be used to inspect the tables which Django generated.  
::
	$ sqlite3 db/service-api-db.db 
	SQLite version 3.7.9 2011-11-01 00:52:41
	Enter ".help" for instructions
	Enter SQL statements terminated with a ";"
	sqlite> .tables
	account_emailaddress                freeform_data_course              
	account_emailconfirmation           freeform_data_course_organizations
	auth_group                          freeform_data_course_users        
	auth_group_permissions              freeform_data_essay               
	auth_permission                     freeform_data_essaygrade          
	auth_user                           freeform_data_membership          
	auth_user_groups                    freeform_data_organization        
	auth_user_user_permissions          freeform_data_problem             
	celery_taskmeta                     freeform_data_problem_courses     
	celery_tasksetmeta                  freeform_data_userprofile         
	django_admin_log                    guardian_groupobjectpermission    
	django_content_type                 guardian_userobjectpermission     
	django_session                      ml_grading_createdmodel           
	django_site                         socialaccount_socialaccount       
	djcelery_crontabschedule            socialaccount_socialapp           
	djcelery_intervalschedule           socialaccount_socialapp_sites     
	djcelery_periodictask               socialaccount_socialtoken         
	djcelery_periodictasks              south_migrationhistory            
	djcelery_taskstate                  tastypie_apiaccess                
	djcelery_workerstate                tastypie_apikey    

You will need to install the ease repo (https://github.com/edx/ease) in the same base directory that you installed discern in order to get all functionality.  Follow the install instructions in that repo.
