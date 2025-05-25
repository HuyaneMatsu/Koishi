__all__ = ()

import re

from hata import BUILTIN_EMOJIS, Emoji, create_button, create_row


CUSTOM_ID_SNIPE_SELECT = 'snipe.select'

CUSTOM_ID_SNIPE_DETAILS_EMOJI = 'snipe.details.emoji'
CUSTOM_ID_SNIPE_DETAILS_REACTION = 'snipe.details.reaction'
CUSTOM_ID_SNIPE_DETAILS_SOUNDBOARD_SOUND = 'snipe.details.soundboard_sound'
CUSTOM_ID_SNIPE_DETAILS_STICKER = 'snipe.details.sticker'
CUSTOM_ID_SNIPE_DETAILS_DISABLED = 'snipe.details.disabled'

CUSTOM_ID_SNIPE_DM = 'snipe.dm'
CUSTOM_ID_SNIPE_DM_DISABLED = 'snipe.dm.disabled'

CUSTOM_ID_SNIPE_REVEAL = 'snipe.reveal'
CUSTOM_ID_SNIPE_REVEAL_DISABLED = 'snipe.reveal.disabled'

CUSTOM_ID_SNIPE_CLOSE = 'snipe.close'

CUSTOM_ID_SNIPE_ACTIONS_EMOJI = 'snipe.actions.emoji'
CUSTOM_ID_SNIPE_ACTIONS_SOUNDBOARD_SOUND = 'snipe.actions.soundboard_sound'
CUSTOM_ID_SNIPE_ACTIONS_STICKER = 'snipe.actions.sticker'
CUSTOM_ID_SNIPE_ACTIONS_DISABLED = 'snipe.actions.disabled'

CUSTOM_ID_SNIPE_ADD_EMOJI = 'snipe.add.emoji'
CUSTOM_ID_SNIPE_ADD_SOUNDBOARD_SOUND = 'snipe.add.soundboard_sound'
CUSTOM_ID_SNIPE_ADD_STICKER = 'snipe.add.sticker'
CUSTOM_ID_SNIPE_ADD_DISABLED = 'snipe.add.disabled'

CUSTOM_ID_SNIPE_REMOVE_EMOJI = 'snipe.remove.emoji'
CUSTOM_ID_SNIPE_REMOVE_SOUNDBOARD_SOUND = 'snipe.remove.soundboard_sound'
CUSTOM_ID_SNIPE_REMOVE_STICKER = 'snipe.remove.sticker'
CUSTOM_ID_SNIPE_REMOVE_DISABLED = 'snipe.remove.disabled'

CUSTOM_ID_SNIPE_EDIT_EMOJI = 'snipe.edit.emoji'
CUSTOM_ID_SNIPE_EDIT_SOUNDBOARD_SOUND = 'snipe.edit.soundboard_sound'
CUSTOM_ID_SNIPE_EDIT_STICKER = 'snipe.edit.sticker'
CUSTOM_ID_SNIPE_EDIT_DISABLED = 'snipe.edit.disabled'

# EMOJI_SNIPE_DM = BUILTIN_EMOJIS['e_mail']
# EMOJI_SNIPE_DETAILS = BUILTIN_EMOJIS['notepad_spiral']
EMOJI_SNIPE_CLOSE = BUILTIN_EMOJIS['x']
EMOJI_SNIPE_ACTIONS = Emoji.precreate(1012027437397323787)
EMOJI_SNIPE_DETAILS = Emoji.precreate(852856148805287956)
EMOJI_SNIPE_DM = Emoji.precreate(1060958335404343296)
EMOJI_SNIPE_REVEAL = Emoji.precreate(852856148381925386)
EMOJI_SNIPE_ADD = Emoji.precreate(1015148449110433792)
EMOJI_SNIPE_REMOVE = Emoji.precreate(1013879972466798632)
EMOJI_SNIPE_EDIT = Emoji.precreate(1031941507881644093)

# details

BUTTON_SNIPE_DETAILS_EMOJI = create_button(
    'Details',
    EMOJI_SNIPE_DETAILS,
    custom_id = CUSTOM_ID_SNIPE_DETAILS_EMOJI,
)

BUTTON_SNIPE_DETAILS_REACTION = BUTTON_SNIPE_DETAILS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_DETAILS_REACTION,
)

BUTTON_SNIPE_DETAILS_SOUNDBOARD_SOUND = BUTTON_SNIPE_DETAILS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_DETAILS_SOUNDBOARD_SOUND,
)

BUTTON_SNIPE_DETAILS_STICKER = BUTTON_SNIPE_DETAILS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_DETAILS_STICKER,
)

BUTTON_SNIPE_DETAILS_DISABLED = BUTTON_SNIPE_DETAILS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_DETAILS_DISABLED,
    enabled = False,
)

# dm

BUTTON_SNIPE_DM = create_button(
    'Dm me',
    EMOJI_SNIPE_DM,
    custom_id = CUSTOM_ID_SNIPE_DM,
)

BUTTON_SNIPE_DM_DISABLED = BUTTON_SNIPE_DM.copy_with(
    custom_id = CUSTOM_ID_SNIPE_DM_DISABLED,
    enabled = False,
)

# reveal

BUTTON_SNIPE_REVEAL = create_button(
    'Reveal',
    EMOJI_SNIPE_REVEAL,
    custom_id = CUSTOM_ID_SNIPE_REVEAL,
)

BUTTON_SNIPE_REVEAL_DISABLED = BUTTON_SNIPE_REVEAL.copy_with(
    custom_id = CUSTOM_ID_SNIPE_REVEAL_DISABLED,
    enabled = False,
)

# actions

BUTTON_SNIPE_ACTIONS_EMOJI = create_button(
    'Actions',
    EMOJI_SNIPE_ACTIONS,
    custom_id = CUSTOM_ID_SNIPE_ACTIONS_EMOJI,
)

BUTTON_SNIPE_ACTIONS_SOUNDBOARD_SOUND = BUTTON_SNIPE_ACTIONS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ACTIONS_SOUNDBOARD_SOUND,
)

BUTTON_SNIPE_ACTIONS_STICKER = BUTTON_SNIPE_ACTIONS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ACTIONS_STICKER,
)

BUTTON_SNIPE_ACTIONS_DISABLED = BUTTON_SNIPE_ACTIONS_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ACTIONS_DISABLED,
    enabled = False,
)

# close
BUTTON_SNIPE_CLOSE = create_button(
    'Close',
    emoji = EMOJI_SNIPE_CLOSE,
    custom_id = CUSTOM_ID_SNIPE_CLOSE,
)

# add

BUTTON_SNIPE_ADD_EMOJI = create_button(
    'Borrow',
    EMOJI_SNIPE_ADD,
    custom_id = CUSTOM_ID_SNIPE_ADD_EMOJI,
)

BUTTON_SNIPE_ADD_SOUNDBOARD_SOUND = BUTTON_SNIPE_ADD_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ADD_SOUNDBOARD_SOUND,
)

BUTTON_SNIPE_ADD_STICKER = BUTTON_SNIPE_ADD_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ADD_STICKER,
)

BUTTON_SNIPE_ADD_DISABLED = BUTTON_SNIPE_ADD_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_ADD_DISABLED,
    enabled = False,
)

# remove

BUTTON_SNIPE_REMOVE_EMOJI = create_button(
    'Yeet',
    EMOJI_SNIPE_REMOVE,
    custom_id = CUSTOM_ID_SNIPE_REMOVE_EMOJI,
)

BUTTON_SNIPE_REMOVE_SOUNDBOARD_SOUND = BUTTON_SNIPE_REMOVE_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_REMOVE_SOUNDBOARD_SOUND,
)

BUTTON_SNIPE_REMOVE_STICKER = BUTTON_SNIPE_REMOVE_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_REMOVE_STICKER,
)

BUTTON_SNIPE_REMOVE_DISABLED = BUTTON_SNIPE_REMOVE_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_REMOVE_DISABLED,
    enabled = False,
)

# edit

BUTTON_SNIPE_EDIT_EMOJI = create_button(
    'Edit',
    EMOJI_SNIPE_EDIT,
    custom_id = CUSTOM_ID_SNIPE_EDIT_EMOJI,
)

BUTTON_SNIPE_EDIT_SOUNDBOARD_SOUND = BUTTON_SNIPE_EDIT_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_EDIT_SOUNDBOARD_SOUND,
)

BUTTON_SNIPE_EDIT_STICKER = BUTTON_SNIPE_EDIT_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_EDIT_STICKER,
)

BUTTON_SNIPE_EDIT_DISABLED = BUTTON_SNIPE_EDIT_EMOJI.copy_with(
    custom_id = CUSTOM_ID_SNIPE_EDIT_DISABLED,
    enabled = False,
)

# action response

ROW_SNIPE_ACTION_RESPONSE = create_row(
    BUTTON_SNIPE_REVEAL,
    BUTTON_SNIPE_CLOSE,
)

# Extra stuffs

create_emoji_add_form_custom_id = lambda emoji: f'snipe.emoji.add.{emoji.id}.{emoji.name}.{emoji.animated:d}'
create_soundboard_sound_add_form_custom_id = lambda sound: f'snipe.soundboard_sound.add.{sound.guild_id}.{sound.id}'
create_sticker_add_form_custom_id = lambda sticker: f'snipe.sticker.add.{sticker.id}'

EMOJI_ADD_FORM_PATTERN = re.compile('snipe\\.emoji\\.add\\.(\\d+)\\.(\\w+)\\.([01])')
SOUNDBOARD_SOUND_ADD_FORM_PATTERN = re.compile('snipe\\.soundboard_sound\\.add\\.(\\d+)\\.(\\d+)')
STICKER_ADD_FORM_PATTERN = re.compile('snipe\\.sticker\\.add\\.(\\d+)')

create_emoji_remove_form_custom_id = lambda emoji: f'snipe.emoji.remove.{emoji.id}.{emoji.name}.{emoji.animated:d}'
create_soundboard_sound_remove_form_custom_id = lambda sound: f'snipe.soundboard_sound.remove.{sound.guild_id}.{sound.id}'
create_sticker_remove_form_custom_id = lambda sticker: f'snipe.sticker.remove.{sticker.id}'

EMOJI_REMOVE_FORM_PATTERN = re.compile('snipe\\.emoji\\.remove\\.(\\d+)\\.(\\w+)\\.([01])')
SOUNDBOARD_SOUND_REMOVE_FORM_PATTERN = re.compile('snipe\\.soundboard_sound\\.remove\\.(\\d+)\\.(\\d+)')
STICKER_REMOVE_FORM_PATTERN = re.compile('snipe\\.sticker\\.remove\\.(\\d+)')

create_emoji_edit_form_custom_id = lambda emoji: f'snipe.emoji.edit.{emoji.id}.{emoji.name}.{emoji.animated:d}'
create_soundboard_sound_edit_form_custom_id = lambda sound: f'snipe.soundboard_sound.edit.{sound.guild_id}.{sound.id}'
create_sticker_edit_form_custom_id = lambda sticker: f'snipe.sticker.edit.{sticker.id}'

EMOJI_EDIT_FORM_PATTERN = re.compile('snipe\\.emoji\\.edit\\.(\\d+)\\.(\\w+)\\.([01])')
SOUNDBOARD_SOUND_EDIT_FORM_PATTERN = re.compile('snipe\\.soundboard_sound\\.edit\\.(\\d+)\\.(\\d+)')
STICKER_EDIT_FORM_PATTERN = re.compile('snipe\\.sticker\\.edit\\.(\\d+)')


EMBED_AUTHOR_ID_PATTERN = re.compile('.+?\\((\\d+)\\)')

MATCH_ID_IN_FIELD_VALUE = re.compile('[0-9]+')
MATCH_GUILD_ID_IN_FOOTER = re.compile('.*?\\(([0-9]+)\\)')
MATCH_NAME_IN_FIELD_VALUE = re.compile('[0-9a-zA-Z_\\-]+')
