import vampytest

from ...touhou_character_preference import CharacterPreference

from ..character_preference import build_character_listing


def _iter_options():
    yield (
        None,
        (
            '```\n'
            '*none*\n'
            '```'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'komeiji_koishi'),
        ],
        (
            '```\n'
            'Komeiji Koishi\n'
            '```'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'komeiji_koishi'),
            CharacterPreference(0, 'komeiji_satori'),
        ],
        (
            '```\n'
            'Komeiji Koishi\n'
            'Komeiji Satori\n'
            '```'
        ),
    )
    
    yield (
        [
            CharacterPreference(0, 'huyane_matsu'),
        ],
        (
            '```\n'
            '*none*\n'
            '```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_character_listing(character_preferences):
    """
    Tests whether ``build_character_listing`` works as intended.
    
    Parameters
    ----------
    character_preferences : `None | list<CharacterPreference>`
        The user's character preferences if any.
    
    Returns
    -------
    character_listing : `str`
    """
    return build_character_listing(character_preferences)
