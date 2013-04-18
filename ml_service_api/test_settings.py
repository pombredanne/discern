from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : '../db/service-api-test-db.db',
        }
}

# Nose Test Runner
INSTALLED_APPS += ('django_nose',)
NOSE_ARGS = ['--cover-erase', '--with-xunit', '--with-xcoverage', '--cover-html',
             '--cover-inclusive', '--cover-html-dir',
             'cover',
             '--cover-package', 'controller',
             '--cover-package', 'staff_grading',
             '--cover-package', 'peer_grading']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'