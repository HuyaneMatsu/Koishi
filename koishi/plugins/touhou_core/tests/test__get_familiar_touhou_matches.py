import vampytest

from ..characters import HOURAISAN_KAGUYA, IZAYOI_SAKUYA, KOMEIJI_KOISHI, REIUJI_UTSUHO, SHAMEIMARU_AYA
from ..utils import get_familiar_touhou_matches


def _iter_options():
    yield 'Komeiji Koishi', [(KOMEIJI_KOISHI, 'komeiji koishi')]
    yield 'aya', [(SHAMEIMARU_AYA, 'aya'), (IZAYOI_SAKUYA, 'sakuya'), (HOURAISAN_KAGUYA, 'kaguya')]
    yield 'oguu', [(REIUJI_UTSUHO, 'okuu')]
    yield 'Gilgamesh', []


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_familiar_touhou_matches(value):
    """
    tests whether ``get_familiar_touhou_matches`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to query for.
    
    Returns
    -------
    output : `list<(TouhouCharacter, str)>`
    """
    return get_familiar_touhou_matches(value)
