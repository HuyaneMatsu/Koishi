import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_claim_many_listing_description


def _iter_options():
    item = get_item_nullable(ITEM_ID_PEACH)
    assert item is not None
    
    yield (
        [
            (True, item, 56, 1000, 0),
        ],
        (
            f'You received the 56 {item.emoji} {item.name} ({item.weight * 56 / 1000:.03f} kg), '
            f'that you purchased for 1000 {EMOJI__HEART_CURRENCY}.'
        ),
    )
    
    yield (
        [
            (True, item, 56, 1000, 0),
            (False, item, 5, 1000, 0),
        ],
        (
            f'You received the 56 {item.emoji} {item.name} ({item.weight * 56 / 1000:.03f} kg), '
            f'that you purchased for 1000 {EMOJI__HEART_CURRENCY}.\n'
            f'You received 1000 {EMOJI__HEART_CURRENCY}, '
            f'for selling 5 {item.emoji} {item.name} ({item.weight * 5 / 1000:.03f} kg).'
        ),
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_claim_many_listing_description(claim_elements):
    """
    Tests whether ``produce_claim_many_listing_description`` works as intended.
    
    Parameters
    ----------
    claim_elements : ``list<(bool, Item, int, int, int)>``
        Elements to produce through.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_claim_many_listing_description(claim_elements)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
