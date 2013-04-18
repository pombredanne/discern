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

#Celery settings
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

#Haystack settings
HAYSTACK_WHOOSH_PATH = os.path.join(ENV_ROOT,"whoosh_api_index_test")