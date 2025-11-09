import vampytest
from hata import BUILTIN_EMOJIS, Emoji, Guild

from ..responding_helpers import identify_input_emoji


def _iter_options():
    guild_id = 202511040000
    emoji_id_0 = 202511040001
    emoji_id_1 = 202511040002
    emoji_id_2 = 202511040003
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = 'OrinSmirk',
        guild_id = guild_id,
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        name = 'OrinSmug',
        guild_id = guild_id,
    )
    
    emoji_2 = Emoji.precreate(
        emoji_id_2,
        name = 'mushroom',
        guild_id = guild_id,
    )
    
    emoji_3 = BUILTIN_EMOJIS['mushroom']
    emoji_4 = BUILTIN_EMOJIS['heart']
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji_0, emoji_1, emoji_2],
    )
    
    yield (
        guild,
        None,
        (
            True,
            None,
        ),
    )
    
    yield (
        guild,
        emoji_0.as_emoji,
        (
            True,
            emoji_0,
        ),
    )
    
    yield (
        guild,
        str(emoji_0.id),
        (
            True,
            emoji_0,
        ),
    )
    
    yield (
        guild,
        emoji_3.unicode,
        (
            True,
            emoji_3,
        ),
    )
    
    yield (
        guild,
        'mushroom',
        (
            True,
            emoji_2,
        ),
    )
    
    yield (
        guild,
        emoji_4.name,
        (
            True,
            emoji_4,
        ),
    )
    
    yield (
        guild,
        'smug',
        (
            True,
            emoji_1,
        ),
    )
    
    yield (
        guild,
        'stare',
        (
            False,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__identify_input_emoji(guild, input_emoji):
    """
    Tests whether ``identify_input_emoji`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to execute the identification for.
    
    input_emoji : `None | str`
        The inputted value.
    
    Returns
    -------
    output : ``None | Emoji``
    """
    output = identify_input_emoji(guild, input_emoji)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    identified, emoji = output
    vampytest.assert_instance(identified, bool)
    vampytest.assert_instance(emoji, Emoji, nullable = True)
    return output
