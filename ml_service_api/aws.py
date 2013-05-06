"""
Deployment settings file
"""

from settings import *
import json

DEBUG=False

TIME_BETWEEN_INDEX_REBUILDS = 60 * 30 # seconds

#Tastypie throttle settings
THROTTLE_AT = 100 #Throttle requests after this number in below timeframe
THROTTLE_TIMEFRAME= 60 * 60 #Timeframe in which to throttle N requests, seconds
THROTTLE_EXPIRATION= 24 * 60 * 60 # When to remove throttle entries from cache, seconds

with open(os.path.join(ENV_ROOT,"env.json")) as env_file:
    ENV_TOKENS = json.load(env_file)

with open(os.path.join(ENV_ROOT, "auth.json")) as auth_file:
    AUTH_TOKENS = json.load(auth_file)

DATABASES = AUTH_TOKENS.get('DATABASES', DATABASES)
CACHES = AUTH_TOKENS.get('CACHES', CACHES)

AWS_ACCESS_KEY_ID = AUTH_TOKENS.get('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)

USE_S3_TO_STORE_MODELS = ENV_TOKENS.get('USE_S3_TO_STORE_MODELS', USE_S3_TO_STORE_MODELS)
S3_BUCKETNAME = ENV_TOKENS.get('S3_BUCKETNAME', S3_BUCKETNAME)

BROKER_URL = AUTH_TOKENS.get('BROKER_URL', BROKER_URL)
CELERY_RESULT_BACKEND = AUTH_TOKENS.get('CELERY_RESULT_BACKEND', CELERY_RESULT_BACKEND)


ELB_HOSTNAME = ENV_TOKENS.get('ELB_HOSTNAME', None)

if ELB_HOSTNAME is not None:
    ALLOWED_HOSTS += [ELB_HOSTNAME]