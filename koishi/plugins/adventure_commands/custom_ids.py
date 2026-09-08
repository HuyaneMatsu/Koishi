__all__ = ()

from base64 import b64encode as base_64_encode
from re import compile as re_compile

from .constants import FLOAT_STRUCT


BASE_64_CHARACTERS = '[A-Za-z0-9\\+\\/]+\\=*'

CUSTOM_ID_ADVENTURE_CANCELLATION_MODE = 'cancellation_mode'


CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_PATTERN = re_compile(
    'adventure\\.create\\.1\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_CREATE_CONFIRM_BUILDER = (
    lambda user_id, location_id, target_id, duration, return_id, auto_cancellation_id :
    f'adventure.create.1.{user_id:x}.{location_id:x}.{target_id:x}.{duration:x}.{return_id:x}.{auto_cancellation_id:x}'
)


CUSTOM_ID_ADVENTURE_ACTION_VIEW_PATTERN = re_compile(
    'adventure\\.action\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_ACTION_VIEW_BUILDER = (
    lambda
        user_id,
        adventure_entry_id,
        adventure_action_index,
        allow_switching_to_adventure_listing_view,
        adventure_page_index,
        allow_switching_to_adventure_action_listing_view,
        adventure_action_page_index,
    : (
        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_index:x}.'
        f'{allow_switching_to_adventure_listing_view:x}.{adventure_page_index:x}.'
        f'{allow_switching_to_adventure_action_listing_view:x}.{adventure_action_page_index:x}'
    )
)


CUSTOM_ID_ADVENTURE_ACTION_VIEW_DEPART = 'adventure.action.view.depart'
CUSTOM_ID_ADVENTURE_ACTION_VIEW_RETURN = 'adventure.action.view.return'


CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_PATTERN = re_compile(
    f'adventure\\.action_listing\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_ACTION_LISTING_VIEW_BUILDER = (
    lambda
        user_id,
        adventure_entry_id,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        adventure_action_listing_page_index,
    : (
        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.'
        f'{allow_switching_to_adventure_listing_view:x}.{adventure_listing_page_index:x}.'
        f'{adventure_action_listing_page_index:x}'
    )
)


CUSTOM_ID_ADVENTURE_CANCEL_PATTERN = re_compile(
    'adventure\\.cancel\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_CANCEL_BUILDER = (
    lambda user_id, adventure_entry_id :
    f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}'
)


CUSTOM_ID_ADVENTURE_VIEW_PATTERN = re_compile(
    'adventure\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_VIEW_BUILDER = (
    lambda
        user_id,
        adventure_entry_id,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
    : (
        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.'
        f'{allow_switching_to_adventure_listing_view:x}.{adventure_listing_page_index:x}'
    )
)


CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_PATTERN = re_compile(
    'adventure\\.action\\.battle\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_ACTION_BATTLE_LOGS_BUILDER = (
    lambda user_id, adventure_entry_id, adventure_action_index :
    f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_index:x}'
)


CUSTOM_ID_ADVENTURE_LISTING_VIEW_PATTERN = re_compile(
    'adventure\\.listing\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
CUSTOM_ID_ADVENTURE_LISTING_VIEW_BUILDER = (
    lambda user_id, page_index :
    f'adventure.listing.{user_id:x}.{page_index:x}'
)


CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_PATTERN = re_compile('adventure\\.butcher\\.i\\.([0-9a-f]+)\\.([0-9a-f]+)')
CUSTOM_ID_ADVENTURE_BUTCHER_INITIAL_BUILDER = lambda user_id, item_id: f'adventure.butcher.i.{user_id:x}.{item_id:x}'
CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_PATTERN = re_compile(
    f'adventure\\.butcher\\.c\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.'
    f'({BASE_64_CHARACTERS})'
)
CUSTOM_ID_ADVENTURE_BUTCHER_CONTINUOUS_BUILDER = (
    lambda user_id, item_id, seed, butcher_flags, index, multiplier : (
        f'adventure.butcher.c.{user_id:x}.{item_id:x}.{seed:x}.{butcher_flags:x}.{index:x}.'
        f'{base_64_encode(FLOAT_STRUCT.pack(multiplier)).decode("ascii")!s}'
    )
)
CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_PATTERN = re_compile('adventure\\.butcher\\.d\\.[0-9a-f]+\\.[0-9a-f]+\\.[0-9a-f]+')
CUSTOM_ID_ADVENTURE_BUTCHER_DISABLED_BUILDER = (
    lambda user_id, item_id, index: f'adventure.butcher.d.{user_id:x}.{item_id:x}.{index:x}'
)
