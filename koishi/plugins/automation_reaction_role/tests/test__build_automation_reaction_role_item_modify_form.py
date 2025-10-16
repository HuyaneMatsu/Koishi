import vampytest
from hata import (
    BUILTIN_EMOJIS, EntitySelectDefaultValue, EntitySelectDefaultValueType, GuildProfile, InteractionForm, Role,
    Message, User, create_label, create_role_select, create_text_display
)

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..custom_ids import CUSTOM_ID_ADD_ROLES, CUSTOM_ID_REMOVE_ROLES
from ..component_builders import build_automation_reaction_role_item_modify_form


def _iter_options():
    guild_id = 202509280200
    user_id = 202510010201
    channel_id_0 = 202509280202
    channel_id_1 = 202509280203
    message_id_0 = 202509280204
    message_id_1 = 202509280205
    
    role_id_0 = 202509280206
    role_id_1 = 202509280207
    role_id_2 = 202509280208
    role_id_3 = 202509280209
    
    entry_id_0 = 6
    entry_id_1 = 7
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['green_heart']
    
    emoji_id_0 = emoji_0.id
    emoji_id_1 = emoji_1.id
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile()
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id,
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
        name = 'satori',
    )
    
    role_2 = Role.precreate(
        role_id_2,
        guild_id = guild_id,
        name = 'okuu',
    )
    
    role_3 = Role.precreate(
        role_id_3,
        guild_id = guild_id,
        name = 'orin',
    )
    
    automation_reaction_role_item_0 = AutomationReactionRoleItem(
        emoji_id_0,
        None,
        None,
    )
    
    automation_reaction_role_item_1 = AutomationReactionRoleItem(
        emoji_id_1,
        (role_id_0, role_id_1),
        (role_id_2, role_id_3),
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    automation_reaction_role_entry_0.items = [
        automation_reaction_role_item_0,
    ]
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message_1,
    )
    automation_reaction_role_entry_1.entry_id = entry_id_1
    automation_reaction_role_entry_1.items = [
        automation_reaction_role_item_1,
    ]
    
    
    yield (
        user,
        1,
        automation_reaction_role_entry_0,
        1,
        automation_reaction_role_item_0,
        [],
        InteractionForm(
            'Modify emoji',
            [
                create_text_display(
                    f'{emoji_0} {emoji_0.name}'
                ),
                create_label(
                    'Added roles upon reacting',
                    component = create_role_select(
                        custom_id = CUSTOM_ID_ADD_ROLES,
                        max_values = 25,
                        min_values = 0,
                    ),
                ),
                create_label(
                    
                    'Removed roles upon reacting',
                    component = create_role_select(
                        custom_id = CUSTOM_ID_REMOVE_ROLES,
                        max_values = 25,
                        min_values = 0,
                    ),
                ),
            ],
            custom_id = f'automation_reaction_role.item_modify.{1:x}.{message_id_0:x}.{1:x}.{emoji_id_0:x}'
        ),
    )
    
    
    yield (
        user,
        0,
        automation_reaction_role_entry_1,
        0,
        automation_reaction_role_item_1,
        [
            role_0,
            role_1,
            role_2,
            role_3,
        ],
        InteractionForm(
            'Modify emoji',
            [
                create_text_display(
                    f'{emoji_1} {emoji_1.name}'
                ),
                create_label(
                    'Added roles upon reacting',
                    component = create_role_select(
                        custom_id = CUSTOM_ID_ADD_ROLES,
                        default_values = [
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id_0),
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id_1),
                        ],
                        max_values = 25,
                        min_values = 0,
                    ),
                ),
                create_label(
                    'Removed roles upon reacting',
                    component = create_role_select(
                        custom_id = CUSTOM_ID_REMOVE_ROLES,
                        default_values = [
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id_2),
                            EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id_3),
                        ],
                        max_values = 25,
                        min_values = 0,
                    ),
                ),
            ],
            custom_id = f'automation_reaction_role.item_modify.{0:x}.{message_id_1:x}.{0:x}.{emoji_id_1:x}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_item_modify_form(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index, item, entity_cache
):
    """
    Tests whether ``build_automation_reaction_role_item_modify_form`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    overview_page_index : `int`
        The overview's page index to redirect back to.
    
    item : ``AutoreactRoleItem``
        The item to prompt modification form for.
    
    entity_cache : `list<object>`
        Additional objects to keep cached.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_automation_reaction_role_item_modify_form(
        user, listing_page_index, automation_reaction_role_entry, overview_page_index, item
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
