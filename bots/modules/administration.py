from datetime import datetime
from functools import partial as partial_func

from hata import Color, Embed, DiscordException, BUILTIN_EMOJIS, ERROR_CODES, parse_emoji, Client, ChannelText, \
    parse_rdelta, time_to_id, ChannelCategory, Emoji, Permission
from hata.ext.slash.menus import Pagination
from hata.ext.slash import abort, InteractionResponse, Row, Button, ButtonStyle, wait_for_component_interaction
from hata.ext.prettyprint import pchunkify

from bot_utils.constants import ROLE__SUPPORT__TESTER

ADMINISTRATION_COLOR = Color.from_rgb(148, 0, 211)

SLASH_CLIENT: Client

EMOJI__REIMU_HAMMER = Emoji.precreate(690550890045898812)

def match_message_author(user, message):
    return (message.author is user)

@SLASH_CLIENT.interactions(is_global=True, show_for_invoking_user_only=True)
async def clear(client, event,
        limit  : ('int'     , 'How much message?'                        )        ,
        before : ('str'     , 'Till when?'                               ) = None ,
        after  : ('str'     , 'Since when?'                              ) = None ,
        where  : ('channel' , 'Where?'                                   ) = None ,
        whos   : ('user'    , 'Who\'s message?'                          ) = None ,
        reason : ('str'     , 'Will show up in the guild\'s audit logs.' ) = None ,
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
        if not isinstance(where, ChannelText):
            abort('The channel must be a text channel.')
        
        channel = where
    
    if limit < 1:
        abort('`limit` cannot be non-positive.')
    
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to use this command.')
    
    client_permissions = channel.cached_permissions_for(client)
    if (not client_permissions.can_manage_messages) or (not client_permissions.can_read_message_history):
        abort('I must have manage messages and read message history in the channel to do it.')
    
    if (before is None) or (not before):
        before = event.id
    else:
        delta = parse_rdelta(before)
        if delta is None:
            abort('`before` could not be parsed.')
        
        before = time_to_id(datetime.utcnow()-delta)
    
    if (after is None) or (not after):
        after = 0
    else:
        delta = parse_rdelta(after)
        if delta is None:
            yield Embed('Error', '`after` could not be parsed.')
        
        before = time_to_id(datetime.utcnow()-delta)
    
    yield 'Yeeting messages began'
    
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
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if not event.user_permissions.can_create_instant_invite:
        abort('You must have `create instant invite` permission to invoke this command.')
    
    if not guild.cached_permissions_for(client).can_create_instant_invite:
        abort('I must have `create instant invite` permission invite to execute this command.')
    
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
    guild = event.message.guild
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
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if not event.user_permissions.can_ban_users:
        abort('You must have `ban users` permission to invoke this command.')
    
    if not guild.cached_permissions_for(client).can_ban_users:
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
    
    await Pagination(client, event, result, check=bans_pagination_check)


def check_channel_invites_pagination_permissions(event):
    permissions = event.message.channel.permissions_for(event.user)
    if not permissions.can_manage_channel:
        return False
    
    if not permissions.can_create_instant_invite:
        return False
    
    return True

def check_guild_invites_pagination_permissions(event):
    guild = event.message.guild
    if guild is None:
        return False
    
    permissions = guild.permissions_for(event.user)
    if not permissions.can_manage_guild:
        return False
    
    if not permissions.can_create_instant_invite:
        return False
    
    return True

PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

@SLASH_CLIENT.interactions(is_global=True)
async def invites_(client, event,
        channel : ('channel', 'Which channel\'s invites do you wanna check?') = None,
            ):
    """Shows up the guild's or the selected channel's invites."""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute the command.')
    
    if (channel is not None) and isinstance(channel, ChannelCategory):
        abort('Category channels have no invites.')
    
    if not event.channel.cached_permissions_for(client)&PERMISSION_MASK_MESSAGING:
        abort('I must have `send messages` permission to invoke this command correctly.')
    
    if channel is None:
        permissions = event.user_permissions
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_guild):
            abort('You must have `create instant invite` and `manage guild` permission to invoke this command.')
        
        permissions = guild.cached_permissions_for(client)
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_guild):
            abort('I must have `create instant invite` and `manage guild` to invite to execute this command.')
    
    else:
        permissions = event.user_permissions
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_channel):
            abort('You must have `create instant invite` and `manage channel` permission to invoke this command.')
        
        permissions = channel.cached_permissions_for(client)
        if (not permissions.can_create_instant_invite) or (not permissions.can_manage_channel):
            abort('I must have `create instant invite` and `manage channel` to invite to execute this command.')
    
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
    
    await Pagination(client, event, pages, timeout=120., check=check)


def check_banner(user, event):
    return user is event.user

    
BAN_BUTTON_CONFIRM = Button('Yes', EMOJI__REIMU_HAMMER, style=ButtonStyle.red)
BAN_BUTTON_CANCEL = Button('No', style=ButtonStyle.gray)

BAN_COMPONENTS = Row(BAN_BUTTON_CONFIRM, BAN_BUTTON_CANCEL)


@SLASH_CLIENT.interactions(is_global=True)
async def ban(client, event,
        user : ('user', 'Select the user to yeet!'),
        reason : ('str', 'Any reason why you would want to yeet?') = None,
        delete_message_days : (range(8), 'Delete previous messages?') = 0,
        notify_user : ('bool', 'Whether the user should get DM about the ban.') = True,
            ):
    """Yeets someone out of the guild. You must have ban users permission."""
    # Check permissions
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to do this.')
    
    if not event.user_permissions.can_ban_users:
        abort('You must have yeet users permission to use this command.')
    
    if not guild.cached_permissions_for(client).can_ban_users:
        abort(f'{client.name_at(guild)} cannot yeet in the guild.')
    
    if not event.user.has_higher_role_than_at(user, guild):
        abort('You must have higher role than the person to be yeeted.')
    
    if not client.has_higher_role_than_at(user, guild):
        abort('I must have higher role than the person to yeeted.')
    
    # Ask, whether the user should be banned.
    if (reason is not None) and (not reason):
        reason = None
    
    embed = Embed('Confirmation', f'Are you sure to yeet {user.mention} from {guild.name}?'). \
        add_field('Delete message day', str(delete_message_days), inline=True). \
        add_field('Notify user', 'true' if notify_user else 'false', inline=True). \
        add_field('Reason', '*No reason provided.*' if reason is None else reason)

    
    message = yield InteractionResponse(embed=embed, components=BAN_COMPONENTS, allowed_mentions=None)
    
    # Wait for user input
    
    try:
        component_interaction = await wait_for_component_interaction(message, timeout=300.0,
            check=partial_func(check_banner, event.user))
    
    except TimeoutError:
        embed.title = 'Timeout'
        embed.description = f'{user.mention} was not yeeted from {guild.name}.'
        
        # Edit the source message with the source interaction
        yield InteractionResponse(embed=embed, components=None, allowed_mentions=None, message=message)
        return
    
    if component_interaction.interaction == BAN_BUTTON_CANCEL:
        embed.title = 'Cancelled'
        embed.description = f'{user.mention} was not yeeted from {guild.name}.'
        
        # Edit the source message with the component interaction
        yield InteractionResponse(embed=embed, components=None, allowed_mentions=None, event=component_interaction)
        return
    
    # Acknowledge the event
    await client.interaction_component_acknowledge(component_interaction)
    
    # Try to notify the user. Ignore bot notifications.
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
    
    # Edit the source message
    yield InteractionResponse(embed=embed, message=message, components=None)


@SLASH_CLIENT.interactions(is_global=True)
async def is_banned(client, event,
        user: ('user', 'Who should I check?')
            ):
    """Checks whether the user is banned."""
    if (not event.user.has_role(ROLE__SUPPORT__TESTER)) and (not event.user_permissions.can_ban_users):
        abort('You need to have `ban users` permissions to do this.')
    
    if not event.channel.cached_permissions_for(client).can_ban_users:
        abort('I need to have `ban users` permissions to do this.')
    
    yield # acknowledge the event
    
    try:
        ban_entry = await client.guild_ban_get(event.guild, user)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            ban_entry = None
        else:
            raise
    
    embed = Embed(f'Ban entry for {user:f}').add_thumbnail(user.avatar_url)
    
    if ban_entry is None:
        embed.description = 'The user **NOT YET** banned.'
    
    else:
        embed.description = 'The user is banned.'
        
        reason = ban_entry.reason
        if reason is None:
            reason = '*No reason was specified.*'
        
        embed.add_field('Reason:', reason)
    
    yield embed


ROLE_EMOJI_CONFIRM= BUILTIN_EMOJIS['ok_hand']
ROLE_EMOJI_CANCEL = BUILTIN_EMOJIS['x']

EMOJI_ROLE_BUTTON_CONFIRM = Button(emoji=ROLE_EMOJI_CONFIRM, style=ButtonStyle.green)
EMOJI_ROLE_BUTTON_CANCEL = Button(emoji=ROLE_EMOJI_CANCEL, style=ButtonStyle.violet)
EMOJI_ROLE_COMPONENTS = Row(EMOJI_ROLE_BUTTON_CONFIRM, EMOJI_ROLE_BUTTON_CANCEL)


def role_emoji_checker(event):
    guild = event.guild
    if guild is None:
        return False
    
    if guild.permissions_for(event.user).can_administrator:
        return True
    
    return False


@SLASH_CLIENT.interactions(is_global=True)
async def emoji_role(client, event,
        emoji: ('str', 'Select the emoji to bind to roles.'),
        role_1: ('role', 'Select a role.') = None,
        role_2: ('role', 'Double role!') = None,
        role_3: ('role', 'Triple role!') = None,
        role_4: ('role', 'Quadra role!') = None,
        role_5: ('role', 'Penta role!') = None,
        role_6: ('role', 'Epic!') = None,
        role_7: ('role', 'Legendary!') = None,
        role_8: ('role', 'Mythical!') = None,
        role_9: ('role', 'Lunatic!') = None,
            ):
    """Binds the given emoji to the selected roles. You must have administrator permission."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to do this.')
    
    if not event.user_permissions.can_ban_users:
        abort('You must have ban users permission to use this command.')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_manage_emojis_and_stickers) or (not permissions.can_add_reactions):
        abort(f'{client.name_at(guild)} requires manage emojis and add reactions permissions for this command.')
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        abort('That\'s not an emoji.')
    
    if emoji.is_unicode_emoji():
        abort('Cannot edit unicode emojis.')
    
    emoji_guild = emoji.guild
    if (emoji_guild is None) or (emoji_guild is not guild):
        abort('Wont edit emojis from an other guild.')
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        abort(f'Role {role.name}, [{role.id}] is bound to an other guild.')
    
    roles = sorted(roles)
    roles_ = emoji.roles
    
    embed = Embed(f'Edit {emoji.name}\'s roles').add_thumbnail(emoji.url)
    
    if (roles_ is None) or (not roles_):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles_])
    
    embed.add_field('Before:', role_text)
    
    if (not roles):
        role_text = '*none*'
    else:
        role_text = ', '.join([role.mention for role in roles])
    
    embed.add_field('After:', role_text)
    
    message = yield InteractionResponse(embed=embed, components=EMOJI_ROLE_COMPONENTS)
    
    try:
        component_interaction = await wait_for_component_interaction(message, timeout=300.0, check=role_emoji_checker)
    
    except TimeoutError:
        component_interaction = None
        cancelled = True
    else:
        if component_interaction.interaction == EMOJI_ROLE_BUTTON_CANCEL:
            cancelled = True
        else:
            cancelled = False
    
    if cancelled:
        description = 'Emoji edit cancelled.'
    else:
        try:
            await client.emoji_edit(emoji, roles=roles)
        except DiscordException as err:
            description = repr(err)
        else:
            description = 'Emoji edited successfully.'
    
    embed = Embed(f'Edit {emoji.name}\'s roles', description).add_thumbnail(emoji.url)
    yield InteractionResponse(embed=embed, components=None, message=message, event=component_interaction)
