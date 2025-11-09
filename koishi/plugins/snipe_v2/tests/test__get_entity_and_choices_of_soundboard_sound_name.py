import vampytest

from hata import SoundboardSound, Guild, InteractionEvent

from ..responding_helpers import get_entity_and_choices_of_soundboard_sound_name


def _iter_options():
    soundboard_sound_id_0 = 202511010060
    soundboard_sound_id_1 = 202511010061
    soundboard_sound_id_2 = 202511010062
    
    guild_id_0 = 202511010063
    
    interaction_event_id_0 = 202511010064
    
    soundboard_sound_0 = SoundboardSound.precreate(
        soundboard_sound_id_0,
        guild_id = guild_id_0,
        name = 'OrinCarting',
    )
    
    soundboard_sound_1 = SoundboardSound.precreate(
        soundboard_sound_id_1,
        guild_id = guild_id_0,
        name = 'OrinShock',
    )
    
    soundboard_sound_2 = SoundboardSound.precreate(
        soundboard_sound_id_2,
        guild_id = guild_id_0,
        name = 'KoishiShock',
    )
    
    guild_0 = Guild.precreate(
        guild_id_0,
        soundboard_sounds = [
            soundboard_sound_0,
            soundboard_sound_1,
            soundboard_sound_2,
        ],
    )
    
    interaction_event_0 = InteractionEvent.precreate(
        interaction_event_id_0,
        guild = guild_0,
    )
    
    yield (
        interaction_event_0,
        'shock',
        [
            guild_0,
        ],
        (
            soundboard_sound_1,
            [
                soundboard_sound_1,
                soundboard_sound_2,
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
async def test__get_entity_and_choices_of_soundboard_sound_name(
    interaction_event, soundboard_sound_name, entity_cache
):
    """
    Tests whether ``get_entity_and_choices_of_soundboard_sound_name`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    soundboard_sound_name : `str`
        The soundboard_sound's name.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : ``(None | SoundboardSound, None | list<SoundboardSound>)``
    """
    async def request_soundboard_sounds_of_patched(guild):
        nonlocal interaction_event
        vampytest.assert_is(interaction_event.guild, guild)
    
    mocked = vampytest.mock_globals(
        get_entity_and_choices_of_soundboard_sound_name,
        request_soundboard_sounds_of = request_soundboard_sounds_of_patched,
    )
    output = await mocked(interaction_event, soundboard_sound_name)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    entity, choices = output
    vampytest.assert_instance(entity, SoundboardSound, nullable = True)
    
    vampytest.assert_instance(choices, list, nullable = True)
    if (choices is not None):
        for element in choices:
            vampytest.assert_instance(element, SoundboardSound)
    
    return output
