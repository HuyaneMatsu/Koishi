__all__ = ()

from re import compile as re_compile, escape as re_escape


CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE = 'automation_reaction_role'


CUSTOM_ID_ITEM_ADD_FACTORY = (
    lambda listing_page_index, message_id :
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.item_add.{listing_page_index:x}.{message_id:x}'
)
CUSTOM_ID_ITEM_ADD_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.item_add\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_ITEM_MODIFY_FACTORY = (
    lambda listing_page_index, message_id, overview_page_index, emoji_id :
    (
        f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.item_modify.{listing_page_index:x}.{message_id:x}.'
        f'{overview_page_index:x}.{emoji_id:x}'
    )
)
CUSTOM_ID_ITEM_MODIFY_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.item_modify\\.'
    f'([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_ITEM_DELETE_FACTORY = (
    lambda listing_page_index, message_id, overview_page_index : (
        f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.item_delete.'
        f'{listing_page_index:x}.{message_id:x}.{overview_page_index:x}'
    )
)
CUSTOM_ID_ITEM_DELETE_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.item_delete\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_ENTRY_DELETE_FACTORY = (
    lambda listing_page_index, message_id :
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.delete.{listing_page_index:x}.{message_id:x}'
)
CUSTOM_ID_ENTRY_DELETE_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.delete\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

# CUSTOM_ID_ENTRY_SYNC_FACTORY = (
#     lambda listing_page_index, message_id :
#     f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.sync.{listing_page_index:x}.{message_id:x}'
# )


CUSTOM_ID_ENTRY_PAGE_VIEW_FACTORY = (
    lambda listing_page_index, message_id, overview_page_index :
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.view.{listing_page_index:x}.{message_id:x}.{overview_page_index:x}'
)
CUSTOM_ID_ENTRY_PAGE_VIEW_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.view\\.([0-9a-f]+)\\.([0-9a-f]+)\\.([0-9a-f]+)'
)

CUSTOM_ID_ENTRY_PAGE_VIEW_DECREMENT_DISABLED = f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.view.decrement.disabled'
CUSTOM_ID_ENTRY_PAGE_VIEW_INCREMENT_DISABLED = f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.view.increment.disabled'

CUSTOM_ID_LISTING_PAGE_VIEW_FACTORY = (
    lambda listing_page_index :
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.listing.{listing_page_index:x}'
)

CUSTOM_ID_LISTING_PAGE_VIEW_PATTERN = re_compile(
    f'{re_escape(CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE)}\\.listing\\.([0-9a-f]+)'
)

CUSTOM_ID_LISTING_PAGE_VIEW_DECREMENT_DISABLED = (
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.listing.decrement.disabled'
)
CUSTOM_ID_LISTING_PAGE_VIEW_INCREMENT_DISABLED = (
    f'{CUSTOM_ID_AUTOMATION_REACTION_ROLE_BASE!s}.listing.increment.disabled'
)

CUSTOM_ID_EMOJI = 'emoji'
CUSTOM_ID_ADD_ROLES = 'add_roles'
CUSTOM_ID_REMOVE_ROLES = 'remove_roles'
