import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..constants import TOP_LIST_TYPE_BALANCE, TOP_LIST_TYPE_CREDIBILITY
from ..content_building import produce_top_list_header


def _iter_options():
    yield (
        TOP_LIST_TYPE_BALANCE,
        0,
        (
            f'# {EMOJI__HEART_CURRENCY} top-list\n'
            f'\n'
            f'Page: 1'
        ),
    )
    
    yield (
        TOP_LIST_TYPE_CREDIBILITY,
        1,
        (
            f'# Credibility top-list\n'
            f'\n'
            f'Page: 2'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_top_list_header(top_list_type, page_index):
    """
    Tests whether ``produce_top_list_header`` works as intended.
    
    Parameters
    ----------
    top_list_type : `int`
        Top list's type.
    
    page_index : `int`
        Page index.
    
    Returns
    -------
    output : `str`
    """
    parts = [*produce_top_list_header(top_list_type, page_index)]
    
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
