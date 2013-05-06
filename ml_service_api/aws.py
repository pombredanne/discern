"""
Deployment settings file
"""

from settings import *
import json

DEBUG=False

STATIC_ROOT = os.path.abspath(ENV_ROOT / "staticfiles")

TIME_BETWEEN_INDEX_REBUILDS = 60 * 30 # seconds

#Tastypie throttle settings
THROTTLE_AT = 100 #Throttle requests after this number in below timeframe
THROTTLE_TIMEFRAME= 60 * 60 #Timeframe in which to throttle N requests, seconds
THROTTLE_EXPIRATION= 24 * 60 * 60 # When to remove throttle entries from cache, seconds

with open(ENV_ROOT + "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)

with open(ENV_ROOT + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

DATABASES = AUTH_TOKENS['DATABASES']
CACHES = AUTH_TOKENS['CACHES']

AWS_ACCESS_KEY_ID = AUTH_TOKENS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS['AWS_SECRET_ACCESS_KEY']

BROKER_URL = AUTH_TOKENS['BROKER_URL']
CELERY_RESULT_BACKEND = AUTH_TOKENS['CELERY_RESULT_BACKEND']