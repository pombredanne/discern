"""
Deployment settings file
"""

from settings import *

DEBUG=False

STATIC_ROOT = os.path.abspath(ENV_ROOT / "staticfiles")

TIME_BETWEEN_INDEX_REBUILDS = 60 * 30 # seconds

#Tastypie throttle settings
THROTTLE_AT = 100 #Throttle requests after this number in below timeframe
THROTTLE_TIMEFRAME= 60 * 60 #Timeframe in which to throttle N requests, seconds
THROTTLE_EXPIRATION= 24 * 60 * 60 # When to remove throttle entries from cache, seconds