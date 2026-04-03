import vampytest
from hata import Guild, Emoji

from ..content_building import produce_guild_emojis_description


def _iter_options():
    guild_id = 202511210010
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            ''
        ),
    )
    
    
    guild_id = 202511210013
    emoji_id_0 = 202511210014
    emoji_id_1 = 202511210015
    emoji_id_2 = 202511210016
    emoji_id_3 = 202511210017
    
    guild = Guild.precreate(
        guild_id,
        emojis = [
            Emoji.precreate(emoji_id_0),
            Emoji.precreate(emoji_id_1),
            Emoji.precreate(emoji_id_2, managed = True),
            Emoji.precreate(emoji_id_3, animated = True),
        ]
    )
    
    yield (
        guild,
        False,
        (
            '## Emojis\n'
            '**Total: 4**\n'
            '**Static emojis: 2** [48 free]\n'
            '**Animated emojis: 1** [49 free]\n'
            '**Managed: 1** [1 static, 0 animated]'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_emojis_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_emojis_description`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_guild_emojis_description(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
