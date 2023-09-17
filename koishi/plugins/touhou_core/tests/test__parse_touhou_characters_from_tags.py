import vampytest

from ...image_handling_core import ImageDetail

from ..characters import KOMEIJI_KOISHI, KOMEIJI_SATORI
from ..tags import parse_touhou_characters_from_tags


def _iter_options():
    yield ImageDetail('https://www.orindance.party/'), set()
    yield ImageDetail('https://www.orindance.party/').with_tags(frozenset(('aya', 'sitting'),)), set()
    yield (
        ImageDetail('https://www.orindance.party/').with_tags(frozenset(('komeiji_koishi', 'komeiji_satori'),)),
        {KOMEIJI_KOISHI, KOMEIJI_SATORI},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_touhou_characters_from_tags(image_detail):
    """
    Tests whether ``parse_touhou_characters_from_tags`` works as intended.
    
    Parameters
    ----------
    image_detail : ``ImageDetail``
        Image detail to parse characters of.
    
    Returns
    -------
    output : `set<TouhouCharacter>`
    """
    return parse_touhou_characters_from_tags(image_detail)
