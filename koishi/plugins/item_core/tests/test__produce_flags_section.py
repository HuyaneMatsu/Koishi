import vampytest

from ..content_building import produce_flags_section
from ..flags import ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE


def _iter_options():
    yield (
        (ITEM_FLAG_EDIBLE | ITEM_FLAG_COSTUME),
        (
            '- Edible\n'
            '- Costume'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_flags_section(flags):
    """
    Tests whether ``produce_flags_section`` works as intended.
    
    Parameters
    ----------
    flags : `int`
        Item flags to produce.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_flags_section(flags)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
