__all__ = ()

from re import compile as re_compile


CUSTOM_ID_BUY_ROLE_CONFIRMATION_BUILDER = lambda role_id, user_id: f'user.buy_role.{role_id:x}.{user_id:x}'

CUSTOM_ID_BUY_ROLE_CONFIRMATION_RP = re_compile('user\\.buy_role\\.([0-9a-f]+)\\.([0-9a-f]+)')
