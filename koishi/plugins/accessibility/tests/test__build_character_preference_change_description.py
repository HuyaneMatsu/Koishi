import vampytest

from ...touhou_core.characters import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..character_preference import build_character_preference_change_description


def _iter_options():
    yield KOMEIJI_KOISHI, True, 'From now on Komeiji Koishi is associate with you.'
    yield KOMEIJI_KOISHI, False, 'From now on wont associate Komeiji Koishi with you.'
    yield KOMEIJI_SATORI, True, 'From now on Komeiji Satori is associate with you.'
    yield KOMEIJI_SATORI, False, 'From now on wont associate Komeiji Satori with you.'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_character_preference_change_description(character, enabled):
    """
    Tests whether ``build_character_preference_change_description`` works as intended.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The touhou character added / removed.
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    output : `str`
    """
    return build_character_preference_change_description(character, enabled)
