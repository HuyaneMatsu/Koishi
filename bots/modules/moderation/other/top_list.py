__all__ = ()

import re
from datetime import datetime as DateTime, timedelta as TimeDelta
from math import floor, log10

from hata import (
    AnsiForegroundColor, AnsiTextDecoration, AuditLogEvent, BUILTIN_EMOJIS, Client, Embed, KOKORO, Permission,
    create_ansi_format_code
)
from hata.ext.slash import Button, InteractionResponse, P, Row
from scarletio import RichAttributeErrorBaseType, TaskGroup

from ..shared_constants import REASON_RP

from .helpers import (
    check_required_permissions_only_client, check_required_permissions_only_guild, check_required_permissions_only_user
)

from bot_utils.user_getter import get_user


DELTA_DAY = TimeDelta(days = 1)

PAGE_SIZE = 20

TYPE_BAN = 1 << 0
TYPE_KICK = 1 << 1
TYPE_MUTE = 1 << 2
TYPE_ALL = TYPE_BAN | TYPE_KICK | TYPE_MUTE

NAME_BAN = 'ban'
NAME_KICK = 'kick'
NAME_MUTE = 'mute'
NAME_ALL = 'all'

TYPES = [
    (NAME_ALL, TYPE_ALL),
    (NAME_BAN, TYPE_BAN),
    (NAME_KICK, TYPE_KICK),
    (NAME_MUTE, TYPE_MUTE),
]

TYPE_TO_NAME = {value: key for value, key in TYPES}

SORT_KEY_ALL = lambda item: (item[1].ban, 0 - item[0].id)

SORT_KEYS_BY_TYPE = {
    TYPE_BAN: lambda item: (item[1].ban, 0 - item[0].id),
    TYPE_KICK: lambda item: (item[1].ban, 0 - item[0].id),
    TYPE_MUTE: lambda item: (item[1].ban, 0 - item[0].id),
    TYPE_ALL: SORT_KEY_ALL,
}

STYLE_NONE = create_ansi_format_code(text_decoration = AnsiTextDecoration.none)
STYLE_BAN = create_ansi_format_code(text_decoration = AnsiForegroundColor.blue)
STYLE_KICK = create_ansi_format_code(text_decoration = AnsiForegroundColor.teal)
STYLE_MUTE = create_ansi_format_code(text_decoration = AnsiForegroundColor.green)
STYLE_ALL = create_ansi_format_code(text_decoration = AnsiForegroundColor.orange)
STYLE_FOCUS = create_ansi_format_code(text_decoration = AnsiForegroundColor.pink)


NAME_BAN_HEADER = NAME_BAN.upper()
NAME_KICK_HEADER = NAME_KICK.upper()
NAME_MUTE_HEADER = NAME_MUTE.upper()
NAME_ALL_HEADER = NAME_ALL.upper()


EMOJI_BACK = BUILTIN_EMOJIS['arrow_backward']
EMOJI_NEXT = BUILTIN_EMOJIS['arrow_forward']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

PAGE_MIN = 1
PAGE_MAX = 99

DAYS_MIN = 1
DAYS_MAX = 45

CUSTOM_ID_BACK_DISABLED = 'mod.top_list.page.min.disabled'
CUSTOM_ID_NEXT_DISABLED = 'mod.top_list.page.max.disabled'
CUSTOM_ID_CLOSE = 'mod.top_list.close'
CUSTOM_ID_PAGE_RP = re.compile('mod\\.top_list\\.page\\.(\d+);s=(\d+);d=(\d+)')

BUTTON_BACK__DISABLED = Button(
    f'Page {PAGE_MIN - 1}',
    EMOJI_BACK,
    custom_id = CUSTOM_ID_BACK_DISABLED,
    enabled = False,
)
    
BUTTON_NEXT_DISABLED = Button(
    f'Page {PAGE_MAX + 1}',
    EMOJI_NEXT,
    custom_id = CUSTOM_ID_NEXT_DISABLED,
    enabled = False,
)

BUTTON_CLOSE = Button(
    'Close',
    EMOJI_CLOSE,
    custom_id = CUSTOM_ID_CLOSE,
)


REQUIRED_PERMISSIONS_USER_VALUE = Permission().update_by_keys(
    ban_users = True,
    kick_users = True,
    moderate_users = True,
    view_audit_logs = True,
)

REQUIRED_PERMISSIONS_USER_NAME = 'ban, kick, moderate users and view audit logs'


REQUIRED_PERMISSIONS_CLIENT_VALUE = Permission().update_by_keys(
    view_audit_logs = True,
)
REQUIRED_PERMISSIONS_CLIENT_NAME = 'view audit logs'


class ActionCounter(RichAttributeErrorBaseType):
    """
    Used to count moderation actions.
    
    Attributes
    ----------
    all : `int`
        The total actions executed.
    ban : `int`
        Bans executed.
    kick : `int`
        Kicks executed.
    mute : `int`
        Mutes executed.
    """
    __slots__ = ('all', 'ban', 'kick', 'mute')
    
    def __new__(cls):
        """
        Creates a new action counter.
        """
        self = object.__new__(cls)
        self.all = 0
        self.ban = 0
        self.kick = 0
        self.mute = 0
        return self
    
    
    def increment_by(self, action_type):
        """
        Increments the action counter counter by the given action type.
        
        Parameters
        ----------
        action_type : `int`
            Action type identifier.
        """
        self.all += 1
        
        if action_type == TYPE_BAN:
            self.ban += 1
        
        elif action_type == TYPE_KICK:
            self.kick += 1
        
        elif action_type == TYPE_MUTE:
            self.mute += 1
    
    
    def __repr_(self):
        """Returns the action counter's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' all = ')
        repr_parts.append(repr(self.all))
        
        repr_parts.append(', ban = ')
        repr_parts.append(repr(self.ban))
        
        repr_parts.append(', kick = ')
        repr_parts.append(repr(self.kick))
        
        repr_parts.append(', mute = ')
        repr_parts.append(repr(self.mute))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


async def get_source_user_from_client_entry(entry):
    """
    Gets the source invoker user if the client executed an action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : ``AuditLogEntry``
        The entry to inspect.
    
    Returns
    -------
    source_user : `None`, ``ClientUserBase``
    """
    reason = entry.reason
    if (reason is None):
        return None
    
    match = REASON_RP.fullmatch(reason)
    if match is None:
        return None
    
    user_id =  int(match.group(1))
    return await get_user(user_id)


async def request_bans(client, guild, after, actions):
    """
    Requests all the bans after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEvent.member_ban_add)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        actions.add((TYPE_BAN, source_user, audit_log_entry.target))


async def request_kicks(client, guild, after, actions):
    """
    Requests all the kicks after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEvent.member_kick)):
        if audit_log_entry.created_at < after:
            break
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        actions.add((TYPE_KICK, source_user, audit_log_entry.target))


async def request_mutes(client, guild, after, actions):
    """
    Requests all the mutes after the given time.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        The executed actions to extend.
    """
    async for audit_log_entry in (await client.audit_log_iterator(guild, event = AuditLogEvent.member_update)):
        if audit_log_entry.created_at < after:
            break
        
        changes = audit_log_entry.changes
        if (changes is None):
            continue
            
        for change in changes:
            if change.attribute_name == 'timed_out_until':
                break
        else:
            continue
        
        if change.after is None:
            continue
        
        source_user = audit_log_entry.user
        if source_user is None:
            continue
        
        if source_user is client:
            source_user = await get_source_user_from_client_entry(audit_log_entry)
            if source_user is None:
                continue
        
        elif source_user.bot:
            continue
        
        actions.add((TYPE_MUTE, source_user, audit_log_entry.target))


async def request_actions(client, guild, after):
    """
    Requests the actions for the given action type in the given interva
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    after : `DateTime`
        The date to get the logs after.
    
    Returns
    -------
    actions : `set` of `tuple` (`int`, ``ClientUserBase``, ``ClientUserBase``)
        A set of `action type` - `source user` - `target user` tuples.
    """
    actions = set()
    
    task_group = TaskGroup(KOKORO)
    task_group.create_task(request_bans(client, guild, after, actions))
    task_group.create_task(request_kicks(client, guild, after, actions))
    task_group.create_task(request_mutes(client, guild, after, actions))
    
    failed_task = await task_group.wait_exception()
    if (failed_task is not None):
        task_group.cancel_all()
        failed_task.get_result()
    
    return actions



async def request_top_list(client, guild, sort_by, days, page):
    """
    Requests raw moderation top-list for the given guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the audit logs with.
    guild : ``Guild``
        The guild to request the actions at.
    sort_by : `int`
        The field's identifier to sort by.
    days : `int`
        The amount of days to request.
    page : `int`
        The page number to filter for.
    
    Returns
    -------
    top_list : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
    """
    actions = await request_actions(client, guild, DateTime.utcnow() - (DELTA_DAY * days))
    
    by_user = {}
    for action in actions:
        source_user = action[1]
        
        try:
            counter = by_user[source_user]
        except KeyError:
            counter = ActionCounter()
            by_user[source_user] = counter
        
        counter.increment_by(action[0])
    
    return sorted(
        by_user.items(),
        key = SORT_KEYS_BY_TYPE.get(sort_by, SORT_KEY_ALL),
        reverse = True,
    )[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]


def get_integer_length(value):
    """
    Gets an integer's length.
    
    Parameters
    ----------
    value : `int`
        The value to get its length of.
    
    Returns
    -------
    length : `int`
    """
    if not value:
        return 1
    
    return floor(log10(value)) + 1


def build_top_list_listing(top_list, sort_by, page):
    """
    Builds the top-list listing.
    
    Parameters
    ----------
    top_list : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
        Top list to show.
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    page : `int`
        The page to show. Used to calculate entry index.
    
    Returns
    -------
    listing : `str`
    """
    style_ban = STYLE_BAN
    style_kick = STYLE_KICK
    style_mute = STYLE_MUTE
    style_all = STYLE_ALL
    
    if sort_by == TYPE_BAN:
        style_ban = STYLE_FOCUS
    elif sort_by == TYPE_KICK:
        style_kick = STYLE_FOCUS
    elif sort_by == TYPE_MUTE:
        style_mute = STYLE_FOCUS
    else:
        style_all = STYLE_FOCUS
    
    result_parts = ['```']
    
    if top_list:
        result_parts.append('ansi\n')
        index_adjust = get_integer_length((page - 1) * PAGE_SIZE + len(top_list))
        all_adjust = max(get_integer_length(max(item[1].all for item in top_list)), len(NAME_ALL))
        ban_adjust = max(get_integer_length(max(item[1].ban for item in top_list)), len(NAME_BAN))
        kick_adjust = max(get_integer_length(max(item[1].kick for item in top_list)), len(NAME_KICK))
        mute_adjust = max(get_integer_length(max(item[1].mute for item in top_list)), len(NAME_MUTE))
        
        result_parts.append(' ' * index_adjust)
        result_parts.append('   ')
        result_parts.append(style_all)
        result_parts.append(NAME_ALL_HEADER.rjust(all_adjust))
        result_parts.append(' ')
        result_parts.append(style_ban)
        result_parts.append(NAME_BAN_HEADER.rjust(ban_adjust))
        result_parts.append(' ')
        result_parts.append(style_kick)
        result_parts.append(NAME_KICK_HEADER.rjust(kick_adjust))
        result_parts.append(' ')
        result_parts.append(style_mute)
        result_parts.append(NAME_MUTE_HEADER.rjust(mute_adjust))
        result_parts.append('\n')
        result_parts.append(STYLE_NONE)
        
        for index, (user, counter) in enumerate(top_list, 1 + (page - 1 ) * PAGE_SIZE):
            result_parts.append(str(index).rjust(index_adjust))
            result_parts.append('.: ')
            result_parts.append(style_all)
            result_parts.append(str(counter.all).rjust(all_adjust))
            result_parts.append(' ')
            result_parts.append(style_ban)
            result_parts.append(str(counter.ban).rjust(ban_adjust))
            result_parts.append(' ')
            result_parts.append(style_kick)
            result_parts.append(str(counter.kick).rjust(kick_adjust))
            result_parts.append(' ')
            result_parts.append(style_mute)
            result_parts.append(str(counter.mute).rjust(mute_adjust))
            result_parts.append(STYLE_NONE)
            result_parts.append(' ')
            result_parts.append(user.full_name)
            result_parts.append('\n')
    else:
        result_parts.append('\n*no result*\n')
    
    result_parts.append('```')
    return ''.join(result_parts)


def build_top_list_response(top_list, sort_by, days, page):
    """
    Builds the top-list response
    
    Parameters
    ----------
    top_list : `list` of `tuple` (``ClientUserBase``, ``ActionCounter``)
        Top list to show.
    sort_by : `int`
        The actions' identifier to sort by.
    page : `str`
        The page to show.
    page : `int`
        The page to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    embed = Embed(
        '**Mod top-list**',
        build_top_list_listing(top_list, sort_by, page),
    ).add_field(
        'Sorted by',
        (
            f'```\n'
            f'{TYPE_TO_NAME.get(sort_by, NAME_ALL)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Days',
        (
            f'```\n'
            f'{days}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Page',
        (
            f'```\n'
            f'{page}\n'
            f'```'
        ),
        inline = True,
    )
    
    if page == PAGE_MIN:
        button_back = BUTTON_BACK__DISABLED
    else:
        button_back = Button(
            f'Page {page - 1}',
            EMOJI_BACK,
            custom_id = f'mod.top_list.page.{page - 1};s={sort_by};d={days}',
        )
    
    if page == PAGE_MAX:
        button_next = BUTTON_NEXT_DISABLED
    else:
        button_next = Button(
            f'Page {page + 1}',
            EMOJI_NEXT,
            custom_id = f'mod.top_list.page.{page + 1};s={sort_by};d={days}',
        )
    
    components = Row(button_back, button_next, BUTTON_CLOSE)
    
    return InteractionResponse(
        embed = embed,
        components = components,
    )


def check_required_top_list_permissions(client, event, guild):
    """
    Checks whether the user and the client has enough permissions to invoke the `top-list` command.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild to request the actions at.
    """
    check_required_permissions_only_guild(guild)
    check_required_permissions_only_user(event, REQUIRED_PERMISSIONS_USER_VALUE, REQUIRED_PERMISSIONS_USER_NAME)
    check_required_permissions_only_client(
        client, guild, REQUIRED_PERMISSIONS_CLIENT_VALUE, REQUIRED_PERMISSIONS_CLIENT_NAME
    )


async def top_list_command(
    client,
    event,
    sort_by : (TYPES, 'Specific action type to sort by.') = TYPE_ALL,
    days : P(int, 'The days to get.', min_value = DAYS_MIN, max_value = DAYS_MAX) = DAYS_MAX,
    page : P(int, 'Page to get..', min_value = PAGE_MIN, max_value = PAGE_MAX) = PAGE_MIN,
):
    """
    Shows mod top-list.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sort_by : `int` = `TYPE_ALL`, Optional
        The actions' identifier to sort by.
    days : `int` = `DAYS_MAX`, Optional
        The days to request.
    page : `int` = `PAGE_MIN`, Optional
        The page to show.
    
    Yields
    ------
    acknowledge / response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    check_required_top_list_permissions(client, event, guild)
    yield
    top_list = await request_top_list(client, guild, sort_by, days, page)
    yield build_top_list_response(top_list, sort_by, days, page)


async def top_list_command_component_close(client, event):
    """
    Deletes the top-list message if the user has enough permissions.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    permissions = event.user_permissions
    if (
        permissions.can_manage_messages or
        permissions & REQUIRED_PERMISSIONS_USER_VALUE == REQUIRED_PERMISSIONS_USER_VALUE
    ):
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


async def top_list_command_component_page(client, event, page, sort_by, days):
    """
    Changes the page of the-top message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    page : `str`
        The page to show. Later converted to `int`.
    sort_by : `str`
        The actions' identifier to sort by. Later converted to `int`.
    days : `str`
        The days to request. Later converted to `int`.
    
    Yields
    ------
    acknowledge / response : `None`, ``InteractionResponse``
    """
    page = int(page)
    sort_by = int(sort_by)
    days = int(days)
    
    guild = event.guild
    check_required_top_list_permissions(client, event, guild)
    yield
    top_list = await request_top_list(client, guild, sort_by, days, page)
    yield build_top_list_response(top_list, sort_by, days, page)
