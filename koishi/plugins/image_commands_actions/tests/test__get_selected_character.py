import vampytest

from ...touhou_core import KOMEIJI_KOISHI, TouhouCharacter

from ..action_filtering import PARAMETER_WILD_CARD, get_selected_character


def _iter_options():
    yield None, None
    yield PARAMETER_WILD_CARD, None
    yield PARAMETER_WILD_CARD.upper(), None
    yield KOMEIJI_KOISHI.name, KOMEIJI_KOISHI
    yield KOMEIJI_KOISHI.name.upper(), KOMEIJI_KOISHI
    yield 'koishi', KOMEIJI_KOISHI
    yield 'koishi'.upper(), KOMEIJI_KOISHI


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_selected_character(character_name):
    """
    Tests whether ``get_selected_character`` works as intended.
    
    Parameters
    ----------
    character_name : `None | str`
        Character name to get character for.
    
    Returns
    -------
    output : `None | TouhouCharacter`
    """
    output = get_selected_character(character_name)
    vampytest.assert_instance(output, TouhouCharacter, nullable = True)
    return output
