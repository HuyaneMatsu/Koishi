import vampytest

from ..component_builders import produce_adventure_listing_view_header


def _iter_options():
    yield (
        0,
        f'### Adventures (page 1)',
    )
    yield (
        100,
        '### Adventures (page 101)',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_listing_view_header(page_index):
    """
    Tests whether ``produce_adventure_listing_view_header`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        The shown page's index.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_listing_view_header(page_index)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
