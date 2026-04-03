import vampytest
from hata import (
    BUILTIN_EMOJIS, GuildProfile, InteractionForm, Message, StringSelectOption, User, create_label, create_string_select
)

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..component_builders import build_automation_reaction_role_item_delete_form
from ..custom_ids import CUSTOM_ID_EMOJI


def _iter_options():
    guild_id = 202510040040
    user_id = 202510040041
    channel_id_0 = 202510040042
    channel_id_1 = 202510040043
    message_id_0 = 202510040044
    message_id_1 = 202510040045
    entry_id_0 = 6
    entry_id_1 = 7
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['flan']
    emoji_2 = BUILTIN_EMOJIS['green_heart']
    
    emoji_id_0 = emoji_0.id
    emoji_id_1 = emoji_1.id
    emoji_id_2 = emoji_2.id
    
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
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(
        message_1,
    )
    automation_reaction_role_entry_1.items = [
        AutomationReactionRoleItem(emoji_id_0, None, None),
        AutomationReactionRoleItem(emoji_id_1, None, None),
        AutomationReactionRoleItem(emoji_id_2, None, None),
    ]
    automation_reaction_role_entry_1.entry_id = entry_id_1
    
    
    yield (
        user,
        1,
        automation_reaction_role_entry_0,
        2,
        [],
        InteractionForm(
            'Delete emoji',
            [
                create_label(
                    'Emoji',
                    component = create_string_select(
                        [
                            StringSelectOption(
                                '0',
                                'none',
                                default = True,
                            ),
                        ],
                        custom_id = CUSTOM_ID_EMOJI,
                    ),
                ),
            ],
            custom_id = f'automation_reaction_role.item_delete.{1:x}.{message_id_0:x}.{2:x}',
        ),
    )
    
    yield (
        user,
        1,
        automation_reaction_role_entry_1,
        1,
        [],
        InteractionForm(
            'Delete emoji',
            [
                create_label(
                    'Emoji',
                    component = create_string_select(
                        [
                            StringSelectOption(
                                format(emoji_id_0, 'x'),
                                emoji_0.name,
                                emoji_0,
                                default = False,
                            ),
                            StringSelectOption(
                                format(emoji_id_1, 'x'),
                                emoji_1.name,
                                emoji_1,
                                default = False,
                            ),
                            StringSelectOption(
                                format(emoji_id_2, 'x'),
                                emoji_2.name,
                                emoji_2,
                                default = False,
                            ),
                        ],
                        custom_id = CUSTOM_ID_EMOJI,
                    ),
                ),
            ],
            custom_id = f'automation_reaction_role.item_delete.{1:x}.{message_id_1:x}.{1:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_item_delete_form(
    user, listing_page_index, automation_reaction_role_entry, overview_page_index, entity_cache
):
    """
    Tests whether ``build_automation_reaction_role_item_delete_form`` works as intended.
    
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
    
    entity_cache : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_automation_reaction_role_item_delete_form(
        user, listing_page_index, automation_reaction_role_entry, overview_page_index
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
