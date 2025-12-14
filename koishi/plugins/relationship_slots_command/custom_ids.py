__all__ = ()

from re import compile as re_compile


CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_BUILDER = lambda user_id: f'user.buy_relationship_slot.{user_id:x}'

CUSTOM_ID_BUY_RELATIONSHIP_SLOT_CONFIRMATION_RP = re_compile('user\\.buy_relationship_slot\\.([0-9a-f]+)')
