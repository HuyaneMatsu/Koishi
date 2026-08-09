__all__ = ()

from .constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_INVITES_DISABLE, ACTION_TYPE_INVITES_ENABLE,
    ACTION_TYPE_KICK, ACTION_TYPE_MASK_PERMISSION_BAN_KICK_MODERATE_USERS_VIEW_AUDIT_LOGS,
    ACTION_TYPE_MASK_PERMISSION_BAN_USERS, ACTION_TYPE_MASK_PERMISSION_KICK_USERS,
    ACTION_TYPE_MASK_PERMISSION_MANAGE_GUILD, ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS,
    ACTION_TYPE_MASK_PERMISSION_VIEW_AUDIT_LOGS, ACTION_TYPE_MASK_BOUND_GUILD, ACTION_TYPE_MASK_BOUND_USER,
    ACTION_TYPE_MASK_CONNECTOR_FROM, ACTION_TYPE_MASK_CONNECTOR_IN, ACTION_TYPE_MASK_CONNECTOR_OF, ACTION_TYPE_MUTE,
    ACTION_TYPE_UN_BAN, ACTION_TYPE_UN_MUTE, TOP_LIST_NAME_ALL, TOP_LIST_NAME_ALL_HEADER, TOP_LIST_NAME_BAN,
    TOP_LIST_NAME_BAN_HEADER, TOP_LIST_NAME_KICK, TOP_LIST_NAME_KICK_HEADER, TOP_LIST_NAME_MUTE,
    TOP_LIST_NAME_MUTE_HEADER, TOP_LIST_PAGE_SIZE, TOP_LIST_STYLE_ALL, TOP_LIST_STYLE_BAN, TOP_LIST_STYLE_FOCUS,
    TOP_LIST_STYLE_KICK, TOP_LIST_STYLE_MUTE, TOP_LIST_STYLE_NAME, TOP_LIST_STYLE_NUMBER
)
from .helpers import get_integer_length


def produce_user_listing(users, guild_id):
    """
    Produces user names separated by comma.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    users : ``tuple<ClientUserBase>``
        Users to produce their names of.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    index = 0
    length = len(users)
    while index < length:
        user = users[index]
        index += 1
        if index != 1:
            yield (' and ' if index == length else ', ')
        
        yield user.name_at(guild_id)


def produce_user_banned(user, guild_id, banned):
    """
    Produces user banned error message.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield user.name_at(guild_id)
    yield ' is '
    if not banned:
        yield '**NOT YET** '
    yield 'banned.'


def produce_error_message_missing_permission(action_type, user_side):
    """
    Produces error message describing missing permissions of the user.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_side : `bool`
        Whether the missing permission issue comes from the user's side.
    
    Yields
    ------
    part : `str`
    """
    yield ('You must have' if user_side else 'I require')
    yield ' '
    
    if action_type & ACTION_TYPE_MASK_PERMISSION_BAN_USERS:
        permission_name = 'ban users'
    elif action_type & ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS:
        permission_name = 'moderate users'
    elif action_type & ACTION_TYPE_MASK_PERMISSION_KICK_USERS:
        permission_name = 'kick users'
    elif action_type & ACTION_TYPE_MASK_PERMISSION_BAN_KICK_MODERATE_USERS_VIEW_AUDIT_LOGS:
        permission_name = 'ban, kick, moderate users and view audit logs'
    elif action_type & ACTION_TYPE_MASK_PERMISSION_VIEW_AUDIT_LOGS:
        permission_name = 'view audit logs'
    elif action_type & ACTION_TYPE_MASK_PERMISSION_MANAGE_GUILD:
        permission_name = 'manage guild'
    else:
        permission_name = 'administrator'
    yield permission_name
    
    yield ' permission to '
    yield ('use this command' if user_side else 'execute this action')
    yield '.'
    

def produce_error_message_mod_other_need_higher_role_than(action_type, user_side, targets, guild_id):
    """
    Produces error message for the scenario when the invoking user's highest role is lower than the targeted one's.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_side : `bool`
        Whether the lower role is coming from the user's side.
    
    targets : ``tuple<ClientUserBase>``
        The targeted users.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    -------
    part : `str`
    """
    yield ('You need to have' if user_side else 'I require')
    yield ' higher role than '
    yield from produce_user_listing(targets, guild_id)
    yield ' to '
    
    if action_type == ACTION_TYPE_BAN_REASON_EDIT:
        yield 'edit their ban reason'
    else:
        if (action_type == ACTION_TYPE_BAN):
            action_name = 'ban'
        elif (action_type == ACTION_TYPE_UN_BAN):
            action_name = 'un-ban'
        elif (action_type == ACTION_TYPE_MUTE):
            action_name = 'mute'
        elif (action_type == ACTION_TYPE_UN_MUTE):
            action_name = 'un-mute'
        elif (action_type == ACTION_TYPE_KICK):
            action_name = 'kick'
        else:
            action_name = 'peg'
        yield action_name
        yield ' them'
    
    yield '.'


def produce_error_message_mod_self_need_higher_role_than(action_type):
    """
    Produces an error message for a scenario when the client's highest role is lower than the user's.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    Yields
    -------
    part : `str`
    """
    yield 'I require higher role than you to '
    
    if (action_type == ACTION_TYPE_BAN):
        action_name = 'ban'
    elif (action_type == ACTION_TYPE_MUTE):
        action_name = 'mute'
    elif (action_type == ACTION_TYPE_KICK):
        action_name = 'kick'
    else:
        action_name = 'peg'
    yield action_name
    
    yield ' you.'


def produce_mod_other_form_description(action_type, target, guild):
    """
    Produces mod other form description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    target : ``None | ClientUserBase``
        The targeted user if any.
    
    guild : ``Guild``
        The local guild.
    
    Yields
    -------
    part : `str`
    """
    yield '### '
    if action_type & ACTION_TYPE_MASK_BOUND_GUILD:
        if (action_type == ACTION_TYPE_INVITES_DISABLE) or (action_type == ACTION_TYPE_INVITES_ENABLE):
            yield ('Disabling' if action_type == ACTION_TYPE_INVITES_DISABLE else 'Enabling')
            yield ' invites '
    
    elif action_type & ACTION_TYPE_MASK_BOUND_USER:
        if (action_type == ACTION_TYPE_BAN):
            action_name = 'Banning'
        elif (action_type == ACTION_TYPE_UN_BAN):
            action_name = 'Un-banning'
        elif (action_type == ACTION_TYPE_BAN_REASON_EDIT):
            action_name = 'Edit ban reason of'
        elif (action_type == ACTION_TYPE_MUTE):
            action_name = 'Muting'
        elif (action_type == ACTION_TYPE_UN_MUTE):
            action_name = 'Un-muting'
        elif (action_type == ACTION_TYPE_KICK):
            action_name = 'Kicking'
        else:
            action_name = 'Pegging'
        yield action_name
        
        yield ' '
        yield ('user(s)' if target is None else target.name_at(guild.id))
        yield ' '
    
    if action_type & ACTION_TYPE_MASK_CONNECTOR_FROM:
        connector = 'from'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_IN:
        connector = 'in'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_OF:
        connector = 'of'
    else:
        connector = 'in'
    yield connector
    
    yield ' '
    yield guild.name
    yield '.'


def produce_mod_self_form_description(action_type, guild):
    """
    Produces mod self form title.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    Yields
    -------
    part : `str`
    """
    yield '### '
    if (action_type == ACTION_TYPE_BAN):
        action_name = 'Banning'
    elif (action_type == ACTION_TYPE_MUTE):
        action_name = 'Muting'
    elif (action_type == ACTION_TYPE_KICK):
        action_name = 'Kicking'
    else:
        action_name = 'Pegging'
    yield action_name
    
    yield ' yourself '
    
    if action_type & ACTION_TYPE_MASK_CONNECTOR_FROM:
        connector = 'from'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_IN:
        connector = 'in'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_OF:
        connector = 'of'
    else:
        connector = 'in'
    yield connector
    
    yield ' '
    yield guild.name
    yield '.'


def produce_mod_other_notification_header(action_type, guild):
    """
    Produces mod other notification header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    Yields
    -------
    part : `str`
    """
    yield 'You have been '
    
    if (action_type == ACTION_TYPE_BAN):
        actioned_name = 'banned'
    elif (action_type == ACTION_TYPE_UN_BAN):
        actioned_name = 'un-banned'
    elif (action_type == ACTION_TYPE_MUTE):
        actioned_name = 'muted'
    elif (action_type == ACTION_TYPE_UN_MUTE):
        actioned_name = 'un-muted'
    elif (action_type == ACTION_TYPE_KICK):
        actioned_name = 'kicked'
    else:
        actioned_name = 'pegged'
    yield actioned_name
    
    yield ' '
    
    if action_type & ACTION_TYPE_MASK_CONNECTOR_FROM:
        connector = 'from'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_IN:
        connector = 'in'
    elif action_type & ACTION_TYPE_MASK_CONNECTOR_OF:
        connector = 'of'
    else:
        connector = 'in'
    yield connector
    
    yield ' '
    yield guild.name
    yield '.'


def produce_mod_other_completion_header(action_type, targets, guild):
    """
    Produces mod other action completion header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    targets : ``None | tuple<ClientUserBase>``
        Targeted users.
    
    guild : ``Guild``
        The local guild.
    
    Yields
    -------
    part : `str`
    """
    yield '### Hecatia Yeah!\n\n'
    
    if action_type & ACTION_TYPE_MASK_BOUND_GUILD:
        if (action_type == ACTION_TYPE_INVITES_DISABLE) or (action_type == ACTION_TYPE_INVITES_ENABLE):
            yield 'Invites of '
            yield guild.name
            yield ' have been '
            yield ('disabled' if action_type == ACTION_TYPE_INVITES_DISABLE else 'enabled')
    
    elif action_type & ACTION_TYPE_MASK_BOUND_USER:
        if action_type == ACTION_TYPE_BAN_REASON_EDIT:
            yield 'Ban reason of '
        
        yield from produce_user_listing(targets, guild.id)
        yield ' '
        yield ('has' if ((targets is None) or (len(targets) == 1)) else 'have')
        yield ' been '
        
        if (action_type == ACTION_TYPE_BAN):
            action_name = 'banned'
        elif (action_type == ACTION_TYPE_UN_BAN):
            action_name = 'un-banned'
        elif (action_type == ACTION_TYPE_BAN_REASON_EDIT):
            action_name = 'edited'
        elif (action_type == ACTION_TYPE_MUTE):
            action_name = 'muted'
        elif (action_type == ACTION_TYPE_UN_MUTE):
            action_name = 'un-muted'
        elif (action_type == ACTION_TYPE_KICK):
            action_name = 'kicked'
        else:
            action_name = 'pegged'
        yield action_name
    
    yield '!'


def produce_mod_self_completion_header(action_type, user, guild_id):
    """
    Produces mod other action completion header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    user : ``ClientUserBase``
        Targeted users.
    
    guild_id : ``Guild``
        The local guild's identifier.
    
    Yields
    -------
    part : `str`
    """
    yield '### Hecatia Yeah!\n\n'
    
    yield user.name_at(guild_id)
    yield ' have '
    
    if (action_type == ACTION_TYPE_BAN):
        action_name = 'banned'
    elif (action_type == ACTION_TYPE_MUTE):
        action_name = 'muted'
    elif (action_type == ACTION_TYPE_KICK):
        action_name = 'kicked'
    else:
        action_name = 'pegged'
    yield action_name
    
    yield ' themselves!'


def produce_top_list_header(guild, page_index, sort_by, days):
    """
    Produces top-list header-
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The local guild.
    
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    days : `int`
        The amount of days to request.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield guild.name
    yield '\'s mod top-list\n\nSort by: '
    
    if sort_by == ACTION_TYPE_BAN:
        sort_by_name = 'ban'
    elif sort_by == ACTION_TYPE_MUTE:
        sort_by_name = 'mute'
    elif sort_by == ACTION_TYPE_KICK:
        sort_by_name = 'kick'
    else:
        sort_by_name = 'none'
    yield sort_by_name
    
    yield '\nDays: '
    yield str(days)
    yield '\nPage: '
    yield str(page_index + 1)


def produce_top_list_content(page_index, entries, sort_by, guild_id):
    """
    Produces the top-list listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    entries : ``list<(ClientUserBase, ActionCounter)>``
        Top list entries.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    -------
    part : `str`
    """
    style_ban = TOP_LIST_STYLE_BAN
    style_kick = TOP_LIST_STYLE_KICK
    style_mute = TOP_LIST_STYLE_MUTE
    style_all = TOP_LIST_STYLE_ALL
    
    if sort_by == ACTION_TYPE_BAN:
        style_ban = TOP_LIST_STYLE_FOCUS
    elif sort_by == ACTION_TYPE_KICK:
        style_kick = TOP_LIST_STYLE_FOCUS
    elif sort_by == ACTION_TYPE_MUTE:
        style_mute = TOP_LIST_STYLE_FOCUS
    else:
        style_all = TOP_LIST_STYLE_FOCUS
    
    yield '```ansi\n'
    
    # Entries should be never empty, but make sure things are still displayed correctly.
    if entries:
        index_adjust = get_integer_length(page_index * TOP_LIST_PAGE_SIZE + 1 + len(entries))
        all_adjust = max(get_integer_length(max(item[1].all for item in entries)), len(TOP_LIST_NAME_ALL))
        ban_adjust = max(get_integer_length(max(item[1].ban for item in entries)), len(TOP_LIST_NAME_BAN))
        kick_adjust = max(get_integer_length(max(item[1].kick for item in entries)), len(TOP_LIST_NAME_KICK))
        mute_adjust = max(get_integer_length(max(item[1].mute for item in entries)), len(TOP_LIST_NAME_MUTE))
        
        yield ' ' * index_adjust
        yield '   '
        yield style_all
        yield TOP_LIST_NAME_ALL_HEADER.rjust(all_adjust)
        yield ' '
        yield style_ban
        yield TOP_LIST_NAME_BAN_HEADER.rjust(ban_adjust)
        yield ' '
        yield style_kick
        yield TOP_LIST_NAME_KICK_HEADER.rjust(kick_adjust)
        yield ' '
        yield style_mute
        yield TOP_LIST_NAME_MUTE_HEADER.rjust(mute_adjust)
        yield '\n'
        
        for index, (user, counter) in enumerate(entries, 1 + page_index * TOP_LIST_PAGE_SIZE):
            yield TOP_LIST_STYLE_NUMBER
            yield str(index).rjust(index_adjust)
            yield '.: '
            yield style_all
            yield str(counter.all).rjust(all_adjust)
            yield ' '
            yield style_ban
            yield str(counter.ban).rjust(ban_adjust)
            yield ' '
            yield style_kick
            yield str(counter.kick).rjust(kick_adjust)
            yield ' '
            yield style_mute
            yield str(counter.mute).rjust(mute_adjust)
            yield ' '
            yield TOP_LIST_STYLE_NAME
            yield user.name_at(guild_id)
            yield '\n'
    
    yield '```'
