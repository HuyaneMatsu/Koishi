import vampytest
from hata import Channel, ChannelType, Client, Guild, GuildProfile, Role, Message, Permission
from scarletio import Task, get_event_loop

from ....bot_utils.models import DB_ENGINE

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..helpers import get_automation_reaction_role_entry_listing_and_sync_page


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_automation_reaction_role_entry_listing_and_sync_page__correct_page():
    """
    Tests whether ``get_automation_reaction_role_entry_listing_and_sync_page`` works as intended.
    
    Case: correct page.
    """
    message_id_0 = 202510040020
    channel_id_0 = 202510040021
    guild_id = 202510040022
    client_id_0 = 202510040023
    entry_id_0 = 888
    message_get_call_count = 0
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id,
    )
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
    )
    
    role_default = Role.precreate(
        guild_id,
        guild_id = guild_id,
        permissions = Permission(8),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        roles = [role_default],
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    automation_reaction_role_entry_0.message_cached = False
    
    automation_reaction_role_by_guild_id = {
        guild_id : [
            automation_reaction_role_entry_0,
        ],
    }
    automation_reaction_role_by_message_id = {
        message_id_0 : automation_reaction_role_entry_0,
    }
    
    
    mocked = vampytest.mock_globals(
        get_automation_reaction_role_entry_listing_and_sync_page,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        recursion = 3,
    )
    
    async def message_get_patched(self, message, *, force_update = False):
        nonlocal message_get_call_count
        message_get_call_count += 1
    
    
    client_0 = Client(
        f'token_{client_id_0:x}',
        client_id = client_id_0
    )
    message_get_original = Client.message_get
    
    try:
        Client.message_get = message_get_patched
        
        guild.clients.append(client_0)
        client_0.guild_profiles[guild_id] = GuildProfile()
        
        task = Task(get_event_loop(), mocked(guild_id, 0))
        task.apply_timeout(0.01)
        output = await task
    
    finally:
        Client.message_get = message_get_original
        client_0._delete()
        client_0 = None
    
    vampytest.assert_instance(output, list, nullable = True)
    vampytest.assert_eq(
        output,
        [
            automation_reaction_role_entry_0,
        ],
    )
    
    vampytest.assert_true(automation_reaction_role_entry_0.message_cached)
    
    vampytest.assert_eq(message_get_call_count, 1)


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_automation_reaction_role_entry_listing_and_sync_page__page_out_of_range():
    """
    Tests whether ``get_automation_reaction_role_entry_listing_and_sync_page`` works as intended.
    
    Case: page out of range.
    """
    message_id_0 = 202510040030
    channel_id_0 = 202510040031
    guild_id = 202510040032
    client_id_0 = 202510040033
    entry_id_0 = 888
    message_get_call_count = 0
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id_0,
        guild_id = guild_id,
    )
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
    )
    
    role_default = Role.precreate(
        guild_id,
        guild_id = guild_id,
        permissions = Permission(8),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        roles = [role_default],
    )
    
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(
        message_0,
    )
    automation_reaction_role_entry_0.entry_id = entry_id_0
    automation_reaction_role_entry_0.message_cached = False
    
    automation_reaction_role_by_guild_id = {
        guild_id : [
            automation_reaction_role_entry_0,
        ],
    }
    automation_reaction_role_by_message_id = {
        message_id_0 : automation_reaction_role_entry_0,
    }
    
    
    mocked = vampytest.mock_globals(
        get_automation_reaction_role_entry_listing_and_sync_page,
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID = automation_reaction_role_by_guild_id,
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID = automation_reaction_role_by_message_id,
        recursion = 3,
    )
    
    async def message_get_patched(self, message, *, force_update = False):
        nonlocal message_get_call_count
        message_get_call_count += 1
    
    
    client_0 = Client(
        f'token_{client_id_0:x}',
        client_id = client_id_0
    )
    message_get_original = Client.message_get
    
    try:
        Client.message_get = message_get_patched
        
        guild.clients.append(client_0)
        client_0.guild_profiles[guild_id] = GuildProfile()
        
        task = Task(get_event_loop(), mocked(guild_id, 1))
        task.apply_timeout(0.01)
        output = await task
    
    finally:
        Client.message_get = message_get_original
        client_0._delete()
        client_0 = None
    
    vampytest.assert_instance(output, list, nullable = True)
    vampytest.assert_eq(
        output,
        [
            automation_reaction_role_entry_0,
        ],
    )
    
    vampytest.assert_false(automation_reaction_role_entry_0.message_cached)
    
    vampytest.assert_eq(message_get_call_count, 0)
