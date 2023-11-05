__all__ = ()

from collections import OrderedDict
from datetime import timedelta as TimeDelta

from hata import GuildProfileFlag, timedelta_to_id_difference


ONBOARDING_MASK_STARTED = GuildProfileFlag().update_by_keys(onboarding_started = True)
ONBOARDING_MASK_COMPLETED = GuildProfileFlag().update_by_keys(onboarding_completed = True)
ONBOARDING_MASK_ALL = ONBOARDING_MASK_STARTED | ONBOARDING_MASK_COMPLETED
CUSTOM_ID_WELCOME_REPLY = 'automation.welcome.reply'

REPLY_EXPIRES_AFTER = timedelta_to_id_difference(TimeDelta(days = 7))


REPLY_CACHE = OrderedDict()
REPLY_CACHE_MAX_SIZE = 100
