import vampytest
from hata import Component, create_button, create_section, create_text_display

from ...item_core import ITEM_FLAG_BUTCHERABLE, Item, OptionButcher

from ..component_building import build_butcher_option_component


def _iter_options():
    user_id = 202606250000
    
    
    item_id_0 = 10
    item_id_1 = 11
    item_id_2 = 12
    
    item_0 = Item(
        item_id_0,
        'item 0',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 100, item_id_1, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_1, 8, 13, 15),
        ),
    )
    
    item_1 = Item(
        item_id_1,
        'item 1',
        None,
        'description',
        0,
        0,
        0,
        None,
        None,
    )
    
    item_2 = Item(
        item_id_2,
        'item 2',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 100, item_id_1, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_1, 8, 13, 15),
        ),
    )
    
    items = {
        item_id_0 : item_0,
        item_id_1 : item_1,
        item_id_2 : item_2,
    }
    
    
    yield (
        user_id,
        item_0,
        None,
        0,
        0,
        2.0,
        0,
        items,
        create_section(
            create_text_display(
                f'### Butcher {item_0.name} costing up to 4314 energy, for:\n'
                f'- 51% chance of 600 {item_1.name}'
            ),
            thumbnail = create_button(
                'Butcher',
                custom_id = f'adventure.butcher.i.{user_id:x}.{item_id_0:x}',
                enabled = True,
            ),
        ),
    )
    
    yield (
        user_id,
        item_1,
        None,
        0,
        0,
        2.0,
        4,
        items,
        create_section(
            create_text_display(
                f'### Butcher {item_1.name} costing up to 0 energy, for: *none*'
            ),
            thumbnail = create_button(
                'Butcher',
                custom_id = f'adventure.butcher.d.{user_id:x}.{item_id_1:x}.{4:x}',
                enabled = False,
            ),
        ),
    )
    
    yield (
        user_id,
        item_0,
        item_2,
        127,
        3,
        2.0,
        4,
        items,
        create_section(
            create_text_display(
                f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                f'- 51% chance of 600 item 1'
            ),
            thumbnail = create_button(
                'Butcher',
                custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{3:x}.{4:x}.AAAAAAAAAEA=',
                enabled = True,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_butcher_option_component(
    user_id, initial_item, butchered_item, seed, butcher_flags, multiplier, index, items
):
    """
    Tests whether ``build_butcher_option_component`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    initial_item : ``Item`
        The item initially butchered.
    
    butchered_item : ``None | Item``
        The just butchered item.
    
    seed : `int`
        Seed to use for butchering.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    index : `int`
        The index of the item.
    
    items : ``dict<int, Item>``
        Items to use.
    
    Returns
    -------
    output : ``Component``
    """
    mocked = vampytest.mock_globals(
        build_butcher_option_component,
        3,
        ITEMS = items,
    )
    
    output = mocked(user_id, initial_item, butchered_item, seed, butcher_flags, multiplier, index)
    vampytest.assert_instance(output, Component)
    return output
