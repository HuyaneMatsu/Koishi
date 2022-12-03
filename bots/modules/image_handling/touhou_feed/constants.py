__all__ = ()

import re

FEEDERS = {}

TAG_NAME_REQUIRED = 'touhou-feed'
TAG_NAME_SOLO = 'solo'

DEFAULT_INTERVAL = 4 * 3600
MIN_INTERVAL = 15 * 60
MAX_INTERVAL = 24 * 3600

TAG_REQUIRED_RP = re.compile(f'(?:\\s|^)#{TAG_NAME_REQUIRED}', re.M | re.U)
TAG_ITER_RP = re.compile(f'(?:\\s|^)#([\\w\\-\\_\\+\\:]+)', re.M | re.U)

INTERVAL_RP = re.compile(f'interval(?:lum)?\\s*\\:((?:\\s*\\d+\\s*[hms])+)')
INTERVAL_UNIT_RP = re.compile('0*?(\\d+)\\s*([hms])')
