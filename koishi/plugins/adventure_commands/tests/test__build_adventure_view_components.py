import vampytest
from hata import Component, create_button, create_row, create_section, create_separator, create_text_display

from ...adventure_core import (
    ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, ACTION_ID_SYSTEM_CANCELLATION_NOW,
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_FINALISED, LOCATIONS,
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOOT_STATE_SUCCESS, TARGETS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, adventure_action_create, adventure_create,
    loot_data_build
)
from ...item_core import ITEM_ID_PEACH, get_item_nullable

from ..component_building import build_adventure_view_components
from ..constants import ADVENTURE_VIEW_MODE_DEFAULT, ADVENTURE_VIEW_MODE_DETAILED, EMOJI_REFRESH


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    adventure_entry_id = 9999
    user_id = 202508040004
    
    adventure_action_0 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463184000,
        None,
        None,
        0,
        10,
    )
    
    adventure_action_1 = adventure_action_create(
        ACTION_ID_SYSTEM_CANCELLATION_NOW,
        1463270400,
        None,
        None,
        0,
        0,
    )
    
    adventure = adventure_create(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    adventure.energy_exhausted = 10
    adventure.created_at = 1463097600
    adventure.state = ADVENTURE_STATE_CANCELLED
    adventure.action_listing = [adventure_action_0, adventure_action_1]
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        ADVENTURE_VIEW_MODE_DEFAULT,
        False,
        0,
        56000,
        12000,
        1463356800,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                'Departed at: 2016-05-13 00:00:00 UTC\n'
                'Used health: 0 / 100\n'
                'Used energy: 10 / 100\n'
                'Used inventory: 12 / 56 kg\n'
                'Elapsed time: 3 days\n'
                'You are currently returning home.'
            ),
            create_separator(),
            create_section(
                create_text_display(
                    f'<t:{adventure.created_at}:T> Depart'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = 'adventure.action.view.depart',
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_0.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{0:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}.{False:x}.{0:x}'
                    ),
                    enabled = True,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_1.created_at}:T> Cancellation'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{1:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Back to adventures',
                    enabled = False,
                    custom_id = f'adventure.listing.{user_id:x}.{0:x}',
                ),
                create_button(
                    'View all action',
                    enabled = False,
                    custom_id = (
                        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{False:x}.{0:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Cancel',
                    enabled = False,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
                create_button(
                    'Detailed',
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{False:x}.{0:x}'
                    ),
                ),
            ),
        ],
    )
    
    
    adventure_entry_id = 9999
    user_id = 202508040005
    
    adventure_action_0 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463184000,
        None,
        None,
        0,
        0,
    )
    
    adventure_action_1 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463270400,
        None,
        None,
        0,
        0,
    )
    
    adventure_action_2 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463270400 + 3600 * 1,
        None,
        None,
        0,
        0,
    )
    
    adventure_action_3 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463270400 + 3600 * 2,
        None,
        None,
        0,
        0,
    )
    
    adventure_action_4 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463270400 + 3600 * 3,
        None,
        None,
        0,
        0,
    )
    
    adventure_action_5 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463270400 + 3600 * 4,
        None,
        loot_data_build([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
        ]),
        0,
        0,
    )
    
    
    adventure = adventure_create(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    adventure.state = ADVENTURE_STATE_ACTIONING
    adventure.created_at = 1463097600
    adventure.action_listing = [
        adventure_action_0,
        adventure_action_1,
        adventure_action_2,
        adventure_action_3,
        adventure_action_4,
        adventure_action_5,
    ]
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        ADVENTURE_VIEW_MODE_DEFAULT,
        True,
        56,
        56000,
        12000,
        1463356800,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                'Departed at: 2016-05-13 00:00:00 UTC\n'
                'Used health: 0 / 100\n'
                'Used energy: 0 / 100\n'
                'Used inventory: 12 / 56 kg\n'
                'Elapsed time: 3 days\n'
                'You are currently working on your target task.'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({5 * item_peach.weight / 1000:.02f} kg)'
            ),
            create_separator(),
            create_text_display('+ 2 truncated (showing latest 5)'),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_1.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{1:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_2.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{2:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_3.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{3:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_4.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{4:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_5.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{5:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = True,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}'
                    ),
                ),
                create_button(
                    'Back to adventures',
                    enabled = True,
                    custom_id = f'adventure.listing.{user_id:x}.{56:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = (
                        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{56:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Cancel',
                    enabled = True,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
                create_button(
                    'Detailed',
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}'
                    ),
                ),
            ),
        ],
    )
    
    
    yield (
        adventure,
        ADVENTURE_VIEW_MODE_DETAILED,
        True,
        56,
        56000,
        12000,
        1463356800,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(

                '- Departed at\n'
                '  - 2016-05-13 00:00:00 UTC\n'
                '- Used health\n'
                '  - 0 / 100\n'
                '- Used energy\n'
                '  - 0 / 100\n'
                '- Used inventory\n'
                '  - 12 / 56 kg\n'
                '- Elapsed time\n'
                '  - 3 days\n'
                '- Adventure settings\n'
                '  - Duration\n'
                '    - 0 second, return unknown\n'
                'You are currently working on your target task.'
            ),
            create_separator(),
            create_text_display(
                f'### Loot (this step):\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({5 * item_peach.weight / 1000:.02f} kg)'
            ),
            create_separator(),
            create_text_display(
                f'### Total loot:\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({5 * item_peach.weight / 1000:.02f} kg)'
            ),
            create_separator(),
            create_text_display('+ 2 truncated (showing latest 5)'),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_1.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{1:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_2.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{2:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_3.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{3:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_4.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{4:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = False,
                ),
            ),
            create_section(
                create_text_display(
                    f'<t:{adventure_action_5.created_at}:T> Gardening'
                ),
                thumbnail = create_button(
                    'View',
                    custom_id = (
                        f'adventure.action.view.{user_id:x}.{adventure_entry_id:x}.{5:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{False:x}.{0:x}'
                    ),
                    enabled = True,
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}'
                    ),
                ),
                create_button(
                    'Back to adventures',
                    enabled = True,
                    custom_id = f'adventure.listing.{user_id:x}.{56:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = (
                        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{56:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Cancel',
                    enabled = True,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
            ),
        ],
    )
    
    
    adventure_entry_id = 9999
    user_id = 202508040006
    
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    adventure_action_0 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463184000,
        None,
        loot_data_build([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 5),
        ]),
        0,
        10,
    )
    
    adventure_action_1 = adventure_action_create(
        ACTION_ID_SYSTEM_CANCELLATION_NOW,
        1463270400,
        None,
        None,
        0,
        0,
    )
    
    adventure = adventure_create(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    adventure.energy_exhausted = 10
    adventure.created_at = 1463097600
    adventure.updated_at = 1463356800
    adventure.state = ADVENTURE_STATE_FINALISED
    adventure.action_listing = [adventure_action_0, adventure_action_1]
    adventure.entry_id = adventure_entry_id
    
    yield (
        adventure,
        ADVENTURE_VIEW_MODE_DEFAULT,
        True,
        4,
        0,
        0,
        1463356800,
        [
            create_text_display(
                f'### Adventure to {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}'
            ),
            create_separator(),
            create_text_display(
                'Departed at: 2016-05-13 00:00:00 UTC\n'
                'Used health: 0 / 100\n'
                'Used energy: 10 / 100\n'
                'Total duration: 3 days\n'
                'Recovery time: 20 minutes'
            ),
            create_separator(),
            create_text_display(
                f'### Loot:\n'
                f'- {item_peach.emoji} {item_peach.name} x5 ({5 * item_peach.weight / 1000:.02f} kg)'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Refresh',
                    EMOJI_REFRESH,
                    enabled = False,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{4:x}'
                    ),
                ),
                create_button(
                    'Back to adventures',
                    enabled = True,
                    custom_id = f'adventure.listing.{user_id:x}.{4:x}',
                ),
                create_button(
                    'View all action',
                    enabled = True,
                    custom_id = (
                        f'adventure.action_listing.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DEFAULT:x}.'
                        f'{True:x}.{4:x}.{0:x}'
                    ),
                ),
                create_button(
                    'Cancel',
                    enabled = False,
                    custom_id = f'adventure.cancel.{user_id:x}.{adventure_entry_id:x}',
                ),
                create_button(
                    'Detailed',
                    enabled = True,
                    custom_id = (
                        f'adventure.view.{user_id:x}.{adventure_entry_id:x}.{ADVENTURE_VIEW_MODE_DETAILED:x}.'
                        f'{True:x}.{4:x}'
                    ),
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_view_components(
    adventure,
    adventure_view_mode,
    allow_switching_to_adventure_listing_view,
    adventure_listing_page_index,
    inventory_total,
    inventory_exhausted,
    now,
):
    """
    Tests whether ``build_adventure_view_components`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The parent adventure.
    
    adventure_view_mode : `int`
        How to render the adventure.
    
    allow_switching_to_adventure_listing_view : `bool`
        Whether switching to adventure listing is allowed from adventure view.
    
    adventure_listing_page_index : `int`
        Adventure listing page index to direct to from adventure view.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    now : `int`
        The current time.
    
    Returns
    -------
    output : ``list<Component>``
    """
    def unix_time_seconds_get_patched():
        nonlocal now
        return now
    
    
    mocked = vampytest.mock_globals(
        build_adventure_view_components,
        2,
        unix_time_seconds_get = unix_time_seconds_get_patched,
    )
    
    output = mocked(
        adventure,
        adventure_view_mode,
        allow_switching_to_adventure_listing_view,
        adventure_listing_page_index,
        inventory_total,
        inventory_exhausted,
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
