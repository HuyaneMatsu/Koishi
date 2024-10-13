import vampytest

from ..utils import get_touhou_character_names_like


def _iter_options():
    yield 'Komeiji Koishi', ['komeiji koishi']
    yield 'aya', ['ayana', 'aya', 'layla', 'sakuya', 'kaguya']
    yield 'oguu', ['okuu']
    yield 'Gilgamesh', []


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_touhou_character_names_like(value):
    """
    tests whether ``get_touhou_character_names_like`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to query for.
    
    Returns
    -------
    output : `list<str>`
    """
    return get_touhou_character_names_like(value)
