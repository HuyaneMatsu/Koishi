__all__ = ()

import re

FEEDERS = {}

TAG_NAME_REQUIRED = 'touhou-feed'
TAG_NAME_SOLO = 'solo'

DEFAULT_INTERVAL = 4 * 3600
MIN_INTERVAL = 15 * 60
MAX_INTERVAL =   24 * 3600
INTERVAL_MULTIPLIER = 50

TAG_REQUIRED_RP = re.compile(f'(?:\\s|^)#{TAG_NAME_REQUIRED}', re.M | re.U)
TAG_RP = re.compile(f'(?:\\s|^)#([\\w\\-]+)', re.M | re.U)
