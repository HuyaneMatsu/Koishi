import vampytest

from ..characters import KOMEIJI_KOISHI, REIUJI_UTSUHO, SHAMEIMARU_AYA
from ..utils import get_touhou_character_like


def _iter_options():
    yield 'Komeiji Koishi', KOMEIJI_KOISHI
    yield 'aya', SHAMEIMARU_AYA
    yield 'oguu', REIUJI_UTSUHO
    yield 'Gilgamesh', None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_touhou_character_like(value):
    """
    tests whether ``get_touhou_character_like`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to query for.
    
    Returns
    -------
    output : `None | TouhouCharacter`
    """
    return get_touhou_character_like(value)
