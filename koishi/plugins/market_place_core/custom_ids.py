__all__ = (
    'CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_BUILDER', 'CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_PATTERN',
    'CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER', 'CUSTOM_ID_MARKET_PLACE_OFFER_PATTERN'
)

from re import compile as re_compile


CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER = (
    lambda user_id, entry_id, create_new_message_when_responding :
    f'market_place.offer.{user_id:x}.{entry_id:x}.{create_new_message_when_responding:x}'
)
CUSTOM_ID_MARKET_PLACE_OFFER_PATTERN = re_compile('market_place\\.offer\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])')


CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_BUILDER = (
    lambda user_id, page_index, page_size, entry_id, create_standalone_response :
    f'market_place.inbox.claim_one.{user_id:x}.{page_index:x}.{page_size:x}.{entry_id:x}.{create_standalone_response:x}'
)
CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_PATTERN = re_compile(
    'market_place\\.inbox\\.claim_one\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])'
)
