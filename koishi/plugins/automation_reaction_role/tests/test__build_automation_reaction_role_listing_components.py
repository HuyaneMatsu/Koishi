import vampytest
from hata import (
    Component, Guild, Message, create_button, create_row, create_section, create_separator, create_text_display
)

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..component_builders import build_automation_reaction_role_listing_components
from ..constants import EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT


def _iter_options():
    guild_id = 202509280000
    
    channel_id_0 = 202509280001
    channel_id_1 = 202509280002
    channel_id_2 = 202509280003
    channel_id_3 = 202509280004
    channel_id_4 = 202509280005
    channel_id_5 = 202509280006
    channel_id_6 = 202509280013
    
    message_id_0 = 202509280007
    message_id_1 = 202509280008
    message_id_2 = 202509280009
    message_id_3 = 202509280010
    message_id_4 = 202509280011
    message_id_5 = 202509280012
    message_id_6 = 202509280014
    
    entry_id_0 = 5
    entry_id_1 = 6
    entry_id_2 = 7
    entry_id_3 = 8
    entry_id_4 = 9
    entry_id_5 = 10
    entry_id_6 = 11
    
    guild = Guild.precreate(
        guild_id = guild_id,
        name = 'potato',
    )
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id,
        content = 'shrimp',
    )
    
    message_1 = Message.precreate(
        message_id_1,
        channel_id = channel_id_1,
        guild_id = guild_id,
        content = 'fry',
    )
    
    message_2 = Message.precreate(
        message_id_2,
        channel_id = channel_id_2,
        guild_id = guild_id,
    )
    
    message_3 = Message.precreate(
        message_id_3,
        channel_id = channel_id_3,
        guild_id = guild_id,
        content = 'cake',
    )
    
    message_4 = Message.precreate(
        message_id_4,
        channel_id = channel_id_4,
        guild_id = guild_id,
        content = 'cream',
    )
    
    message_5 = Message.precreate(
        message_id_5,
        channel_id = channel_id_5,
        guild_id = guild_id,
        content = 'shrimp',
    )
    
    message_6 = Message.precreate(
        message_id_6,
        channel_id = channel_id_6,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message_1,
    )
    automation_reaction_role_entry_1.entry_id = entry_id_1
    
    automation_reaction_role_entry_2 = AutomationReactionRoleEntry(
        message_2,
    )
    automation_reaction_role_entry_2.entry_id = entry_id_2
    
    automation_reaction_role_entry_3 = AutomationReactionRoleEntry(
        message_3,
    )
    automation_reaction_role_entry_3.entry_id = entry_id_3
    
    automation_reaction_role_entry_4 = AutomationReactionRoleEntry(
        message_4,
    )
    automation_reaction_role_entry_4.entry_id = entry_id_4
    
    automation_reaction_role_entry_5 = AutomationReactionRoleEntry(
        message_5,
    )
    automation_reaction_role_entry_5.entry_id = entry_id_5
    
    automation_reaction_role_entry_6 = AutomationReactionRoleEntry(
        message_6,
    )
    automation_reaction_role_entry_6.entry_id = entry_id_6
    
    yield (
        guild,
        None,
        0,
        [
            create_text_display('### Auto react roles of potato'),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    custom_id = 'automation_reaction_role.listing.decrement.disabled',
                    emoji = EMOJI_PAGE_DECREMENT,
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    custom_id = 'automation_reaction_role.listing.increment.disabled',
                    emoji = EMOJI_PAGE_INCREMENT,
                    enabled = False,
                ),
            ),
        ]
    )

    yield (
        guild,
        [
            automation_reaction_role_entry_0,
            automation_reaction_role_entry_1,
            automation_reaction_role_entry_2,
            automation_reaction_role_entry_3,
            automation_reaction_role_entry_4,
            automation_reaction_role_entry_5,
            automation_reaction_role_entry_6,
        ],
        0,
        [
            create_text_display('### Auto react roles of potato'),
            create_separator(),
            create_section(
                create_text_display(f'### {message_0.url}'),
                create_text_display('shrimp'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_0:x}.{0:x}'
                ),
            ),
            create_section(
                create_text_display(f'### {message_1.url}'),
                create_text_display('fry'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_1:x}.{0:x}'
                ),
            ),
            create_section(
                create_text_display(f'### {message_2.url}'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_2:x}.{0:x}'
                ),
            ),
            create_section(
                create_text_display(f'### {message_3.url}'),
                create_text_display('cake'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_3:x}.{0:x}'
                ),
            ),
            create_section(
                create_text_display(f'### {message_4.url}'),
                create_text_display('cream'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_4:x}.{0:x}'
                ),
            ),
            create_section(
                create_text_display(f'### {message_5.url}'),
                create_text_display('shrimp'),
                thumbnail = create_button(
                    'View',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_5:x}.{0:x}'
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    custom_id = 'automation_reaction_role.listing.decrement.disabled',
                    emoji = EMOJI_PAGE_DECREMENT,
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    custom_id = f'automation_reaction_role.listing.{1:x}',
                    emoji = EMOJI_PAGE_INCREMENT,
                    enabled = True,
                ),
            ),
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_listing_components(guild, automation_reaction_role_entries, listing_page_index):
    """
    Tests whether ``build_automation_reaction_role_listing_components`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The local guild.
    
    automation_reaction_role_entries : ``None | list<AutomationReactionRoleEntry>``
        Auto react role entries.
    
    listing_page_index : `int`
        The current listing page index.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_automation_reaction_role_listing_components(guild, automation_reaction_role_entries, listing_page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
