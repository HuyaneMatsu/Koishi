import vampytest
from hata import (
    BUILTIN_EMOJIS, ButtonStyle, Component, GuildProfile, Message, Role, User, create_button, create_row,
    create_section, create_separator, create_text_display
)
from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..component_builders import build_automation_reaction_role_entry_overview_components
from ..constants import EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT


def _iter_options():
    guild_id = 202509280020
    user_id = 202510010004
    channel_id_0 = 202509280021
    channel_id_1 = 202509280024
    message_id_0 = 202509280022
    message_id_1 = 202509280023
    entry_id_0 = 6
    entry_id_1 = 7
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['flan']
    emoji_2 = BUILTIN_EMOJIS['green_heart']
    emoji_3 = BUILTIN_EMOJIS['apple']
    emoji_4 = BUILTIN_EMOJIS['mushroom']
    emoji_5 = BUILTIN_EMOJIS['potato']
    emoji_6 = BUILTIN_EMOJIS['green_apple']
    
    emoji_id_0 = emoji_0.id
    emoji_id_1 = emoji_1.id
    emoji_id_2 = emoji_2.id
    emoji_id_3 = emoji_3.id
    emoji_id_4 = emoji_4.id
    emoji_id_5 = emoji_5.id
    emoji_id_6 = emoji_6.id
    
    role_id_0 = 202509280025
    role_id_1 = 202509280026
    role_id_2 = 202509280027
    role_id_3 = 202509280028
    role_id_4 = 202509280029
    role_id_5 = 202509280030
    role_id_6 = 202509280031
    
    user = User.precreate(user_id,)
    user.guild_profiles[guild_id] = GuildProfile()
    
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
    )
    
    role_0 = Role.precreate(
        role_id_0,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_1 = Role.precreate(
        role_id_1,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_2 = Role.precreate(
        role_id_2,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_3 = Role.precreate(
        role_id_3,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_4 = Role.precreate(
        role_id_4,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_5 = Role.precreate(
        role_id_5,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    role_6 = Role.precreate(
        role_id_6,
        guild_id = guild_id,
        name = 'koishi',
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message_1,
    )
    automation_reaction_role_entry_1.items = [
        AutomationReactionRoleItem(emoji_id_0, (role_id_0,), None),
        AutomationReactionRoleItem(emoji_id_1, (role_id_1, role_id_2), None),
        AutomationReactionRoleItem(emoji_id_2, None, (role_id_3,)),
        AutomationReactionRoleItem(emoji_id_3, None, (role_id_4, role_id_5)),
        AutomationReactionRoleItem(emoji_id_4, (role_id_0,), (role_id_3,)),
        AutomationReactionRoleItem(emoji_id_5, None, None),
        AutomationReactionRoleItem(emoji_id_6, None, None),
    ]
    automation_reaction_role_entry_1.entry_id = entry_id_1
    
    
    yield (
        user,
        1,
        automation_reaction_role_entry_0,
        0,
        [],
        [
            create_text_display(f'### Auto react role {automation_reaction_role_entry_0.message.url}'),
            create_text_display('shrimp'),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    custom_id = 'automation_reaction_role.view.decrement.disabled',
                    emoji = EMOJI_PAGE_DECREMENT,
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    custom_id = 'automation_reaction_role.view.increment.disabled',
                    emoji = EMOJI_PAGE_INCREMENT,
                    enabled = False,
                ),
                create_button(
                    'Back to listing',
                    custom_id =  f'automation_reaction_role.listing.{1:x}'
                ),
                create_button(
                    'Delete',
                    custom_id = f'automation_reaction_role.delete.{1:x}.{message_id_0:x}',
                    style = ButtonStyle.red,
                ),
            ),
            create_row(
                create_button(
                    'Add new',
                    custom_id = f'automation_reaction_role.item_add.{1:x}.{message_id_0:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Delete one',
                    custom_id = f'automation_reaction_role.item_delete.{1:x}.{message_id_0:x}.{0:x}',
                    enabled = False,
                ),
                # create_button(
                #     'Sync',
                #     custom_id = f'automation_reaction_role.sync.{1:x}.{message_id_0:x}',
                # ),
            ),
        ],
    )
    
    yield (
        user,
        0,
        automation_reaction_role_entry_1,
        0,
        [
            role_0,
            role_1,
            role_2,
            role_3,
            role_4,
            role_5,
        ],
        [
            create_text_display(f'### Auto react role {automation_reaction_role_entry_1.message.url}'),
            create_separator(),
            create_section(
                create_text_display(f'{emoji_0} {emoji_0.name}'),
                create_text_display(
                    f'Add roles:\n'
                    f'- {role_0.mention}'
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_0:x}',
                ),
            ),
            create_section(
                create_text_display(f'{emoji_1} {emoji_1.name}'),
                create_text_display(
                    f'Add roles:\n'
                    f'- {role_1.mention}\n'
                    f'- {role_2.mention}'
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_1:x}',
                ),
            ),
            create_section(
                create_text_display(f'{emoji_2} {emoji_2.name}'),
                create_text_display(
                    f'Remove roles:\n'
                    f'- {role_3.mention}'
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_2:x}',
                ),
            ),
            create_section(
                create_text_display(f'{emoji_3} {emoji_3.name}'),
                create_text_display(
                    f'Remove roles:\n'
                    f'- {role_4.mention}\n'
                    f'- {role_5.mention}'
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_3:x}',
                ),
            ),
            create_section(
                create_text_display(f'{emoji_4} {emoji_4.name}'),
                create_text_display(
                    f'Add roles:\n'
                    f'- {role_0.mention}\n'
                    f'Remove roles:\n'
                    f'- {role_3.mention}'
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_4:x}',
                ),
            ),
            create_section(
                create_text_display(f'{emoji_5} {emoji_5.name}'),
                create_text_display(
                    f'none',
                ),
                thumbnail = create_button(
                    'Modify',
                    custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_5:x}',
                ),
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 0',
                    custom_id = 'automation_reaction_role.view.decrement.disabled',
                    emoji = EMOJI_PAGE_DECREMENT,
                    enabled = False,
                ),
                create_button(
                    'Page 2',
                    custom_id = f'automation_reaction_role.view.{0:x}.{message_id_1:x}.{1:x}',
                    emoji = EMOJI_PAGE_INCREMENT,
                ),
                create_button(
                    'Back to listing',
                    custom_id =  f'automation_reaction_role.listing.{0:x}'
                ),
                create_button(
                    'Delete',
                    custom_id = f'automation_reaction_role.delete.{0:x}.{message_id_1:x}',
                    style = ButtonStyle.red,
                ),
            ),
            create_row(
                create_button(
                    'Add new',
                    custom_id = f'automation_reaction_role.item_add.{0:x}.{message_id_1:x}',
                    enabled = True,
                    style = ButtonStyle.green,
                ),
                create_button(
                    'Delete one',
                    custom_id = f'automation_reaction_role.item_delete.{0:x}.{message_id_1:x}.{0:x}',
                    enabled = True,
                ),
                # create_button(
                #     'Sync',
                #     custom_id = f'automation_reaction_role.sync.{0:x}.{message_id_1:x}',
                # ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_entry_overview_components(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index, entity_cache
):
    """
    Tests whether ``build_automation_reaction_role_entry_overview_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    overview_page_index : `int`
        The current overview page index.
    
    entity_cache  `list<object>`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_automation_reaction_role_entry_overview_components(
        user, listing_page_index, automation_reaction_role_entry, overview_page_index
    )
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
