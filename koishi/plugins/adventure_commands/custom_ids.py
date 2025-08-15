__all__ = ()

from re import compile as re_compile


ADVENTURE_CREATE_CONFIRM_RP = re_compile(
    'adventure\\.create\\.1\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_CREATE_CONFIRM_BUILDER = (
    lambda user_id, location_id, target_id, duration, return_id, auto_cancellation_id :
    f'adventure.create.1.{user_id:x}.{location_id:x}.{target_id:x}.{duration:x}.{return_id:x}.{auto_cancellation_id:x}'
)


ADVENTURE_CREATE_CANCEL_RP = re_compile(
    'adventure\\.create\\.0\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_CREATE_CANCEL_BUILDER = (
    lambda user_id, location_id, target_id, duration, return_id, auto_cancellation_id :
    f'adventure.create.0.{user_id:x}.{location_id:x}.{target_id:x}.{duration:x}.{return_id:x}.{auto_cancellation_id:x}'
)


ADVENTURE_ACTION_VIEW_RP = re_compile(
    'adventure\\.action\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
ADVENTURE_ACTION_VIEW_BUILDER = (
    lambda
        user_id,
        adventure_entry_id,
        adventure_action_entry_id,
        allow_switching_to_adventure_listing_view,
        adventure_page_index,
        allow_switching_to_adventure_action_listing_view,
        adventure_action_page_index,
    : (
        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}.'
        f'{allow_switching_to_adventure_listing_view:x}.{adventure_page_index:x}.'
        f'{allow_switching_to_adventure_action_listing_view:x}.{adventure_action_page_index:x}'
    )
)


ADVENTURE_ACTION_VIEW_DEPART = 'adventure.action.view.depart'
ADVENTURE_ACTION_VIEW_RETURN = 'adventure.action.view.return'


ADVENTURE_ACTION_LISTING_VIEW_RP = re_compile(
    f'adventure\\.action_listing\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_ACTION_LISTING_VIEW_BUILDER = (
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


ADVENTURE_CANCEL_RP = re_compile(
    'adventure\\.cancel\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_CANCEL_BUILDER = (
    lambda user_id, adventure_entry_id :
    f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}'
)


ADVENTURE_VIEW_RP = re_compile(
    'adventure\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([01])\\.([0-9a-f]+)'
)
ADVENTURE_VIEW_BUILDER = (
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


ADVENTURE_ACTION_BATTLE_LOGS_RP = re_compile(
    'adventure\\.action\\.battle\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_ACTION_BATTLE_LOGS_BUILDER = (
    lambda user_id, adventure_entry_id, adventure_action_entry_id :
    f'adventure.action.battle.{user_id:x}.{adventure_entry_id:x}.{adventure_action_entry_id:x}'
)


ADVENTURE_LISTING_VIEW_RP = re_compile(
    'adventure\\.listing\\.([0-9a-f]+)\\.([0-9a-f]+)'
)
ADVENTURE_LISTING_VIEW_BUILDER = (
    lambda user_id, page_index :
    f'adventure.listing.{user_id:x}.{page_index:x}'
)
