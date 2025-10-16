import vampytest
from hata import Component, create_text_display

from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..builders import build_character_preference_change_components


def _iter_options():
    yield (
        KOMEIJI_KOISHI,
        True,
        [
            create_text_display(
                'From now on **Komeiji Koishi** is associate with you.',
            )
        ],
    )
    
    yield (
        KOMEIJI_SATORI,
        False,
        [
            create_text_display(
                'From now on wont associate **Komeiji Satori** with you.',
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_character_preference_change_components(character, added):
    """
    Tests whether ``build_character_preference_change_components`` works as intended.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The touhou character added / removed.
    
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    components : ``list<Component>``
    """
    output = build_character_preference_change_components(character, added)
    
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
