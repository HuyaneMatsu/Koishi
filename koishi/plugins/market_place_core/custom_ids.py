__all__ = ('CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER', 'CUSTOM_ID_MARKET_PLACE_OFFER_RP')

from re import compile as re_compile


CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER = (
    lambda user_id, entry_id, create_new_message_when_responding :
    f'market_place.offer.{user_id:x}.{entry_id:x}.{create_new_message_when_responding:x}'
)

CUSTOM_ID_MARKET_PLACE_OFFER_RP = re_compile('market_place\\.offer\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])')
