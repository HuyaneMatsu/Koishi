__all__ = ()

from math import floor
from re import compile as re_compile


CUSTOM_ID_EVENT_CONFIRMATION_FACTORY = (
    lambda event_mode, duration, amount, user_limit :
    f'heart_event.new.{event_mode:x}.{floor(duration.total_seconds()):x}.{amount:x}.{user_limit:x}'
)

CUSTOM_ID_EVENT_CONFIRMATION_PATTERN = re_compile(
    'heart_event\\.new\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_EVENT_ACTIVE = 'heart_event.active'
CUSTOM_ID_EVENT_INACTIVE = 'heart_event.inactive'
