__all__ = ()

from re import compile as re_compile


CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER = (
    lambda user_id :
    f'market_place.close.{user_id:x}'
)

CUSTOM_ID_MARKET_PLACE_CLOSE_RP = re_compile('market_place\\.close\\.([0-9a-f]+)')


CUSTOM_ID_MARKET_PLACE_SELL_BUILDER = (
    lambda item_id, item_amount, duration_days, starting_sell_price :
    f'market_place.sell.{item_id:x}.{item_amount:x}.{duration_days:x}.{starting_sell_price:x}'
)
CUSTOM_ID_MARKET_PLACE_SELL_RP = re_compile(
    'market_place\\.sell\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_BUILDER = (
    lambda user_id, page_index, page_size :
    f'market_place.own_offers.view.{user_id:x}.{page_index:x}.{page_size:x}'
)
CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_RP = re_compile(
    'market_place\\.own_offers\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_DECREMENT_DISABLED = 'market_place.own_offers.disabled.d'
CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_INCREMENT_DISABLED = 'market_place.own_offers.disabled.i'


CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_BUILDER = (
    lambda user_id, page_index, page_size :
    f'market_place.inbox.view.{user_id:x}.{page_index:x}.{page_size:x}'
)
CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_RP = re_compile(
    'market_place\\.inbox\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_DECREMENT_DISABLED = 'market_place.inbox.disabled.d'
CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_INCREMENT_DISABLED = 'market_place.inbox.disabled.i'


CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_BUILDER = (
    lambda user_id, page_index, page_size, entry_id :
    f'market_place.inbox.claim.{user_id:x}.{page_index:x}.{page_size:x}.{entry_id:x}'
)
CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_RP = re_compile(
    'market_place\\.inbox\\.claim\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)


CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER = (
    lambda user_id, item_id, required_flags, page_index, page_size :
    f'market_place.purchase.view.{user_id:x}.{item_id:x}.{required_flags:x}.{page_index:x}.{page_size:x}'
)
CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_RP = re_compile(
    'market_place\\.purchase\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_DECREMENT_DISABLED = 'market_place.purchase.disabled.d'
CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_INCREMENT_DISABLED = 'market_place.purchase.disabled.i'


CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_BUILDER = (
    lambda user_id, item_id, required_flags, page_index, page_size, entry_id :
    f'market_place.purchase.details.{user_id:x}.{item_id:x}.{required_flags:x}.{page_index:x}.{page_size:x}.{entry_id:x}'
)
CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_RP = re_compile(
    'market_place\\.purchase\\.details\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
 
CUSTOM_ID_MARKET_PLACE_BID_BUILDER = (
    lambda user_id, item_id, required_flags, page_index, page_size, internal_call, entry_id :
    (
        f'market_place.bid.{user_id:x}.{item_id:x}.{required_flags:x}.{page_index:x}.{page_size:x}.'
        f'{internal_call:x}.{entry_id:x}'
    )
)
CUSTOM_ID_MARKET_PLACE_BID_RP = re_compile(
    'market_place\\.bid\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
CUSTOM_ID_MARKET_PLACE_BID_DISABLED = 'market_place.bid.disabled'

CUSTOM_ID_BID_BALANCE_AMOUNT = 'bid_balance_amount'
