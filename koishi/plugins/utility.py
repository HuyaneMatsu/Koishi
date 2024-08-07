__all__ = ()

import json
from colorsys import rgb_to_hsv, rgb_to_yiq
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from functools import partial as partial_func
from math import ceil
from random import choice

from PIL import Image as PIL
from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import (
    BUILTIN_EMOJIS, Color, DATETIME_FORMAT_CODE, Embed, ICON_TYPE_NONE, InviteTargetType, KOKORO, Permission, Status,
    cchunkify, elapsed_time, escape_markdown, parse_color
)
from hata.discord.application.application.constants import EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID
from hata.ext.slash import InteractionResponse, abort
from hata.ext.slash.menus import Pagination
from scarletio import ReuBytesIO, TaskGroup

from ..bot_utils.constants import GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT
from ..bot_utils.tools import Pagination10step
from ..bots import FEATURE_CLIENTS, MAIN_CLIENT


UTILITY_COLOR = Color(0x5dc66f)

PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

STATUS_ONLINE = Status.online
STATUS_IDLE = Status.idle
STATUS_DND = Status.dnd
STATUS_OFFLINE = Status.offline

STATUS_VALUE_OFFLINE = STATUS_OFFLINE.value

EMOJI_HEART_GREEN = BUILTIN_EMOJIS['green_heart']
EMOJI_HEART_YELLOW = BUILTIN_EMOJIS['yellow_heart']
EMOJI_HEART_RED = BUILTIN_EMOJIS['heart']
EMOJI_HEART_BLACK = BUILTIN_EMOJIS['black_heart']

STATUS_VALUE_TO_HEART_EMOJI = {
    STATUS_ONLINE.value: EMOJI_HEART_GREEN,
    STATUS_IDLE.value: EMOJI_HEART_YELLOW,
    STATUS_DND.value: EMOJI_HEART_RED,
    STATUS_OFFLINE.value: EMOJI_HEART_BLACK,
}

PLATFORMS = ('desktop', 'mobile', 'web')

@FEATURE_CLIENTS.interactions(is_global = True)
async def rawr(client, event):
    """Sends a message with everyone from my universe."""
    channel = event.channel
    tasks = []
    
    for client_ in channel.clients:
        if client_ is client:
            coroutine = client.interaction_response_message_create(event, 'Rawrr !')
        else:
            if not channel.cached_permissions_for(client_) & PERMISSION_MASK_MESSAGING:
                continue
            
            coroutine = client_.message_create(channel, 'Rawrr !')
        tasks.append(KOKORO.create_task(coroutine))
    
    task_group = TaskGroup(KOKORO, tasks)
    failed_task = await task_group.wait_exception()
    if (failed_task is not None):
        # Cancel all and propagate the exception of the first failed task.
        task_group.cancel_all()
        failed_task.get_result()


@FEATURE_CLIENTS.interactions(is_global = True)
async def color_(
    client,
    event,
    color: ('str', 'Beauty!'),
):
    """Shows the given color"""
    
    color = parse_color(color)
    if color is None:
        yield 'Could not recognize the color.'
        return
    
    yield
    
    embed = Embed(color = color)
    embed.add_field('hex', f'#{color:06X}', inline = True)
    embed.add_field('rgb', f'{color >> 16} r\n{(color >> 8) & 255} g\n{color & 255} b', inline = True)
    r, g, b = color.as_rgb_float_tuple
    embed.add_field('rgb%', f'{r * 100.0:0.2f}% r\n{g * 100.0:0.2f}% g\n{b * 100.0:0.2f}% b', inline = True)
    h, s, v = rgb_to_hsv(r, g, b)
    embed.add_field('hsv%', f'{h * 100.0:0.2f}% h\n{s * 100.0:0.2f}% s\n{v * 100.0:0.2f}% v', inline = True)
    y, i, q = rgb_to_yiq(r, g, b)
    embed.add_field('yiq%', f'{y * 100.0:0.2f}% y\n{i * 100.0:0.2f}% i\n{q * 100.0:0.2f}% q', inline = True)
    
    embed.add_image('attachment://color.png')
    
    with ReuBytesIO() as buffer:
        image = PIL.new('RGB', (240, 30), color.as_rgb)
        image.save(buffer,'png')
        buffer.seek(0)
        
        await client.interaction_followup_message_create(event, embed = embed, file = ('color.png', buffer))


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    target = 'message',
    required_permissions = Permission().update_by_keys(manage_messages = True),
)
async def raw(client, event):
    """Shows up the message's payload."""
    if not event.user_permissions.can_manage_messages:
        abort('You must have manage messages permission to invoke this command.')
    
    data = await client.api.message_get(event.channel_id, event.interaction.target_id)
    chunks = cchunkify(json.dumps(data, indent = 4, sort_keys = True).splitlines())
    
    pages = [Embed(description = chunk) for chunk in chunks]
    await Pagination(client, event, pages)


class RoleCache:
    __slots__ = ('cache', 'guild', 'roles',)
    
    def __new__(cls, guild):
        self = object.__new__(cls)
        self.guild = guild
        roles = guild.role_list
        roles.reverse()
        self.roles = roles
        self.cache = {}
        
        self.create_page_0(guild)
        return self
    
    def create_page_0(self, guild):
        embed = Embed(
            f'Roles of **{guild.name}**:',
            '\n'.join([role.mention for role in self.roles]),
            color = (guild.icon_hash & 0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xFFFFFF),
        )
        
        embed.add_footer(f'Page 1 / {len(self.roles) + 1}')
        self.cache[0] = embed
    
    def __getitem__(self,index):
        page = self.cache.get(index, None)
        if page is None:
            page = self.create_page(index)
        
        return page

    def create_page(self,index):
        role = self.roles[index - 1]
        embed = Embed(role.name,
            '\n'.join([
                f'id : {role.id!r}',
                f'color : {role.color.as_html}',
                f'permission number : {role.permissions:d}',
                f'managed : {role.managed}',
                f'separated : {role.separated}',
                f'mentionable : {role.mentionable}',
                '\nPermissions:\n```diff',
                *(f'{"+" if value else "-"}{key.replace("_", "-")}' for key, value in role.permissions.items()),
                '```',
            ]),
            color = role.color,
        )
        embed.add_footer(f'Page {index + 1} /  {len(self.roles) + 1}')
        
        self.cache[index] = embed
        return embed
    
    def __len__(self):
        return len(self.roles) + 1

PERMISSION_MASK_REACT = Permission().update_by_keys(
    add_reactions = True,
)

@FEATURE_CLIENTS.interactions(is_global = True)
async def roles_(client, event):
    """Lists the roles of the guild for my cutie!"""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute this command')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions & PERMISSION_MASK_MESSAGING) or ( not permissions & PERMISSION_MASK_REACT):
        abort('I require `send messages` and `add reactions` permissions to execute this command.')
    
    await Pagination10step(client, event, RoleCache(guild))


# Koishi user caching will be disabled, so this command would not work.
'''
def shared_guilds_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False


@FEATURE_CLIENTS.interactions(is_global = True)
async def shared_guilds(client, event):
    """Returns the shared guilds between you and me."""
    pages = []
    lines = []
    lines_count = 0
    
    user = event.user
    for guild_id, guild_profile in user.guild_profiles.items():
        guild = GUILDS[guild_id]
        nick = guild_profile.nick
        guild_name = guild.name
        if nick is None:
            line = guild_name
        else:
            line = f'{guild_name} [{nick}]'
        
        lines.append(line)
        lines_count += 1
        
        if lines_count == 10:
            pages.append('\n'.join(lines))
            lines.clear()
            lines_count = 0
    
    if lines_count:
        pages.append('\n'.join(lines))
    
    if not pages:
        pages.append('*none*')
    
    embeds = []
    embed_title = f'Shared guilds with {user.full_name}:'
    
    for page in pages:
        embed = Embed(embed_title, page, color = UTILITY_COLOR)
        embeds.append(embed)
    
    await Pagination(client, event, embeds, check = partial_func(shared_guilds_pagination_check, user))
'''


USER_PER_PAGE = 16
class InRolePageGetter:
    __slots__ = ('users', 'guild', 'title')
    def __init__(self, users, guild, roles):
        title_parts = ['Users with roles: ']
        
        roles = sorted(roles)
        index = 0
        limit = len(roles)
        
        while True:
            role = roles[index]
            index += 1
            role_name = role.name
            
            # Handle special case, when the role is an application's role, what means it's length can be over 32-
            if len(role_name) > 32:
                role_name = role_name[:32]+'...'
            
            title_parts.append(role_name)
            
            if index == limit:
                break
            
            title_parts.append(', ')
            
        self.title = ''.join(title_parts)
        self.users = users
        self.guild = guild
    
    def __len__(self):
        length = len(self.users)
        if length:
            length = ceil(length / USER_PER_PAGE)
        else:
            length = 1
        
        return length
    
    def __getitem__(self, index):
        users = self.users
        length = len(users)
        guild = self.guild
        if length:
            user_index = index * USER_PER_PAGE
            user_limit = user_index + USER_PER_PAGE
            
            if user_limit > length:
                user_limit = length
            
            description_parts = []
            while True:
                user = users[user_index]
                user_index += 1
                description_parts.append(user.full_name)
                guild_profile = user.get_guild_profile_for(guild)
                if (guild_profile is not None):
                    nick = guild_profile.nick
                    if nick is not None:
                        description_parts.append(' *[')
                        description_parts.append(nick)
                        description_parts.append(']*')
                
                if user_index == user_limit:
                    break
                
                description_parts.append('\n')
                continue
            
            description = ''.join(description_parts)
        
        else:
            description = '*none*'
        
        return Embed(
            self.title,
            description,
        ).add_author(
            guild.name,
            guild.icon_url,
        ).add_footer(
            f'Page {index + 1}/{ceil(len(self.users) / USER_PER_PAGE)}',
        )


def in_role_pagination_check(user, event):
    event_user = event.user
    if user is event.user:
        return True
    
    if event.message.channel.permissions_for(event_user).can_manage_messages:
        return True
    
    return False

@MAIN_CLIENT.interactions(guild = [GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT])
async def in_role(
    client,
    event,
    role_1: ('role', 'Select a role.'),
    role_2: ('role', 'Double role!') = None,
    role_3: ('role', 'Triple role!') = None,
    role_4: ('role', 'Quadra role!') = None,
    role_5: ('role', 'Penta role!') = None,
    role_6: ('role', 'Epic!') = None,
    role_7: ('role', 'Legendary!') = None,
    role_8: ('role', 'Mythical!') = None,
    role_9: ('role', 'Lunatic!') = None,
):
    """Shows the users with the given roles."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    roles = set()
    for role in role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8, role_9:
        if role is None:
            continue
        
        if role.guild is guild:
            roles.add(role)
            continue
        
        abort(f'Role {role.name}, [{role.id}] is bound to an other guild.')
    
    users = []
    for user in guild.users.values():
        guild_profile = user.get_guild_profile_for(guild)
        if guild_profile is None:
            continue
        
        guild_profile_roles = guild_profile.roles
        if guild_profile_roles is None:
            continue
        
        if not roles.issubset(guild_profile_roles):
            continue
        
        users.append(user)
    
    pages = InRolePageGetter(users, guild, roles)
    
    await Pagination(client, event, pages, check = partial_func(in_role_pagination_check, event.user))


@FEATURE_CLIENTS.interactions(is_global = True, target = 'user')
async def status_(user):
    status = user.status
    emoji = STATUS_VALUE_TO_HEART_EMOJI.get(status.value, EMOJI_HEART_BLACK)
    
    embed = Embed(f'{user.full_name}\'s status', f'{emoji} {status.name}').add_thumbnail(user.avatar_url)
    
    statuses = user.statuses
    if (statuses is not None) and statuses:
        field_value_parts = []
        
        for platform in PLATFORMS:
            status_value = statuses.get(platform, STATUS_VALUE_OFFLINE)
            emoji = STATUS_VALUE_TO_HEART_EMOJI.get(status_value, EMOJI_HEART_BLACK)
            
            if field_value_parts:
                field_value_parts.append('\n')
            
            field_value_parts.append(platform)
            field_value_parts.append(': ')
            field_value_parts.append(emoji.as_emoji)
            field_value_parts.append(' ')
            field_value_parts.append(status_value)
        
        field_value = ''.join(field_value_parts)
        
        embed.add_field('Per platform', field_value)
    
    
    return embed


def add_user_field(embed, index, joined_at, user):
    created_at = user.created_at
    embed.add_field(
        f'{index}. {user.full_name}',
        (
            f'Id: {user.id}\n'
            f'Mention: {user.mention}\n'
            '\n'
            f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
            f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
            f'Difference : {elapsed_time(RelativeDelta(created_at, joined_at))}'
        ),
    )

@MAIN_CLIENT.interactions(
    guild = [GUILD__SUPPORT, GUILD__ORIN_PARTY_HOUSE],
    required_permissions = Permission().update_by_keys(kick_users = True),
)
async def latest_users(client, event):
    """Shows the new users of the guild."""
    if not event.user_permissions.can_kick_users:
        abort('You must have kick users to invoke this command.')
    
    date_limit = DateTime.now(TimeZone.utc) - TimeDelta(days = 7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # Use created at and not `joined_at`, we can ignore lurkers.
        created_at = user.get_guild_profile_for(guild).created_at
        if created_at > date_limit:
            users.append((created_at, user))
    
    users.sort(reverse = True)
    del users[10:]
    
    embed = Embed('Recently joined users')
    if users:
        for index, (joined_at, user) in enumerate(users, 1):
            add_user_field(embed, index, joined_at, user)
    
    else:
        embed.description = '*none*'
    
    return InteractionResponse(embed = embed, allowed_mentions = None)


@MAIN_CLIENT.interactions(
    guild = [GUILD__ORIN_PARTY_HOUSE, GUILD__SUPPORT],
    required_permissions = Permission().update_by_keys(kick_users = True),
)
async def all_users(client, event):
    """Shows the new users of the guild."""
    if not event.user_permissions.can_kick_users:
        abort('You must have kick users to invoke this command.')
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        joined_at = user.get_guild_profile_for(guild).joined_at
        if (joined_at is not None):
            users.append((joined_at, user))
    
    users.sort(reverse = True)
    
    embeds = []
    
    for index, (joined_at, user) in enumerate(users, 1):
        if index % 10 == 1:
            embed = Embed('Joined users')
            embeds.append(embed)
        
        add_user_field(embed, index, joined_at, user)
    
    
    await Pagination(client, event, embeds)


@FEATURE_CLIENTS.interactions(is_global = True, target = 'message')
async def escape(message):
    content = message.content
    if content is None:
        abort('The message has no content to escape')
    
    content = escape_markdown(content)
    if len(content) > 2000:
        content = content[:1997]+'...'
    
    return InteractionResponse(content, allowed_mentions = None)


@FEATURE_CLIENTS.interactions(integration_types = ['guild_install', 'user_install'], is_global = True)
async def calc(
    expression: ('expression', 'Mathematical expression to evaluate')
):
    return repr(expression)


@FEATURE_CLIENTS.interactions(is_global = True)
async def choose(
    choice_1: (str, 'choice'),
    choice_2: (str, 'another one') = None,
    choice_3: (str, 'another one') = None,
    choice_4: (str, 'another one') = None,
    choice_5: (str, 'another one') = None,
    choice_6: (str, 'another one') = None,
    choice_7: (str, 'another one') = None,
    choice_8: (str, 'another one') = None,
    choice_9: (str, 'another one') = None,
    choice_10: (str, 'another one') = None,
    choice_11: (str, 'another one') = None,
    choice_12: (str, 'another one') = None,
    choice_13: (str, 'another one') = None,
    choice_14: (str, 'another one') = None,
    choice_15: (str, 'another one') = None,
    choice_16: (str, 'another one') = None,
    choice_17: (str, 'another one') = None,
    choice_18: (str, 'another one') = None,
    choice_19: (str, 'another one') = None,
    choice_20: (str, 'another one') = None,
    choice_21: (str, 'another one') = None,
    choice_22: (str, 'another one') = None,
    choice_23: (str, 'another one') = None,
    choice_24: (str, 'another one') = None,
    choice_25: (str, 'another one') = None,
):
    return InteractionResponse(
        choice([
            choice_ for choice_ in (
                choice_1, choice_2, choice_3, choice_4, choice_5,
                choice_6, choice_7, choice_8, choice_9, choice_10,
                choice_11, choice_12, choice_13, choice_14, choice_15,
                choice_16, choice_17, choice_18, choice_19, choice_20,
                choice_21, choice_22, choice_23, choice_24, choice_25,
            ) if choice_ is not None
        ]),
        allowed_mentions = None,
    )


CREATE_EMBEDDED_ACTIVITY_PERMISSIONS = Permission().update_by_keys(
    use_embedded_activities = True,
    create_instant_invite = True,
)

@FEATURE_CLIENTS.interactions(is_global = True)
async def create_activity(
    client,
    event,
    activity: (EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID, 'Select an activity'),
    channel: ('channel_guild_voice', 'The channel to create the activity for.') = None,
):
    """Creates an embedded activity."""
    if event.user_permissions & CREATE_EMBEDDED_ACTIVITY_PERMISSIONS != CREATE_EMBEDDED_ACTIVITY_PERMISSIONS:
        abort(
            'You need to have `create instant invite` and `create embedded activities` permission to invoke this '
            'command'
        )
    
    # Use goto to detect channel.
    while True:
        if channel is not None:
            break
        
        guild = event.guild
        if (guild is not None):
            voice_state = guild.get_voice_state(event.user.id)
            if (voice_state is not None):
                channel = voice_state.channel
                if channel.is_guild_voice():
                    break
        
        abort('Please give a voice channel or be in one.')
    
    client_permissions = channel.cached_permissions_for(client)
    if client_permissions & CREATE_EMBEDDED_ACTIVITY_PERMISSIONS != CREATE_EMBEDDED_ACTIVITY_PERMISSIONS:
        abort(
            f'I need to have `create instant invite` and `create embedded activities` permission in '
            f'{channel.mention} to execute this command.'
        )
    
    invite = await client.invite_create(
        channel,
        max_age = 21600,  # 6 hours
        target_application_id = activity,
        target_type = InviteTargetType.embedded_application,
    )
    return invite.url
