__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from functools import partial as partial_func

from hata import Color, DiscordException, ERROR_CODES, parse_rdelta, datetime_to_id, Emoji, Permission
from hata.ext.slash import abort

from ..bots import FEATURE_CLIENTS


ADMINISTRATION_COLOR = Color.from_rgb(148, 0, 211)


EMOJI__REIMU_HAMMER = Emoji.precreate(690550890045898812)

def match_message_author(user, message):
    return (message.author is user)

@FEATURE_CLIENTS.interactions(
    is_global = True,
    show_for_invoking_user_only = True,
    integration_context_types = ['guild'],
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def clear(client, event,
    limit: ('int', 'How much message?'),
    before: ('str', 'Till when?') = None,
    after: ('str', 'Since when?') = None,
    where: ('channel_group_guild_messageable', 'Where?') = None,
    whos: ('user', 'Who\'s message?') = None,
    reason: ('str', 'Will show up in the guild\'s audit logs.') = None,
):
    """Yeets messages."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to do this.')
    
    if where is None:
        channel = event.channel
    else:
        channel = where
    
    if limit < 1:
        abort('`limit` cannot be non-positive.')
    
    if not event.user_permissions.administrator:
        abort('You must have administrator permission to use this command.')
    
    client_permissions = channel.cached_permissions_for(client)
    if (not client_permissions.manage_messages) or (not client_permissions.read_message_history):
        abort('I must have manage messages and read message history in the channel to do it.')
    
    if (before is None) or (not before):
        before = event.id
    
    else:
        delta = parse_rdelta(before)
        if delta is None:
            abort('`before` could not be parsed.')
        
        before = datetime_to_id(DateTime.now(TimeZone.utc) - delta)
    
    if (after is None) or (not after):
        after = 0
    else:
        delta = parse_rdelta(after)
        if delta is None:
            abort('`before` could not be parsed.')
        
        after = datetime_to_id(DateTime.now(TimeZone.utc) - delta)
    
    yield 'Yeeting messages began'
    
    if whos is None:
        filter = None
    else:
        filter = partial_func(match_message_author, whos)
    
    if (reason is not None) and (not reason):
        reason = None
    
    try:
        await client.multi_client_message_delete_sequence(
            channel, after = after, before = before, limit = limit, filter = filter, reason = reason
        )
    except DiscordException as err:
        if err.code not in (
            ERROR_CODES.unknown_channel,
        ):
            raise


@FEATURE_CLIENTS.interactions(
    is_global = True,
    show_for_invoking_user_only = True,
    integration_context_types = ['guild'],
    required_permissions = Permission().update_by_keys(create_instant_invite = True),
)
async def invite_create(client, event,
    permanent: ('bool', 'Create permanent?') = False,
):
    """I create an invite for you!"""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if not event.user_permissions.create_instant_invite:
        abort('You must have `create instant invite` permission to invoke this command.')
    
    if not guild.cached_permissions_for(client).create_instant_invite:
        abort('I must have `create instant invite` permission invite to execute this command.')
    
    yield
    
    if permanent:
        invite = await client.invite_get_vanity(guild)
        if invite is None:
            max_age = 0
            max_uses = 0
    else:
        invite = None
        max_age = 21600
        max_uses = 1
    
    if invite is None:
        yield
        invite = await client.invite_create_preferred(guild, max_age = max_age, max_uses = max_uses)
    
    if invite is None:
        content = '**Error**\nI do not have enough permission to create invite from the guild\'s preferred channel.'
    else:
        content = invite.url
    
    yield content

'''
def bans_pagination_check(event):
    guild = event.message.guild
    if guild is None:
        return False
    
    if guild.permissions_for(event.user).ban_users:
        return True
    
    return False



@FEATURE_CLIENTS.interactions(
    is_global = True,
    integration_context_types = ['guild'],
    required_permissions = Permission().update_by_keys(ban_users = True),
)

async def bans(client, event):
    """Lists the guild's bans."""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if not event.user_permissions.ban_users:
        abort('You must have `ban users` permission to invoke this command.')
    
    if not guild.cached_permissions_for(client).ban_users:
        abort('I must have `ban users` permission invite to execute this command.')
    
    yield
    
    ban_data = await client.guild_ban_get_all(guild)
    
    embeds = []
    main_text = f'Guild bans for {guild.name} {guild.id}:'
    limit = len(ban_data)
    if limit:
        index = 0
        
        while True:
            field_count = 0
            embed_length = len(main_text)
            embed = Embed(main_text)
            embeds.append(embed)
            
            while True:
                user, reason = ban_data[index]
                if reason is None:
                    reason = 'Not defined.'
                name = f'{user:f} {user.id}'
                embed_length += len(reason) + len(name)
                if embed_length > 5900:
                    break
                embed.add_field(name, reason)
                field_count += 1
                if field_count == 25:
                    break
                index += 1
                if index == limit:
                    break
            if index == limit:
                break
    else:
        embed = Embed(main_text, '*none*')
        embeds.append(embed)
    
    index = 0
    field_count = 0
    embed_ln = len(embeds)
    result = []
    while True:
        embed = embeds[index]
        index += 1
        embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count + 1}-{field_count + len(embed.fields)}/{limit}')
        field_count += len(embed.fields)
        
        result.append(embed)
        
        if index == embed_ln:
            break
    
    await Pagination(client, event, result, check = bans_pagination_check)
'''

def check_channel_invites_pagination_permissions(event):
    permissions = event.message.channel.permissions_for(event.user)
    if not permissions.manage_channels:
        return False
    
    if not permissions.create_instant_invite:
        return False
    
    return True

def check_guild_invites_pagination_permissions(event):
    guild = event.message.guild
    if guild is None:
        return False
    
    permissions = guild.permissions_for(event.user)
    if not permissions.manage_guild:
        return False
    
    if not permissions.create_instant_invite:
        return False
    
    return True

'''
PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

@FEATURE_CLIENTS.interactions(
    is_global = True,
    integration_context_types = ['guild'],
    required_permissions = Permission().update_by_keys(create_instant_invite = True),
)
async def invites_(client, event,
    channel: ('channel', 'Which channel\'s invites do you wanna check?') = None,
):
    """Shows up the guild's or the selected channel's invites."""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if (channel is not None) and (not channel.is_in_group_invitable()):
        abort('Cannot create invite to the selected channel.')
    
    if not event.channel.cached_permissions_for(client) & PERMISSION_MASK_MESSAGING:
        abort('I must have `send messages` permission to invoke this command correctly.')
    
    if channel is None:
        permissions = event.user_permissions
        if (not permissions.create_instant_invite) or (not permissions.manage_guild):
            abort('You must have `create instant invite` and `manage guild` permission to invoke this command.')
        
        permissions = guild.cached_permissions_for(client)
        if (not permissions.create_instant_invite) or (not permissions.manage_guild):
            abort('I must have `create instant invite` and `manage guild` to invite to execute this command.')
    
    else:
        permissions = event.user_permissions
        if (not permissions.create_instant_invite) or (not permissions.manage_channels):
            abort('You must have `create instant invite` and `manage channel` permission to invoke this command.')
        
        permissions = channel.cached_permissions_for(client)
        if (not permissions.create_instant_invite) or (not permissions.manage_channels):
            abort('I must have `create instant invite` and `manage channel` to invite to execute this command.')
    
    yield
    
    if channel is None:
        coroutine = client.invite_get_all_guild(guild)
    else:
        coroutine = client.invite_get_all_guild(guild)
    invites = await coroutine
    
    pages = [Embed(description = chunk) for chunk in pchunkify(invites, write_parents = False)]
    
    if channel is None:
        check = check_guild_invites_pagination_permissions
    else:
        check = check_channel_invites_pagination_permissions
    
    await Pagination(client, event, pages, timeout = 120.0, check = check)

'''
