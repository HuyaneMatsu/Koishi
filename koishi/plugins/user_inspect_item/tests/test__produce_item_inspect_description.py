import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..content_building import produce_item_inspect_description


def _iter_options():
    item = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        item,
        (
            f'## {item.emoji} {item.name}\n'
            f'\n'
            f'{item.description}\n'
            f'\n'
            f'### Trading information\n'
            f'Weight: 1.018 kg\n'
            f'Value: 3000 {EMOJI__HEART_CURRENCY}\n'
            f'### Categories\n'
            f'- Weapon\n'
            f'### Modifiers\n'
            f'- +1 Housewife capabilities\n'
            f'- +1 Bedroom skills\n'
            f'- +1 Loyalty\n'
            f'- -20% Fishing'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_item_inspect_description(item):
    """
    Tests whether ``produce_item_inspect_description`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_item_inspect_description(item)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
