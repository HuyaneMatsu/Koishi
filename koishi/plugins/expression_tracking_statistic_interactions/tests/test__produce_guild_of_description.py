import vampytest
from hata import Emoji, Guild, GuildProfile, Role, User

from ...expression_tracking import ACTION_TYPE_EMOJI_CONTENT

from ..content_building import produce_guild_of_description


def _iter_options():
    emoji_id_0 = 202512100000
    emoji_id_1 = 202512100001
    emoji_id_2 = 202512100002
    guild_id = 202512100003
    user_id = 202512100004
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = 'koishi',
        guild_id = guild_id,
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        name = 'koishi',
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile()
    
    role = Role.precreate(
        guild_id,
        guild_id = guild_id,
    )
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji_0],
        roles = [role],
        users = [user],
    )
    
    yield (
        user,
        (1 << ACTION_TYPE_EMOJI_CONTENT),
        [
            (emoji_id_0, 5, 4),
            (emoji_id_1, 5, 3),
            (emoji_id_2, 5, 2),
        ],
        [
            guild,
            emoji_0,
            emoji_1,
        ],
        (
            f'`Total | Internal | External | Emojis`\n'
            f'`    5 |        4 |        1 | ` {emoji_0.as_emoji}\n'
            f'`    5 |        3 |        2 | :{emoji_1.name}:`\n'
            f'`    5 |        2 |        3 | {emoji_id_2}`'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_of_description(client, action_types_packed, entries, entity_cache):
    """
    Tests whether ``produce_guild_of_description`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    action_types_packed : `int`
        The action types packed.
    
    entries : `list<(int, int, int)>`
        Entries to render.
    
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_guild_of_description(client, action_types_packed, entries)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
