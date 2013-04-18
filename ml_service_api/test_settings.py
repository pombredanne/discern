from settings import *
import logging

south_logger=logging.getLogger('south')
south_logger.setLevel(logging.INFO)

warning_logger=logging.getLogger('py.warnings')
warning_logger.setLevel(logging.ERROR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : '../db/service-api-test-db.db',
        }
}

# Nose Test Runner
INSTALLED_APPS += ('django_nose',)
NOSE_ARGS = ['--cover-erase', '--with-xunit', '--with-coverage', '--cover-html',
             '--cover-inclusive', '--cover-html-dir', 'cover',
             '--cover-package', 'freeform_data',
             '--cover-package', 'ml_grading',]
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'