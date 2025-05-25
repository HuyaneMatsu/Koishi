import vampytest

from hata import Component, create_text_display

from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_item_components


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        item_id,
        [
            create_text_display(
                f'**Item information: {item.name} {item.emoji}**\n'
                f'\n'
                f'{item.description}'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_item_components(item_id):
    """
    Tests whether ``build_item_components`` works as intended.
    
    Parameters
    ----------
    item_id : `int`
        The item's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_item_components(item_id)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
