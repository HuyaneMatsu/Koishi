import vampytest
from hata import (
    Emoji, EntitySelectDefaultValue, EntitySelectDefaultValueType, Guild, GuildProfile, InteractionForm, Permission,
    Role, SoundboardSound, Sticker, TextInputStyle, User, create_label, create_role_select, create_text_input
)

from ..component_building import build_edit_form
from ..entity_packing import pack_entity


def _iter_options():
    user_id_0 = 202511030040
    user_id_1 = 202511030041
    
    guild_id_0 = 202511030042
    guild_id_1 = 202511030043
    guild_name_0 = 'Orin dance house'
    guild_name_1 = 'Okuu nuclear waste land'
    
    emoji_id_0 = 202511030044
    sticker_id_0 = 202511030045
    soundboard_sound_id_0 = 202511030046
    
    
    user_0 = User.precreate(
        user_id_0,
    )
    user_0.guild_profiles[guild_id_0] = GuildProfile()
    user_0.guild_profiles[guild_id_1] = GuildProfile()
    
    user_1 = User.precreate(
        user_id_1,
    )
    user_1.guild_profiles[guild_id_0] = GuildProfile()
    user_1.guild_profiles[guild_id_1] = GuildProfile()
    
    role_0 = Role.precreate(
        guild_id_0,
        name = 'green',
        guild_id = guild_id_0,
        permissions = Permission().update_by_keys(administrator = True),
    )
    
    role_1 = Role.precreate(
        guild_id_1,
        name = 'red',
        guild_id = guild_id_1,
        permissions = Permission().update_by_keys(administrator = True),
    )
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = 'satori',
        guild_id = guild_id_0,
        role_ids = [guild_id_0],
    )
    
    sticker_0 = Sticker.precreate(
        sticker_id_0,
        name = 'kasha',
        guild_id = guild_id_0,
        tags = ['orin'],
        description = 'Carting to hell.',
    )
    
    soundboard_sound_0 = SoundboardSound.precreate(
        soundboard_sound_id_0,
        name = 'yama',
        guild_id = guild_id_0,
        emoji = emoji_0,
        volume = 0.5,
    )
    
    guild_0 = Guild.precreate(
        guild_id_0,
        name = guild_name_0,
        roles = [role_0],
        users = [user_0, user_1],
        emojis = [emoji_0],
        stickers = [sticker_0],
        soundboard_sounds = [soundboard_sound_0],
    )
    guild_0.clients.append(user_1)
    
    guild_1 = Guild.precreate(
        guild_id_1,
        name = guild_name_1,
        roles = [role_1],
        users = [user_0, user_1],
    )
    guild_1.clients.append(user_1)
    
    yield (
        emoji_0,
        guild_id_0,
        [
            guild_0,
            guild_1,
        ],
        InteractionForm(
            f'Edit emoji: {emoji_0.name!s}',
            [
                create_label(
                    'Name',
                    'New name for the emoji.',
                    create_text_input(
                        min_length = 2,
                        max_length = 32,
                        custom_id = 'name',
                        value = emoji_0.name,
                    ),
                ),
                create_label(
                    'Roles',
                    'Limits the Emoji\'s usage only to users with any of the specified roles, current guild only.',
                    create_role_select(
                        'roles',
                        default_values = [
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_0.id),
                        ],
                        max_values = 25,
                        min_values = 0,
                    ),
                ),
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.edit.{pack_entity(emoji_0)}',
        ),
    )
    
    yield (
        sticker_0,
        guild_id_0,
        [
            guild_0,
            guild_1,
        ],
        InteractionForm(
            f'Edit sticker: {sticker_0.name!s}',
            [
                create_label(
                    'Name',
                    'New name for the sticker.',
                    create_text_input(
                        min_length = 2,
                        max_length = 32,
                        custom_id = 'name',
                        value = sticker_0.name,
                    ),
                ),
                create_label(
                    'Tags',
                    'Additional values to be matched by auto completion, for custom stickers only 1 is recognized.',
                    create_text_input(
                        custom_id = 'tags',
                        min_length = 0,
                        max_length = 100,
                        value = ', '.join(sticker_0.tags),
                    ),
                ),
                create_label(
                    'Description',
                    'The sticker\'s description. Supposed to be used by screen readers.',
                    create_text_input(
                        custom_id = 'description',
                        min_length = 0,
                        max_length = 1024,
                        value = sticker_0.description,
                        style = TextInputStyle.paragraph,
                    ),
                ),
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.edit.{pack_entity(sticker_0)}',
        ),
    )
    
    yield (
        soundboard_sound_0,
        guild_id_0,
        [
            guild_0,
            guild_1,
        ],
        InteractionForm(
            f'Edit sound: {soundboard_sound_0.name!s}',
            [
                create_label(
                    'Name',
                    'New name for the sound.',
                    create_text_input(
                        min_length = 2,
                        max_length = 32,
                        custom_id = 'name',
                        value = soundboard_sound_0.name,
                    ),
                ),
                create_label(
                    'Emoji',
                    'An emoji assigned to the sound.',
                    create_text_input(
                        custom_id = 'emoji',
                        min_length = 0,
                        max_length = 60,
                        value = soundboard_sound_0.emoji.as_emoji,
                    ),
                ),
                create_label(
                    'volume',
                    'An volume assigned to the sound.',
                    create_text_input(
                        custom_id = 'volume',
                        min_length = 0,
                        max_length = 50,
                        value = format(soundboard_sound_0.volume, '.02f'),
                    ),
                ),
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.edit.{pack_entity(soundboard_sound_0)}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_edit_form(entity, guild_id, entity_cache):
    """
    Tests whether ``build_edit_form`` works as intended.
    
    Parameters
    ----------
    entity : ``None | Sticker | SoundboardSound``
        Entity to use as default.
    
    guild_id : `int`
        The local guild's identifier.
    
    entity_cache : `list<object>`
        Additional entities to keep cached.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    output = build_edit_form(entity, guild_id)
    vampytest.assert_instance(output, InteractionForm)
    return output
