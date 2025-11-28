import vampytest
from hata import User

from ..content_building import produce_inventory_header


def _iter_options():
    user = User.precreate(202511110020, name = 'Alice')
    
    yield (
        user,
        0,
        1,
        0,
        0,
        1335,
        63122,
        (
            f'# {user.name}\'s inventory\n'
            f'\n'
            f'Page: 2; Sort by: name; Sort order: increasing\n'
            f'Weight: 1.335 / 63.122 kg'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_inventory_header(user, guild_id, page_index, sort_by, sort_order, weight, capacity):
    """
    Tests whether ``produce_inventory_header`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's inventory is being rendered.
    
    guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The current page's index.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_inventory_header(user, guild_id, page_index, sort_by, sort_order, weight, capacity)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
