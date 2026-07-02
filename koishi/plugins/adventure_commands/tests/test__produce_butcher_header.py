import vampytest

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..content_building import produce_butcher_header


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        item_peach,
        f'# Butchering {item_peach.emoji} {item_peach.name}'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_butcher_header(item):
    """
    Tests whether ``produce_butcher_header`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to produce header for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_butcher_header(item)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
