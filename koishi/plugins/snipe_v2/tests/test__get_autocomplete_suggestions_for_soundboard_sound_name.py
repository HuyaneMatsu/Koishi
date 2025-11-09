import vampytest
from hata import SoundboardSound, Guild, InteractionEvent

from ..responding_helpers import get_autocomplete_suggestions_for_soundboard_sound_name


def _iter_options():
    soundboard_sound_id_0 = 202511010080
    soundboard_sound_id_1 = 202511010081
    soundboard_sound_id_2 = 202511010082
    
    guild_id_0 = 202511010083
    
    interaction_event_id_0 = 202511010084
    
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
        [
            soundboard_sound_1.name,
            soundboard_sound_2.name,
        ],
    )
    
    yield (
        interaction_event_0,
        'okuu',
        [],
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_autocomplete_suggestions_for_soundboard_sound_name(interaction_event, soundboard_sound_name_or_id, entity_cache):
    """
    Gets auto-complete suggestion for the given soundboard_sound's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    soundboard_sound_name_or_id : `None | str`
        The typed value.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : `None | list<str>`
    """
    async def request_soundboard_sounds_of_patched(guild):
        nonlocal interaction_event
        vampytest.assert_instance(interaction_event.guild, guild)
    
    mocked = vampytest.mock_globals(
        get_autocomplete_suggestions_for_soundboard_sound_name,
        request_soundboard_sounds_of = request_soundboard_sounds_of_patched,
    )
    
    mocked = get_autocomplete_suggestions_for_soundboard_sound_name
    output = await mocked(interaction_event, soundboard_sound_name_or_id)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
