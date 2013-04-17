"""
Deployment settings file
"""

from settings import *

DEBUG=False

STATIC_ROOT = os.path.abspath(ENV_ROOT / "staticfiles")

TIME_BETWEEN_INDEX_REBUILDS = 60 * 30 # seconds