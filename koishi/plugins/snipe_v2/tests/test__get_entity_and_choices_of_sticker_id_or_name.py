import vampytest

from hata import Sticker, Guild, InteractionEvent

from ..responding_helpers import get_entity_and_choices_of_sticker_name_or_id


def _iter_options():
    sticker_id_0 = 202511010050
    sticker_id_1 = 202511010051
    sticker_id_2 = 202511010052
    
    guild_id_0 = 202511010053
    
    interaction_event_id_0 = 202511010054
    
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
        [
            sticker_0,
        ],
        sticker_0,
        (
            sticker_0,
            None,
        ),
    )
    
    yield (
        interaction_event_0,
        str(sticker_0.id),
        [
            sticker_0,
        ],
        None,
        (
            None,
            None,
        ),
    )
    
    yield (
        interaction_event_0,
        'shock',
        [
            guild_0,
        ],
        None,
        (
            sticker_1,
            [
                sticker_1,
                sticker_2,
            ],
        ),
    )
    
    yield (
        interaction_event_0,
        'okuu',
        [],
        None,
        (
            None,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_entity_and_choices_of_sticker_name_or_id(interaction_event, sticker_name, entity_cache, request_response):
    """
    Tests whether ``get_entity_and_choices_of_sticker_name_or_id`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sticker_name : `str`
        The sticker's name.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    request_response : ``None | Sticker``
        Response to return from a get sticker call.
    
    Returns
    -------
    output : ``(None | Sticker, None | list<Sticker>)``
    """
    async def get_sticker_patched(sticker_id):
        nonlocal request_response
        if request_response is None:
            return None
        
        vampytest.assert_eq(sticker_id, request_response.id)
        return request_response
    
    mocked = vampytest.mock_globals(
        get_entity_and_choices_of_sticker_name_or_id,
        get_sticker = get_sticker_patched,
    )
    output = await mocked(interaction_event, sticker_name)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    entity, choices = output
    vampytest.assert_instance(entity, Sticker, nullable = True)
    
    vampytest.assert_instance(choices, list, nullable = True)
    if (choices is not None):
        for element in choices:
            vampytest.assert_instance(element, Sticker)
    
    return output
