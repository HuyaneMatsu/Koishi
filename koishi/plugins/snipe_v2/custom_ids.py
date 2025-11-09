__all__ = ()

from re import compile as re_compile

BASE_64_CHARACTERS = '[A-Za-z0-9\\+\\/]+\\=*'


CUSTOM_ID_SNIPE_ACTION_BUILDER = (
    lambda user_id, feature_flags, entity_packed: f'snipe.action.{user_id:x}.{feature_flags:x}.{entity_packed!s}'
)
CUSTOM_ID_SNIPE_ACTION_PATTERN = re_compile(
    f'snipe\\.action\\.([0-9a-f]+)\\.([0-9a-f]+)\\.({BASE_64_CHARACTERS})'
)


CUSTOM_ID_SNIPE_CHOICE_BUILDER = lambda user_id, feature_flags : f'snipe.choice.{user_id:x}.{feature_flags:x}'
CUSTOM_ID_SNIPE_CHOICE_PATTERN = re_compile(f'snipe\\.choice\\.([0-9a-f]+)\\.([0-9a-f]+)')

CUSTOM_ID_SNIPE_ADD_BUILDER = lambda default_entity_packed : f'snipe.add.{default_entity_packed!s}'
CUSTOM_ID_SNIPE_ADD_PATTERN = re_compile(f'snipe\\.add\\.({BASE_64_CHARACTERS})')

CUSTOM_ID_SNIPE_EDIT_BUILDER = lambda default_entity_packed : f'snipe.edit.{default_entity_packed!s}'
CUSTOM_ID_SNIPE_EDIT_PATTERN = re_compile(f'snipe\\.edit\\.({BASE_64_CHARACTERS})')

CUSTOM_ID_SNIPE_REMOVE_BUILDER = lambda default_entity_packed : f'snipe.remove.{default_entity_packed!s}'
CUSTOM_ID_SNIPE_REMOVE_PATTERN = re_compile(f'snipe\\.remove\\.({BASE_64_CHARACTERS})')

CUSTOM_ID_ENTITY_GUILD = 'guild'
CUSTOM_ID_ENTITY_NAME = 'name'
CUSTOM_ID_ENTITY_ROLES = 'roles'
CUSTOM_ID_ENTITY_TAGS = 'tags'
CUSTOM_ID_ENTITY_DESCRIPTION = 'description'
CUSTOM_ID_ENTITY_EMOJI = 'emoji'
CUSTOM_ID_ENTITY_VOLUME = 'volume'
CUSTOM_ID_ENTITY_FILE = 'file'
CUSTOM_ID_ENTITY_REASON = 'reason'
