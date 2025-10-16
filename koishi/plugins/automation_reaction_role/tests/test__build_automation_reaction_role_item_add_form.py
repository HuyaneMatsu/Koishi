import vampytest
from hata import (
    BUILTIN_EMOJIS, Emoji, GuildProfile, InteractionForm, Message, Reaction, ReactionMapping, ReactionMappingLine,
    StringSelectOption, User, create_label, create_role_select, create_string_select
)

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..component_builders import build_automation_reaction_role_item_add_form
from ..custom_ids import CUSTOM_ID_ADD_ROLES, CUSTOM_ID_EMOJI, CUSTOM_ID_REMOVE_ROLES


def _iter_options():
    guild_id_0 = 202509290000
    guild_id_1 = 202509290007
    user_id = 202510010005
    channel_id_0 = 202509290001
    channel_id_1 = 202509290002
    channel_id_2 = 202509290003
    message_id_0 = 202509290004
    message_id_1 = 202509290005
    message_id_2 = 202509290006
    
    entry_id_0 = 6
    entry_id_1 = 7
    entry_id_2 = 7
    
    user = User.precreate(user_id,)
    user.guild_profiles[guild_id_0] = GuildProfile()
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['green_heart']
    emoji_2 = BUILTIN_EMOJIS['apple']
    
    emoji_id_0 = emoji_0.id
    emoji_id_1 = emoji_1.id
    emoji_id_2 = emoji_2.id
    
    emoji_id_3 = 202509290008
    emoji_id_4 = 202509290009
    emoji_id_5 = 202509290010
    
    emoji_3 = Emoji.precreate(
        emoji_id_3,
        guild_id = guild_id_0,
        available = True,
        name = 'pudding',
    )
    
    emoji_4 = Emoji.precreate(
        emoji_id_4,
        guild_id = guild_id_0,
        available = False,
        name = 'cream',
    )
    
    emoji_5 = Emoji.precreate(
        emoji_id_5,
        guild_id = guild_id_1,
        available = True,
        name = 'cake',
    )
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_1,
        guild_id = guild_id_0,
    )
    
    message_1 = Message.precreate(
        message_id_1,
        channel_id = channel_id_1,
        guild_id = guild_id_0,
        reactions = ReactionMapping(
            lines = [
                (Reaction(emoji_0), ReactionMappingLine(count = 5)),
                (Reaction(emoji_1), ReactionMappingLine(count = 5)),
                (Reaction(emoji_2), ReactionMappingLine(count = 5)),
            ],
        )
    )
    
    message_2 = Message.precreate(
        message_id_2,
        channel_id = channel_id_2,
        guild_id = guild_id_0,
        reactions = ReactionMapping(
            lines = [
                (Reaction(emoji_3), ReactionMappingLine(count = 5)),
                (Reaction(emoji_4), ReactionMappingLine(count = 5)),
                (Reaction(emoji_5), ReactionMappingLine(count = 5)),
            ],
        )
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
    
    
    yield (
        user,
        1,
        automation_reaction_role_entry_0,
        [],
        InteractionForm(
            'Add new emoji',
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
            custom_id = f'automation_reaction_role.item_add.{1:x}.{message_id_0:x}',
        ),
    )
    
    yield (
        user,
        1,
        automation_reaction_role_entry_1,
        [],
        InteractionForm(
            'Add new emoji',
            [
                create_label(
                    'Emoji',
                    component = create_string_select(
                        [
                            StringSelectOption(
                                format(emoji_id_0, 'x'),
                                emoji_0.name,
                                emoji_0,
                                default = True,
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
            custom_id = f'automation_reaction_role.item_add.{1:x}.{message_id_1:x}',
        ),
    )
    
    yield (
        user,
        1,
        automation_reaction_role_entry_2,
        [emoji_3, emoji_4, emoji_5],
        InteractionForm(
            'Add new emoji',
            [
                create_label(
                    'Emoji',
                    component = create_string_select(
                        [
                            StringSelectOption(
                                format(emoji_id_3, 'x'),
                                emoji_3.name,
                                emoji_3,
                                default = True,
                            ),
                            StringSelectOption(
                                format(emoji_id_4, 'x'),
                                emoji_4.name,
                                None,
                                default = False,
                            ),
                            StringSelectOption(
                                format(emoji_id_5, 'x'),
                                emoji_5.name,
                                None,
                                default = False,
                            ),
                        ],
                        custom_id = CUSTOM_ID_EMOJI,
                    ),
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
            custom_id = f'automation_reaction_role.item_add.{1:x}.{message_id_2:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_item_add_form(user, listing_page_index, automation_reaction_role_entry, entity_cache):
    """
    Tests whether ``build_automation_reaction_role_item_add_form`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user from who's view are building.
    
    listing_page_index : `int`
        The current listing page index.
    
    automation_reaction_role_entry : ``AutoreactRoleEntry``
        The selected auto react role entry.
    
    entity_cache : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_automation_reaction_role_item_add_form(user, listing_page_index, automation_reaction_role_entry)
    vampytest.assert_instance(output, InteractionForm)
    return output
