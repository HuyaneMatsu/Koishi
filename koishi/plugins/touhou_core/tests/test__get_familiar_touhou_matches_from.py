import vampytest

from ..characters import KOMEIJI_KOISHI, REIUJI_UTSUHO, SHAMEIMARU_AYA
from ..utils import get_familiar_touhou_matches_from


def _iter_options():
    yield 'Komeiji Koishi', [KOMEIJI_KOISHI], [(KOMEIJI_KOISHI, 'komeiji koishi')]
    yield 'Komeiji Koishi', [SHAMEIMARU_AYA], []
    yield 'aya', [SHAMEIMARU_AYA, REIUJI_UTSUHO], [(SHAMEIMARU_AYA, 'aya')]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_familiar_touhou_matches_from(value, characters):
    """
    tests whether ``get_familiar_touhou_matches_from`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to query for.
    characters : `list<TouhouCharacter>`
        Characters to query from.
    
    Returns
    -------
    output : `list<(TouhouCharacter, str)>`
    """
    return get_familiar_touhou_matches_from(value, characters)
