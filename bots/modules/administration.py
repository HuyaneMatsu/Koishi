# -*- coding: utf-8 -*-
from datetime import datetime
from functools import partial as partial_func

from hata import Color, Embed, DiscordException, BUILTIN_EMOJIS, ERROR_CODES, parse_emoji, Client, ChannelText, \
    parse_rdelta, time_to_id, ChannelCategory
from hata.ext.commands import Pagination, wait_for_reaction
from hata.ext.prettyprint import pchunkify


ADMINISTRATION_COLOR = Color.from_rgb(148, 0, 211)

SLASH_CLIENT: Client

def match_message_author(user, message):
    return (message.author is user)

@SLASH_CLIENT.interactions(is_global=True)
async def clear(client, event,
        limit  : ('int'     , 'How much message?'                       )        ,
        before : ('str'     , 'Till when?'                               ) = None ,
        after  : ('str'     , 'Since when?'                              ) = None ,
        where  : ('channel' , 'Where?'                                   ) = None ,
        whos   : ('user'    , 'Who\'s message?'                          ) = None ,
        reason : ('str'     , 'Will show up in the guild\'s audit logs.' ) = None ,
            ):
    """Yeets messages."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    if where is None:
        channel = event.channel
    else:
        if not isinstance(where, ChannelText):
            yield Embed('Error', 'The channel must be a text channel.')
            return
        
        channel = where
    
    if limit < 1:
        yield Embed('Ohoho', '`limit` cannot be non-positive.')
        return
    
    if not event.user_permissions.can_administrator:
        yield Embed('Permission denied', 'You must have administrator permission to use this command.')
        return
    
    client_permissions = channel.cached_permissions_for(client)
    if (not client_permissions.can_manage_messages) or (not client_permissions.can_read_message_history):
        yield Embed('Permission denied',
            'I must have manage messages and read message history in the channel to do it.')
        return
    
    if (before is None) or (not before):
        before = event.id
    else:
        delta = parse_rdelta(before)
        if delta is None:
            yield Embed('Error', '`before` could not be parsed.')
            return
        
        before = time_to_id(datetime.now()-delta)
    
    if (after is None) or (not after):
        after = 0
    else:
        delta = parse_rdelta(after)
        if delta is None:
            yield Embed('Error', '`after` could not be parsed.')
        
        before = time_to_id(datetime.now()-delta)
    
    yield
    
    if whos is None:
        filter = None
    else:
        filter = partial_func(match_message_author, whos)
    
    if (reason is not None) and (not reason):
        reason = None
    
    await client.multi_client_message_delete_sequence(channel, after=after, before=before, limit=limit, filter=filter,
        reason=reason)

@SLASH_CLIENT.interactions(is_global=True, show_for_invoking_user_only=True)
async def invite_create(client, event,
        permanent : ('bool', 'Create permanent?') = False,
            ):
    """I create an invite for you!"""
    guild = event.guild
    if guild is None:
        yield '**Error**\nGuild only command'
        return
    
    if guild not in client.guild_profiles:
        yield '**Error**\nI must be in the guild to execute the command.'
        return
    
    if not event.user_permissions.can_create_instant_invite:
        yield '**Permission denied**\nYou must have `create instant invite` permission to invoke this command.'
        return
    
    if not guild.cached_permissions_for(client).can_create_instant_invite:
        yield '**Permission denied**\nI must have `create instant invite` permission invite to execute this command.'
        return
    
    yield
    
    if permanent:
        invite = await client.vanity_invite_get(guild)
        if invite is None:
            max_age = 0
            max_uses = 0
    else:
        invite = None
        max_age = 21600
        max_uses = 1
    
    if invite is None:
        yield
        invite = await client.invite_create_preferred(guild, max_age=max_age, max_uses=max_uses)
    
    if invite is None:
        content = '**Error**\nI do not have enough permission to create invite from the guild\'s preferred channel.'
    else:
        content = invite.url
    
    yield content

def bans_pagination_check(event):
    guild = event.guild
    if guild is None:
        return False
    
    if guild.permissions_for(event.user).can_ban_users:
        return True
    
    return False

@SLASH_CLIENT.interactions(is_global=True)
async def bans(client, event):
    """Lists the guild's bans."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command')
        return
    
    if guild not in client.guild_profiles:
        yield 'I must be in the guild to execute the command.'
        return
    
    if not event.user_permissions.can_ban_users:
        yield Embed('Permission denied',
            'You must have `ban users` permission to invoke this command.')
        return
    
    if not guild.cached_permissions_for(client).can_ban_users:
        yield Embed('Permission denied',
            'I must have `ban users` permission invite to execute this command.')
        return
    
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
                embed_length += len(reason)+len(name)
                if embed_length > 5900:
                    break
                embed.add_field(name, reason)
                field_count += 1
                if field_count == 25:
                    break
                index +=1
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
        index +=1
        embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
        field_count += len(embed.fields)
        
        result.append(embed)
        
        if index == embed_ln:
            break
    
    await Pagination(client, event.channel, result, check=bans_pagination_check)

def check_channel_invites_pagination_permissions(event):
    permissions = event.message.channel.permissions_for(event.user)
    if not permissions.can_manage_channel:
        return False
    
    if not permissions.can_create_instant_invite:
        return False
    
    return True

def check_guild_invites_pagination_permissions(event):
    guild = event.message.channel.guild
    if guild is None:
        return False
    
    permissions = guild.permissions_for(event.user)
    if not permissions.can_manage_guild:
        return False
    
    if not permissions.can_create_instant_invite:
        return False
    
    return True


@SLASH_CLIENT.interactions(is_global=True)
async def invites_(client, event,
        channel : ('channel', 'Which channel\'s invites do you wanna check?') = None,
            ):
    """Shows up the guild's or the selected channel's invites."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Error', 'I must be in the guild to execute the command.')
        return
    
    if (channel is not None) and isinstance(channel, ChannelCategory):
        yield Embed('Error', 'Category channels have no invites.')
        return
    
    if not event.channel.cached_permissions_for(client).can_send_messages:
        yield Embed('Permission denied', 'I must have `send messages` permission to invoke this command correctly.')
        return
    
    if channel is None:
        permissions = event.user_permissions
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_guild):
            yield Embed('Permission denied',
                'You must have `create instant invite` and `manage guild` permission to invoke this command.')
            return
        
        permissions = guild.cached_permissions_for(client)
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_guild):
            yield Embed('Permission denied',
                'I must have `create instant invite` and `manage guild` to invite to execute this command.')
            return
    else:
        permissions = event.user_permissions
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_channel):
            yield Embed('Permission denied',
                'You must have `create instant invite` and `manage channel` permission to invoke this command.')
            return
        
        permissions = channel.cached_permissions_for(client)
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_channel):
            yield Embed('Permission denied',
                'I must have `create instant invite` and `manage channel` to invite to execute this command.')
            return
    
    yield
    
    if channel is None:
        coroutine = client.invite_get_all_guild(guild)
    else:
        coroutine = client.invite_get_all_guild(guild)
    invites = await coroutine
    
    pages = [Embed(description=chunk) for chunk in pchunkify(invites, write_parents=False)]
    
    if channel is None:
        check = check_guild_invites_pagination_permissions
    else:
        check = check_channel_invites_pagination_permissions
    
    await Pagination(client, event.channel, pages, 120., check=check)



@SLASH_CLIENT.interactions(is_global=True)
async def yeet(client, event,
        user :('user', 'Select the user to yeet!'),
        reason : ('str', 'Any reason why you would want to yeet?') = None,
        delete_message_days : ([(str(v), v) for v in range(8)], 'Delete previous messages?') = 0,
        notify_user : ('bool', 'Whether the user should get DM about the ban.') = True,
            ):
    """Yeets someone out of the guild. You must have ban users permission."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
    
    if not event.user_permissions.can_ban_users:
        yield Embed('Permission denied', 'You must have yeet users permission to use this command.')
        return
    
    if not guild.cached_permissions_for(client).can_ban_users:
        yield Embed('Permission denied', f'{client.name_at(guild)} cannot yeet in the guild.')
        return
    
    if not event.user.has_higher_role_than_at(user, guild):
        yield Embed('Permission denied', 'You must have higher role than the person to be yeeted.')
        return
    
    if not client.has_higher_role_than_at(user, guild):
        yield Embed('Permission denied', 'I must have higher role than the person to yeeted.')
        return
    
    if (reason is not None) and (not reason):
        reason = None
    
    yield
    
    if notify_user:
        if user.is_bot:
            notify_note = None
        else:
            try:
                channel = await client.channel_private_create(user)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return # We cannot help no internet
                
                raise
            
            embed = Embed('Yeeted', f'You were yeeted from {guild.name}.'). \
                add_field('Reason', '*No reason provided.*' if reason is None else reason)
            
            try:
                await client.message_create(channel, embed=embed)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return # We cannot help no internet
                
                elif isinstance(err, DiscordException) and (err.code == ERROR_CODES.cannot_message_user):
                    notify_note = 'Notification cannot be delivered: user has DM disabled.'
                else:
                    raise
            else:
                notify_note = None
    else:
        notify_note = None
    
    if reason is None:
        caller = event.user
        reason = f'Requested by: {caller.full_name} [{caller.id}]'
    
    await client.guild_ban_add(guild, user, delete_message_days=delete_message_days, reason=reason)
    
    embed = Embed('Hecatia yeah!', f'{user.full_name} has been yeeted.')
    if (notify_note is not None):
        embed.add_footer(notify_note)
    
    yield embed


ROLE_EMOJI_OK     = BUILTIN_EMOJIS['ok_hand']
ROLE_EMOJI_CANCEL = BUILTIN_EMOJIS['x']
ROLE_EMOJI_EMOJIS = (ROLE_EMOJI_OK, ROLE_EMOJI_CANCEL)

class _role_emoji_emoji_checker(object):
    __slots__ = ('guild',)
    
    def __init__(self, guild):
        self.guild = guild
    
    def __call__(self, event):
        if event.emoji not in ROLE_EMOJI_EMOJIS:
            return False
        
        user = event.user
        if user.is_bot:
            return False
        
        if not self.guild.permissions_for(user).can_administrator:
            return False
        
        return True

@SLASH_CLIENT.interactions(is_global=True)
async def emoji_role(client, event,
        emoji : ('str', 'Select the emoji to bind to roles.'),
        role_1 : ('role', 'Select a role.') = None,
        role_2 : ('role', 'Double role!') = None,
        role_3 : ('role', 'Triple role!') = None,
        role_4 : ('role', 'Quadra role!') = None,
        role_5 : ('role', 'Penta role!') = None,
        role_6 : ('role', 'Epic!') = None,
        role_7 : ('role', 'Legendary!') = None,
        role_8 : ('role', 'Mythical!') = None,
        role_9 : ('role', 'Lunatic!') = None,
            ):
    """Binds the given emoji to the selected roles. You must have administrator permission."""
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Ohoho', 'I must be in the guild to do this.')
        return
    
    if not event.user_permissions.can_ban_users:
        yield Embed('Permission denied', 'You must have ban users permission to use this command.')
        return
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_manage_emojis) or (not permissions.can_add_reactions):
        yield Embed('Permission denied',
            f'{client.name_at(guild)} requires manage emojis and add reactions permissions for this command.')
        return
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        yield Embed('Error', 'That\'s not an emoji.')
        return
    
    if emoji.is_unicode_emoji():
        yield Embed('Error', 'Cannot edit unicode emojis.')
        return
    
    emoji_guild = emoji.guild
    if (emoji_guild is None) or (emoji_guild is not guild):
        yield Embed('Error', 'Wont edit emojis from an other guild.')
        return
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        yield Embed('Error', f'Role {role.name}, [{role.id}] is bound to an other guild.')
        return
    
    roles = sorted(roles)
    roles_ = emoji.roles
    
    embed = Embed().add_author(emoji.url, emoji.name)
    
    if (roles_ is None) or (not roles_):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles_])
    
    embed.add_field('Roles before:', role_text)
    
    if (not roles):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles])
    
    embed.add_field('Roles after:', role_text)
    
    yield
    message = yield embed
    for emoji_ in ROLE_EMOJI_EMOJIS:
        await client.reaction_add(message, emoji_)
    
    try:
        event = await wait_for_reaction(client, message, _role_emoji_emoji_checker(message.guild), 300.)
    except TimeoutError:
        emoji_ = ROLE_EMOJI_CANCEL
    else:
        emoji_ = event.emoji
    
    if message.channel.cached_permissions_for(client).can_manage_messages:
        try:
            await client.reaction_clear(message)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return
            
            raise
    
    if emoji_ is ROLE_EMOJI_OK:
        try:
            await client.emoji_edit(emoji, roles=roles)
        except DiscordException as err:
            content = repr(err)
        else:
            content = 'Emoji edited successfully.'
    
    elif emoji_ is ROLE_EMOJI_CANCEL:
        content = 'Emoji edit cancelled'
    
    else: # should not happen
        return
    
    yield Embed(None, content)
