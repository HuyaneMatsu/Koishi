import vampytest

from ....plugins.touhou_core import YAKUMO_RAN, YAKUMO_YUKARI

from ..building import _get_character_names


def _iter_options():
    yield None, None
    yield (YAKUMO_RAN,), (YAKUMO_RAN.name,)
    yield (YAKUMO_RAN, YAKUMO_YUKARI), (YAKUMO_RAN.name, YAKUMO_YUKARI.name)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_get_character_names(strings):
    """
    Tests whether ``_get_character_names`` works as intended.
    
    Parameters
    ----------
    characters : `None | tuple<TouhouCharacter>`
        Characters to get their names of.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = _get_character_names(strings)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
