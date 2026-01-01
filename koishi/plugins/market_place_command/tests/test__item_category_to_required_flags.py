import vampytest

from ..item_name_auto_completion import item_category_to_required_flags


def _iter_options():
    yield None, 0
    yield '8', 8
    yield '10', 16
    yield 'l', 0
    yield '0', 0


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__item_category_to_required_flags(item_category):
    """
    Tests whether ``item_category_to_required_flags`` works as intended.
    
    Parameters
    ----------
    item_category : `None | str`
        The given item category.
    
    Returns
    -------
    output : `int`
    """
    output = item_category_to_required_flags(item_category)
    vampytest.assert_instance(output, int)
    return output
