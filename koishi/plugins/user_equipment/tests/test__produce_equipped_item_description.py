import vampytest

from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..content_building import produce_equipped_item_description


def _iter_options():
    item = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        'Head accessory',
        None,
        None,
        'Hairband',
        (
            f'### Head accessory: Hairband'
        ),
    )
    
    yield (
        'Head accessory',
        item,
        None,
        'Hairband',
        (
            f'### Head accessory: {item.emoji} {item.name}\n'
            '- +1 Housewife capabilities\n'
            '- +1 Bedroom skills\n'
            '- +1 Loyalty\n'
            '- -20% Fishing'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_produce_equipped_item_description(title, item, item_emoji_default, item_name_default):
    """
    Tests whether ``produce_equipped_item_description`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Title to show.
    
    item : ``None | Item``
        Item to render.
    
    item_emoji_default : ``None | Emoji``
        Emoji to use if item is `None`.
    
    item_name_default : ``None | Emoji``
        Name to use if item is `None`.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_equipped_item_description(title, item, item_emoji_default, item_name_default)]
    for element in output:
        vampytest.assert_instance(element, str)
    return ''.join(output)
