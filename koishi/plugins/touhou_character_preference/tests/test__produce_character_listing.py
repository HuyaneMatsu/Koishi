import vampytest

from ..builders import produce_character_listing
from ..character_preference import CharacterPreference


def _iter_options():
    yield (
        None,
        (
            '*none*'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'komeiji_koishi'),
        ],
        (
            'Komeiji Koishi'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'komeiji_koishi'),
            CharacterPreference(0, 'komeiji_satori'),
        ],
        (
            'Komeiji Koishi\n'
            'Komeiji Satori'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'huyane_matsu'),
        ],
        (
            '*none*'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_character_listing(character_preferences):
    """
    Tests whether ``produce_character_listing`` works as intended.
    
    Parameters
    ----------
    character_preferences : ``None | list<CharacterPreference>``
        The user's character preferences if any.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_character_listing(character_preferences)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
