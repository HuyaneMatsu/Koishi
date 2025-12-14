__all__ = ()

from re import compile as re_compile


CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_BUILDER = (
    lambda
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
        target_user_id,
    : (
        f'user.stats_upgrade.{modify_housewife_by:x}.{modify_cuteness_by:x}.{modify_bedroom_by:x}.'
        f'{modify_charm_by:x}.{modify_loyalty_by:x}.{target_user_id:x}'
    )
)


CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_RP = re_compile(
    'user\\.stats_upgrade\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
