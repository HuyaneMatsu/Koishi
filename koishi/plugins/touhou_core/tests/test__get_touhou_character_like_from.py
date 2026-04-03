import vampytest

from ..characters import KOMEIJI_KOISHI, REIUJI_UTSUHO, SHAMEIMARU_AYA
from ..utils import get_touhou_character_like_from


def _iter_options():
    yield 'Komeiji Koishi', [KOMEIJI_KOISHI], KOMEIJI_KOISHI
    yield 'Komeiji Koishi', [SHAMEIMARU_AYA, REIUJI_UTSUHO], None
    yield 'aya', [SHAMEIMARU_AYA, REIUJI_UTSUHO], SHAMEIMARU_AYA


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_touhou_character_like_from(value, characters):
    """
    tests whether ``get_touhou_character_like_from`` works as intended.
    
    Parameters
    ----------
    value : `str`
        Value to query for.
    characters : `list<TouhouCharacter>`
        Characters to query from.
    
    Returns
    -------
    output : `None | TouhouCharacter`
    """
    return get_touhou_character_like_from(value, characters)
