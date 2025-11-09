import vampytest

from hata import Emoji, Guild, InteractionEvent

from ..responding_helpers import get_entity_and_choices_of_emoji_name


def _iter_options():
    emoji_id_0 = 202511010040
    emoji_id_1 = 202511010041
    emoji_id_2 = 202511010042
    
    guild_id_0 = 202511010043
    
    interaction_event_id_0 = 202511010044
    
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
        (
            emoji_0,
            None,
        ),
    )
    
    yield (
        interaction_event_0,
        'shock',
        [
            guild_0,
        ],
        (
            emoji_1,
            [
                emoji_1,
                emoji_2,
            ],
        ),
    )
    
    yield (
        interaction_event_0,
        'okuu',
        [],
        (
            None,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_entity_and_choices_of_emoji_name(interaction_event, emoji_name, entity_cache):
    """
    Tests whether ``get_entity_and_choices_of_emoji_name`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    emoji_name : `str`
        The emoji's name.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : ``(None | Emoji, None | list<Emoji>)``
    """
    output = get_entity_and_choices_of_emoji_name(interaction_event, emoji_name)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    entity, choices = output
    vampytest.assert_instance(entity, Emoji, nullable = True)
    
    vampytest.assert_instance(choices, list, nullable = True)
    if (choices is not None):
        for element in choices:
            vampytest.assert_instance(element, Emoji)
    
    return output
