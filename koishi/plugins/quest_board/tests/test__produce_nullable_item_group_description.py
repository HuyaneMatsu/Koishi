import vampytest

from ...item_core import ITEM_GROUP_ID_KNIFE, get_item_group_nullable

from ..content_building import produce_nullable_item_group_description


def _iter_options():
    item_group_id = ITEM_GROUP_ID_KNIFE
    item_group = get_item_group_nullable(item_group_id)
    assert item_group is not None
    
    yield (
        item_group,
        (
            f'**Item group information: {item_group.emoji} {item_group.name}**\n'
            f'\n'
            f'{item_group.description}\n'
            f'\n'
            f'**Items:**\n'
            f'- Aching affection\'s Heart-piercer\n'
            f'- Kitchen knife\n'
            f'- Poking knife'
        )
    )
    
    yield (
        None,
        (
            f'**Item group information: unknown**\n'
            f'\n'
            f'*no description*\n'
            f'\n'
            f'**Items:** *none*'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_nullable_item_group_description(item_group):
    """
    Tests whether ``produce_nullable_item_group_description`` works as intended.
    
    Parameters
    ----------
    item_group : ``None | ItemGroup``
        Item group to produce its description of.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_nullable_item_group_description(item_group)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
