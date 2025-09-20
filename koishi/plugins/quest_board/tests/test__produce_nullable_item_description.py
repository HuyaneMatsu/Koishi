import vampytest

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..content_builders import produce_nullable_item_description


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        item,
        (
            f'**Item information: {item.emoji} {item.name}**\n'
            f'\n'
            f'{item.description}'
        )
    )
    
    yield (
        None,
        (
            f'**Item information: unknown**\n'
            f'\n'
            f'*no description*'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_nullable_item_description(item):
    """
    Tests whether ``produce_nullable_item_description`` works as intended.
    
    Parameters
    ----------
    item : ``None | Item``
        The item to build its description of.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_nullable_item_description(item)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
