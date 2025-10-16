import vampytest
from hata import BUILTIN_EMOJIS, GuildProfile, ReactionAddEvent, ReactionDeleteEvent, Role, Message, User

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..events import get_user_new_role_ids




def _iter_options():
    # The reaction adds and removes roles (reaction add evnet)
    guild_id = 202510010170
    channel_id = 202510010171
    message_id = 202510010172
    user_id = 202510010173
    entry_id = 777
    
    role_id_0 = 202510010174
    role_id_1 = 202510010175
    role_id_2 = 202510010176
    role_id_3 = 202510010177
    role_id_4 = 202510010178
    
    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [role_id_4, role_id_2, role_id_3],
    )
    
    event = ReactionAddEvent(
        message,
        emoji,
        user,
    )
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        (role_id_0, role_id_1),
        (role_id_2, role_id_3),
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        automation_reaction_role_item,
    ]
    
    yield (
        event,
        True,
        {
            message_id : automation_reaction_role_entry,
        },
        [],
        (
            {
                role_id_4,
                role_id_2,
                role_id_3,
            },
            [
                role_id_0,
                role_id_1,
            ],
            [
                role_id_2,
                role_id_3,
            ]
        ),
    )
    
    # The reaction adds and removes roles (reaction remove evnet)
    guild_id = 202510010180
    channel_id = 202510010181
    message_id = 202510010182
    user_id = 202510010183
    entry_id = 777
    
    role_id_0 = 202510010184
    role_id_1 = 202510010185
    role_id_2 = 202510010186
    role_id_3 = 202510010187
    role_id_4 = 202510010188
    
    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [role_id_4, role_id_2, role_id_3],
    )
    
    event = ReactionDeleteEvent(
        message,
        emoji,
        user,
    )
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        (role_id_2, role_id_3),
        (role_id_0, role_id_1),
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        automation_reaction_role_item,
    ]
    
    yield (
        event,
        False,
        {
            message_id : automation_reaction_role_entry,
        },
        [],
        (
            {
                role_id_4,
                role_id_2,
                role_id_3,
            },
            [
                role_id_0,
                role_id_1,
            ],
            [
                role_id_2,
                role_id_3,
            ],
        )
    )
    
    # reaction add event, but no roles change.
    guild_id = 202510010190
    channel_id = 202510010191
    message_id = 202510010192
    user_id = 202510010193
    entry_id = 777
    
    role_id_0 = 202510010194
    role_id_1 = 202510010195
    role_id_2 = 202510010196
    role_id_3 = 202510010197
    role_id_4 = 202510010198
    
    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [role_id_4, role_id_0, role_id_1],
    )
    
    event = ReactionAddEvent(
        message,
        emoji,
        user,
    )
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        (role_id_0, role_id_1),
        (role_id_2, role_id_3),
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        automation_reaction_role_item,
    ]
    
    yield (
        event,
        True,
        {
            message_id : automation_reaction_role_entry,
        },
        [],
        None,
    )
    
    # reaction add event, but no roles assigned
    guild_id = 202510010200
    channel_id = 202510010201
    message_id = 202510010202
    user_id = 202510010203
    entry_id = 777
    
    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [],
    )
    
    event = ReactionAddEvent(
        message,
        emoji,
        user,
    )
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        None,
        None,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        automation_reaction_role_item,
    ]
    
    yield (
        event,
        True,
        {
            message_id : automation_reaction_role_entry,
        },
        [],
        None,
    )
    
    # reaction add event, but no emoji is hit.
    guild_id = 202510010210
    channel_id = 202510010211
    message_id = 202510010212
    user_id = 202510010213
    entry_id = 777
    
    role_id_0 = 202510010124
    role_id_1 = 202510010125
    role_id_2 = 202510010126
    role_id_3 = 202510010127
    
    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    
    emoji_used = BUILTIN_EMOJIS['green_heart']
    emoji_used_id = emoji_used.id
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [],
    )
    
    event = ReactionAddEvent(
        message,
        emoji_used,
        user,
    )
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        (role_id_0, role_id_1),
        (role_id_2, role_id_3),
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.items = [
        automation_reaction_role_item,
    ]
    
    yield (
        event,
        True,
        {
            message_id : automation_reaction_role_entry,
        },
        [],
        None,
    )
    
    # reaction add event, no message hit
    guild_id = 202510010230
    channel_id = 202510010231
    message_id = 202510010232
    user_id = 202510010233
    
    emoji = BUILTIN_EMOJIS['heart']
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    user = User.precreate(
        user_id,
    )
    user.guild_profiles[guild_id] = GuildProfile(
        role_ids = [],
    )
    
    event = ReactionAddEvent(
        message,
        emoji,
        user,
    )
    
    yield (
        event,
        True,
        {},
        [],
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_new_role_ids(event, addition, automation_reaction_role_by_message_id, entity_cache):
    """
    Gets the user's new role ids.
    
    Parameters
    ----------
    event : ``ReactionAddEvent``
        Received event.
    
    addition : `bool`
        Whether the add role should be added and remove roles should be removed, or the other way around.
    
    automation_reaction_role_by_message_id : ``dict<int, AutomationReactionRoleEntry>``
        Auto react role entries variable to patch the cache.
    
    entity_cache : `list<object>`
        Additional entities to keep in cache.
    
    Returns
    -------
    output : `None | (set<int>, None | list<int>, None | list<int>)`
    """
    mocked = vampytest.mock_globals(
        get_user_new_role_ids,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
    )
    
    output = mocked(event, addition)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
