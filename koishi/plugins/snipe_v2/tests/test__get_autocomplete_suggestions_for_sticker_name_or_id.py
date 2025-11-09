import vampytest
from hata import Sticker, Guild, InteractionEvent

from ..responding_helpers import get_autocomplete_suggestions_for_sticker_name_or_id


def _iter_options():
    sticker_id_0 = 202511010080
    sticker_id_1 = 202511010081
    sticker_id_2 = 202511010082
    
    guild_id_0 = 202511010083
    
    interaction_event_id_0 = 202511010084
    
    sticker_0 = Sticker.precreate(
        sticker_id_0,
        guild_id = guild_id_0,
        name = 'OrinCarting',
    )
    
    sticker_1 = Sticker.precreate(
        sticker_id_1,
        guild_id = guild_id_0,
        name = 'OrinShock',
    )
    
    sticker_2 = Sticker.precreate(
        sticker_id_2,
        guild_id = guild_id_0,
        name = 'KoishiShock',
    )
    
    guild_0 = Guild.precreate(
        guild_id_0,
        stickers = [
            sticker_0,
            sticker_1,
            sticker_2,
        ],
    )
    
    interaction_event_0 = InteractionEvent.precreate(
        interaction_event_id_0,
        guild = guild_0,
    )
    
    yield (
        interaction_event_0,
        str(sticker_0.id),
        [],
        [
            str(sticker_0.id),
        ]
    )
    
    yield (
        interaction_event_0,
        'shock',
        [
            guild_0,
        ],
        [
            sticker_1.name,
            sticker_2.name,
        ],
    )
    
    yield (
        interaction_event_0,
        'okuu',
        [],
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_autocomplete_suggestions_for_sticker_name_or_id(interaction_event, sticker_name_or_id, entity_cache):
    """
    Gets auto-complete suggestion for the given sticker's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sticker_name_or_id : `None | str`
        The typed value.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : `None | list<str>`
    """
    output = await get_autocomplete_suggestions_for_sticker_name_or_id(interaction_event, sticker_name_or_id)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
