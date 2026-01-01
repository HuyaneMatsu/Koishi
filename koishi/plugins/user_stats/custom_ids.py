__all__ = ()

from re import compile as re_compile


CUSTOM_ID_USER_STATS_PRIMARY_BUILDER = (
    lambda user_id, target_user_id : f'user_stats.primary.{user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_USER_STATS_PRIMARY_RP = re_compile('user_stats\\.primary\\.([0-9a-f]+)\\.([0-9a-f]+)')
CUSTOM_ID_USER_STATS_SECONDARY_BUILDER = (
    lambda user_id, target_user_id : f'user_stats.secondary.{user_id:x}.{target_user_id:x}'
)
CUSTOM_ID_USER_STATS_SECONDARY_RP = re_compile('user_stats\\.secondary\\.([0-9a-f]+)\\.([0-9a-f]+)')
