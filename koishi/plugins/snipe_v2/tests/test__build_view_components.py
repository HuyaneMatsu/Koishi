import vampytest
from hata import (
    Component, Emoji, Guild, GuildProfile, MediaInfo, MediaItem, Permission, Role, StringSelectOption,
    User, create_media_gallery, create_row, create_string_select, create_text_display
)

from ..component_building import build_view_components
from ..constants import (
    ACTION_ADD, ACTION_CLOSE, ACTION_DETAILS, ACTION_DM, ACTION_EDIT, ACTION_REMOVE, ACTION_REVEAL, EMOJI_ADD,
    EMOJI_CLOSE, EMOJI_DETAILS, EMOJI_DM, EMOJI_EDIT, EMOJI_REMOVE, EMOJI_REVEAL, FEATURE_FLAG_DETAILED,
    FEATURE_FLAG_DM, FEATURE_FLAG_REVEALED
)
from ..entity_packing import pack_entity


def _iter_options():
    user_id_0 = 202510310000
    user_name_0 = 'pudding'
    
    user_id_1 = 202510310001
    user_name_1 = 'dealer'
    
    user_id_2 = 202510310002
    user_name_2 = 'eater'
    
    guild_id_0 = 202510310003
    guild_name_0 = 'mansion'
    
    guild_id_1 = 202510310004
    guild_name_1 = 'shrine'
    
    emoji_id_0 = 202510310005
    emoji_name_0 = 'cry'
    
    emoji_id_1 = 202510310006
    emoji_name_1 = 'hug'
    
    user_0 = User.precreate(
        user_id_0,
        name = user_name_0,
    )
    user_0.guild_profiles[guild_id_0] = GuildProfile()
    user_0.guild_profiles[guild_id_1] = GuildProfile()
    
    user_1 = User.precreate(
        user_id_1,
        name = user_name_1,
    )
    user_1.guild_profiles[guild_id_0] = GuildProfile()
    
    user_2 = User.precreate(
        user_id_2,
        name = user_name_2,
    )
    user_2.guild_profiles[guild_id_0] = GuildProfile()
    user_2.guild_profiles[guild_id_1] = GuildProfile()
    
    role_0 = Role.precreate(
        guild_id_0,
        guild_id = guild_id_0,
        permissions = Permission(),
    )
    
    role_1 = Role.precreate(
        guild_id_1,
        guild_id = guild_id_1,
        permissions = Permission().update_by_keys(administrator = True),
    )
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = emoji_name_0,
        guild_id = guild_id_0,
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        name = emoji_name_1,
        guild_id = guild_id_1,
    )
    
    guild_0 = Guild.precreate(
        guild_id_0,
        emojis = [emoji_0, emoji_1],
        roles = [role_0],
        name = guild_name_0,
        users = [user_0, user_1, user_2],
    )
    guild_0.clients.append(user_0)
    guild_0.clients.append(user_2)
    
    guild_1 = Guild.precreate(
        guild_id_1,
        emojis = [emoji_0, emoji_1],
        roles = [role_1],
        name = guild_name_1,
        users = [user_0, user_1, user_2],
    )
    guild_0.clients.append(user_0)
    guild_1.clients.append(user_2)
    
    
    yield (
        user_0,
        user_1,
        0,
        emoji_0,
        None,
        0,
        [guild_0, guild_1, role_0, role_1],
        [
            create_text_display(
                f'Name: {emoji_name_0!s}\n'
                f'Identifier: {emoji_id_0!s}'
            ),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        emoji_0.url,
                    ),
                ),
            ),
            create_row(
                create_string_select(
                    [
                        StringSelectOption(ACTION_DETAILS, 'Details', EMOJI_DETAILS),
                        StringSelectOption(ACTION_DM, 'Dm me', EMOJI_DM),
                        StringSelectOption(ACTION_REVEAL, 'Reveal', EMOJI_REVEAL),
                        StringSelectOption(ACTION_CLOSE, 'Close', EMOJI_CLOSE),
                    ],
                    custom_id = f'snipe.action.{user_id_1:x}.{0:x}.{pack_entity(emoji_0)}',
                    placeholder = 'Select an action',
                ),
            ),
        ],
    )
    
    yield (
        user_0,
        user_2,
        0,
        emoji_1,
        [emoji_1, emoji_0],
        0,
        [guild_0, guild_1, role_0, role_1],
        [
            create_text_display(
                f'Name: {emoji_name_1!s}\n'
                f'Identifier: {emoji_id_1!s}'
            ),
            create_media_gallery(
                MediaItem(
                    MediaInfo(
                        emoji_1.url,
                    ),
                )
            ),
            create_row(
                create_string_select(
                    [
                        StringSelectOption(pack_entity(emoji_1), emoji_name_1, emoji_1, default = True),
                        StringSelectOption(pack_entity(emoji_0), emoji_name_0, emoji_0),
                    ],
                    custom_id = f'snipe.choice.{user_id_2:x}.{0:x}',
                    placeholder = 'Select an entity',
                ),
            ),
            create_row(
                create_string_select(
                    [
                        StringSelectOption(ACTION_DETAILS, 'Details', EMOJI_DETAILS),
                        StringSelectOption(ACTION_DM, 'Dm me', EMOJI_DM),
                        StringSelectOption(ACTION_REVEAL, 'Reveal', EMOJI_REVEAL),
                        StringSelectOption(ACTION_ADD, 'Add', EMOJI_ADD),
                        StringSelectOption(ACTION_EDIT, 'Edit', EMOJI_EDIT),
                        StringSelectOption(ACTION_REMOVE, 'Remove', EMOJI_REMOVE),
                        StringSelectOption(ACTION_CLOSE, 'Close', EMOJI_CLOSE),
                    ],
                    custom_id = f'snipe.action.{user_id_2:x}.{0:x}.{pack_entity(emoji_1)}',
                    placeholder = 'Select an action',
                ),
            ),
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_view_components(
    client,
    user,
    feature_flags,
    entity,
    choices,
    guild_id,
    entity_cache,
):
    """
    Tests whether ``build_view_components`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client displaying the components.
    
    user : ``ClientUserBase``
        The user the components are displayed for.
    
    feature_flags : `int`
        How the message should be displayed as.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to display.
    
    choices : ``None | list<Emoji | Sticker | SoundboardSound>``
        Additional choices to display.
    
    guild_id : `int`
        The local guild's identifier.
    
    entity_cache : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_view_components(
        client,
        user,
        feature_flags,
        entity,
        choices,
        guild_id,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
