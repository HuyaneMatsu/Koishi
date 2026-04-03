import vampytest
from hata import Emoji, Guild, InteractionEvent

from ..responding_helpers import get_autocomplete_suggestions_for_emoji_name


def _iter_options():
    emoji_id_0 = 202511010070
    emoji_id_1 = 202511010071
    emoji_id_2 = 202511010072
    
    guild_id_0 = 202511010073
    
    interaction_event_id_0 = 202511010074
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        guild_id = guild_id_0,
        name = 'OrinCarting',
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        guild_id = guild_id_0,
        name = 'OrinShock',
    )
    
    emoji_2 = Emoji.precreate(
        emoji_id_2,
        guild_id = guild_id_0,
        name = 'KoishiShock',
    )
    
    guild_0 = Guild.precreate(
        guild_id_0,
        emojis = [
            emoji_0,
            emoji_1,
            emoji_2,
        ],
    )
    
    interaction_event_0 = InteractionEvent.precreate(
        interaction_event_id_0,
        guild = guild_0,
    )
    
    yield (
        interaction_event_0,
        emoji_0.as_emoji,
        [
            emoji_0,
        ],
        [
            emoji_0.as_emoji,
        ]
    )
    
    yield (
        interaction_event_0,
        'shock',
        [
            guild_0,
        ],
        [
            emoji_1.name,
            emoji_2.name,
        ],
    )
    
    yield (
        interaction_event_0,
        'okuu',
        [],
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_autocomplete_suggestions_for_emoji_name(interaction_event, emoji_name, entity_cache):
    """
    Gets auto-complete suggestion for the given emoji's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    emoji_name : `None | str`
        The typed value.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : `None | list<str>`
    """
    output = await get_autocomplete_suggestions_for_emoji_name(interaction_event, emoji_name)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
