import vampytest
from hata import Component, create_text_display

from ...touhou_character_preference import CharacterPreference

from ..builders import build_character_preference_components


def _iter_options():
    character_preferences = [
        CharacterPreference(0, 'komeiji_koishi'),
        CharacterPreference(0, 'komeiji_satori'),
    ]
    
    yield (
        character_preferences,
        [
            create_text_display(
                'Komeiji Koishi\n'
                'Komeiji Satori'
            ),
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_character_preference_components(character_preferences):
    """
    Tests whether ``build_character_preference_components`` works as intended.
    
    Parameters
    ----------
    character_preferences : ``None | list<CharacterPreference>``
        The user's character preferences if any.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_character_preference_components(character_preferences)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
