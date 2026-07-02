from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import (
    Component, Icon, IconType, User, create_button, create_section, create_separator, create_text_display,
    create_thumbnail_media
)

from ...item_core import ITEM_FLAG_BUTCHERABLE, Item, OptionButcher

from ..component_building import build_butcher_components


def _iter_options():
    user_id = 202606250001
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2), name = 'Koishi')
    
    item_id_0 = 10
    item_id_1 = 11
    item_id_2 = 12
    
    now = DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc)
    
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
            OptionButcher(True, 1, 2, 3, item_id_2, 10, 11, 13),
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
        user,
        0,
        item_0,
        0,
        0,
        2.0,
        None,
        0,
        None,
        None,
        None,
        0,
        now,
        None,
        items,
        [
            create_section(
                create_text_display(
                    f'# Butchering {item_0.name}'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id}/00000000000000000000000000000002.png',
                )
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_0.name} costing up to 25 energy, for:\n'
                    f'- 75% chance of 3 {item_2.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.i.{user_id:x}.{item_id_0:x}',
                    enabled = True,
                ),
            ),
        ],
    )
    
    yield (
        user,
        0,
        item_0,
        127,
        0,
        2.0,
        [
            (item_id_2, 3),
        ],
        25,
        [
            (item_2, 0),
            (item_2, 1),
            (item_2, 2),
        ],
        item_0,
        [
            (item_id_2, 3),
        ],
        25,
        now,
        now + TimeDelta(seconds = 12),
        items,
        [
            create_section(
                create_text_display(
                    f'# Butchering {item_0.name}'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id}/00000000000000000000000000000002.png',
                )
            ),
            create_text_display(
                f'### Butchered {item_0.name}\n'
                f'Used energy: 25\n'
                f'Butchered:\n'
                f'- 3 {item_2.name}'
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                    f'- 51% chance of 600 {item_1.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{0:x}.{0:x}.AAAAAAAAAEA=',
                    enabled = True,
                ),
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                    f'- 51% chance of 600 {item_1.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{0:x}.{1:x}.AAAAAAAAAEA=',
                    enabled = True,
                ),
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                    f'- 51% chance of 600 {item_1.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{0:x}.{2:x}.AAAAAAAAAEA=',
                    enabled = True,
                ),
            ),
            create_separator(),
            create_text_display(
                f'You are recovering for 12 seconds, until <t:{(now + TimeDelta(seconds = 12)).timestamp():.0f}:T>.'
            ),
        ],
    )
    
    yield (
        user,
        0,
        item_0,
        127,
        2,
        2.0,
        [
            (item_id_2, 2),
            (item_id_1, 400),
        ],
        3999,
        [
            (item_2, 0),
            (item_2, 2),
        ],
        item_2,
        [
            (item_id_1, 400),
        ],
        3974,
        now,
        None,
        items,
        [
            create_section(
                create_text_display(
                    f'# Butchering {item_0.name}'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id}/00000000000000000000000000000002.png',
                )
            ),
            create_text_display(
                f'### Butchered {item_2.name}\n'
                f'Used energy: 3974\n'
                f'Butchered:\n'
                f'- 400 {item_1.name}'
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                    f'- 51% chance of 600 {item_1.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{2:x}.{0:x}.AAAAAAAAAEA=',
                    enabled = True,
                ),
            ),
            create_section(
                create_text_display(
                    f'### Butcher {item_2.name} costing up to 4314 energy, for:\n'
                    f'- 51% chance of 600 {item_1.name}'
                ),
                thumbnail = create_button(
                    'Butcher',
                    custom_id = f'adventure.butcher.c.{user_id:x}.{item_id_0:x}.{127:x}.{2:x}.{2:x}.AAAAAAAAAEA=',
                    enabled = True,
                ),
            ),
            create_text_display(
                f'### Total\n'
                f'Used energy: 3999\n'
                f'Butchered:\n'
                f'- 2 {item_2.name}\n'
                f'- 400 {item_1.name}'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_butcher_components(
    user,
    guild_id,
    initial_item,
    seed,
    butcher_flags,
    multiplier,
    butcher_amounts_accumulated,
    energy_cost_accumulated,
    butcherables,
    butchered_item,
    butcher_amounts,
    energy_cost,
    now,
    recovering_until,
    items,
):
    """
    Tests whether ``build_butcher_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user invoking the interaction.
    
    guild_id : `int`
        The local guild's identifier.
    
    initial_item : ``Item``
        Item to butcher.
    
    seed : `int`
        Seed to use for butchering.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    now : `DateTime`
        The current date time.
    
    recovering_until : `None | DateTime`
        Until when the user is recovering for.
    
    items : ``dict<int, Item>``
        Items to use.
    
    Returns
    -------
    output : ``list<Component>``
    """
    mocked = vampytest.mock_globals(
        build_butcher_components,
        4,
        ITEMS = items,
    )
    output = mocked(
        user,
        guild_id,
        initial_item,
        seed,
        butcher_flags,
        multiplier,
        butcher_amounts_accumulated,
        energy_cost_accumulated,
        butcherables,
        butchered_item,
        butcher_amounts,
        energy_cost,
        now,
        recovering_until,
    )
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
