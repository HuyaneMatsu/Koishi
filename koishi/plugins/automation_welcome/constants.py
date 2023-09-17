__all__ = ()

from hata import GuildProfileFlag

ONBOARDING_MASK_STARTED = GuildProfileFlag().update_by_keys(onboarding_started = True)
ONBOARDING_MASK_COMPLETED = GuildProfileFlag().update_by_keys(onboarding_completed = True)
ONBOARDING_MASK_ALL = ONBOARDING_MASK_STARTED | ONBOARDING_MASK_COMPLETED
