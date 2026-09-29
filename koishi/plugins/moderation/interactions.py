__all__ = ()

from hata import ClientUserBase, DiscordException, ERROR_CODES, GuildFeature
from hata.ext.slash import P

from ...bot_utils.user_getter import get_user
from ...bots import FEATURE_CLIENTS

from ..unit_core import parse_duration

from .component_building import (
    build_mod_ban_question_components, build_mod_other_completion_components, build_mod_other_form,
    build_mod_other_notification_components, build_mod_self_completion_components, build_mod_self_form,
    build_mod_top_list_components
)
from .constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_BAN_QUESTION, ACTION_TYPE_BAN_REASON_EDIT, ACTION_TYPE_INVITES_DISABLE,
    ACTION_TYPE_INVITES_ENABLE, ACTION_TYPE_KICK, ACTION_TYPE_MASK_BOUND_USER, ACTION_TYPE_MASK_PERMISSION_BAN_USERS,
    ACTION_TYPE_MASK_PERMISSION_KICK_USERS, ACTION_TYPE_MASK_PERMISSION_MANAGE_GUILD,
    ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS, ACTION_TYPE_MUTE, ACTION_TYPE_NONE, ACTION_TYPE_TOP_LIST_CLIENT,
    ACTION_TYPE_TOP_LIST_USER, ACTION_TYPE_UN_BAN, ACTION_TYPE_UN_MUTE, ERROR_MESSAGE_FORBIDDEN_FOR_BOOSTERS,
    ERROR_MESSAGE_GUILD_ONLY, ERROR_MESSAGE_INVALID_DAYS, ERROR_MESSAGE_INVALID_PAGE, ERROR_MESSAGE_INVALID_SORT_BY,
    ERROR_MESSAGE_INVITES_DISABLED, ERROR_MESSAGE_INVITES_ENABLED, ERROR_MESSAGE_MUTE_0_SECOND,
    ERROR_MESSAGE_NO_USER_SELECTED, ERROR_MESSAGE_PERMISSION_CHANGE, ERROR_MESSAGE_USER_LEFT_MEANWHILE,
    NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE, NOTIFICATION_RESULT_STATE_FAILURE_DMS_CLOSED,
    NOTIFICATION_RESULT_STATE_SUCCESS, PERMISSIONS_MASK_ADMINISTRATOR, PERMISSIONS_MASK_BAN, PERMISSIONS_MASK_KICK,
    PERMISSIONS_MASK_MODERATE_USERS, PERMISSIONS_MASK_TOP_LIST_CLIENT, PERMISSIONS_MASK_TOP_LIST_USER,
    PERMISSIONS_MASK_VIEW_AUDIT_LOGS, PERMISSION_MASK_MANAGE_GUILD, REASON_PATTERN, TOP_LIST_NAME_ALL,
    TOP_LIST_NAME_BAN, TOP_LIST_NAME_KICK, TOP_LIST_NAME_MUTE, TOP_LIST_OPTION_DAYS_MAX, TOP_LIST_OPTION_DAYS_MIN,
    TOP_LIST_OPTION_PAGE_MAX, TOP_LIST_OPTION_PAGE_MIN
)
from .content_building import (
    produce_error_message_missing_permission, produce_error_message_mod_other_need_higher_role_than,
    produce_error_message_mod_self_need_higher_role_than, produce_user_banned
)
from .custom_ids import (
    CUSTOM_ID_DELETE_MESSAGE_DURATION, CUSTOM_ID_DURATION, CUSTOM_ID_MOD_OTHER_PATTERN, CUSTOM_ID_MOD_SELF_PATTERN,
    CUSTOM_ID_MOD_TOP_LIST_CLOSE_PATTERN, CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_PATTERN,
    CUSTOM_ID_NOTIFY_USER, CUSTOM_ID_REASON, CUSTOM_ID_USERS
)
from .easter_eggs import should_show_nazrin, should_show_orin
from .helpers import (
    build_reason, iter_select_client_with_shared_guild, parse_boolean_select_values, process_reason,
    select_client_with_permission, try_notify_user
)
from .top_list_queries import request_top_list


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED,
    ],
)
async def handle_dummy():
    """
    handles a component interaction that should not happen.
    """
    pass


COMMAND_MODERATE_OTHER = FEATURE_CLIENTS.interactions(
    None,
    name = 'mod',
    description = 'Moderate users.',
    integration_context_types = ['guild'],
    is_global = True,
)

async def mod_other_common(
    client,
    interaction_event,
    action_type,
    target,
):
    """
    Common function to moderate an other user. Well, generally not self.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionNEvent``
        The received interaction event.
    
    action_type : `int`
        Action's type to execute.
    
    target : ``None | ClientUserBase``
        Target user if any.
    """
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        if action_type & ACTION_TYPE_MASK_PERMISSION_BAN_USERS:
            permission_mask = PERMISSIONS_MASK_BAN
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS:
            permission_mask = PERMISSIONS_MASK_MODERATE_USERS
        elif action_type & ACTION_TYPE_MASK_PERMISSION_KICK_USERS:
            permission_mask = PERMISSIONS_MASK_KICK
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MANAGE_GUILD:
            permission_mask = PERMISSION_MASK_MANAGE_GUILD
        else:
            permission_mask = PERMISSIONS_MASK_ADMINISTRATOR
            
        user = interaction_event.user
        if (guild.permissions_for(user) & permission_mask) != permission_mask:
            error_message = ''.join([*produce_error_message_missing_permission(action_type, True)])
            break
        
        selected_client = select_client_with_permission(client, guild, permission_mask)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(action_type, False)])
            break
        
        if (target is not None):
            if not user.has_higher_role_than_at(target, guild):
                error_message = ''.join([
                    *produce_error_message_mod_other_need_higher_role_than(action_type, True, (target,), guild.id)
                ])
                break
            
            if not selected_client.has_higher_role_than_at(target, guild):
                error_message = ''.join([
                    *produce_error_message_mod_other_need_higher_role_than(action_type, False, (target,), guild.id)
                ])
                break
        
        reason_default = None
        
        if (action_type == ACTION_TYPE_BAN_REASON_EDIT):
            if (target is not None):
                try:
                    ban_entry = await selected_client.guild_ban_get(guild, target)
                except DiscordException as err:
                    if err.code != ERROR_CODES.unknown_ban:
                        raise
                    
                    error_message = ''.join([*produce_user_banned(user, guild.id, False)])
                    break
                
                reason_default = ban_entry.reason
                if (reason_default is not None):
                    match = REASON_PATTERN.fullmatch(reason_default)
                    if (match is not None):
                        reason_default = match.group(1)
        
        elif (action_type == ACTION_TYPE_INVITES_DISABLE):
            if guild.has_feature(GuildFeature.invites_disabled):
                error_message = ERROR_MESSAGE_INVITES_DISABLED
                break
        
        elif (action_type == ACTION_TYPE_INVITES_ENABLE):
            if not guild.has_feature(GuildFeature.invites_disabled):
                error_message = ERROR_MESSAGE_INVITES_ENABLED
                break
        
        await client.interaction_form_send(
            interaction_event,
            build_mod_other_form(action_type, target, guild, reason_default, 3600, 3600),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'ban')
async def command_mod_other_ban(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to ban?') = None,
):
    """
    Bans someone out of the guild. You must have ban users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``None | ClientUserBase`` = `None`, Optional
        The user to ban.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_BAN,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'un-ban')
async def command_mod_other_un_ban(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to ban?'),
):
    """
    Un-bans someone out of the guild. You must have ban users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``ClientUserBase``
        The user to un-ban.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_UN_BAN,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'ban-reason-edit')
async def command_mod_other_ban_reason_edit(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who\'s ban reason to edit?'),
):
    """
    Edits someone's ban reason. You must have ban users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : `` ClientUserBase``
        The user to edit their ban reason of..
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_BAN_REASON_EDIT,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'mute')
async def command_mod_other_mute(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to mute?') = None,
):
    """
    Mute someone in the guild. You must have moderate users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``None | ClientUserBase`` = `None`, Optional (Keyword only)
        The user to mute.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_MUTE,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'un-mute')
async def command_mod_other_un_mute(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to un-mute?') = None,
):
    """
    Un-mutes someone in the guild. You must have moderate users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``None | ClientUserBase`` = `None`, Optional (Keyword only)
        The user to un-mute.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_UN_MUTE,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'kick')
async def command_mod_other_kick(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to kick?') = None,
):
    """
    Kicks someone out of the guild. You must have kick users permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``None | ClientUserBase`` = `None`, Optional
        The user to kick.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_KICK,
        target,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'invites-disable')
async def command_mod_other_invites_disable(
    client,
    interaction_event,
):
    """
    Disables the invites of the guild. YOu must have manage guild permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_INVITES_DISABLE,
        None,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'invites-enable')
async def command_mod_other_invites_enable(
    client,
    interaction_event,
):
    """
    Disables the invites of the guild. YOu must have manage guild permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await mod_other_common(
        client,
        interaction_event,
        ACTION_TYPE_INVITES_ENABLE,
        None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MOD_OTHER_PATTERN, target = 'form')
async def handle_mod_other_common(
    client,
    interaction_event,
    action_type,
    target_user_id,
    *,
    targets : CUSTOM_ID_USERS = None,
    reason : CUSTOM_ID_REASON = None,
    notify_user : CUSTOM_ID_NOTIFY_USER = None,
    delete_message_duration : CUSTOM_ID_DELETE_MESSAGE_DURATION = None,
    duration : CUSTOM_ID_DURATION = None,
):
    """
    handles a mod other interaction.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    action_type : `str`
        Action type a string representing a hexadecimal integer.
    
    target_user_id : `str`
        The single user's identifier, as string representing a hexadecimal integer.
    
    targets : ``None | ClientUserBase`` = `None`, Optional (Keyword only)
        The targeted users if any.
    
    reason : `None | str` = `None`, Optional (Keyword only)
        Ban reason if any.
    
    notify_user : `None | tuple<str>` = `None, Optional (Keyword only)
        Whether to notify the user.
    
    delete_message_duration : `None | str` = `None`, Optional (Keyword only)
        How old messages to delete.
    
    duration : `None | str` = `None`, Optional (Keyword only)
        Mute duration.
    """
    try:
        target_user_id = int(target_user_id, 16)
        action_type = int(action_type, 16)
    except ValueError:
        return
    
    reason = process_reason(reason)
    notify_user = parse_boolean_select_values(notify_user, False)
    delete_message_duration = (
        0 if delete_message_duration is None else min(604800, parse_duration(delete_message_duration))
    )
    duration = 0 if duration is None else min(2419200, parse_duration(duration))
    
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
        wait = False,
    )
    
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        if action_type & ACTION_TYPE_MASK_BOUND_USER:
            if target_user_id:
                target = await get_user(target_user_id)
                targets = (target,)
            
            elif targets is None:
                error_message = ERROR_MESSAGE_NO_USER_SELECTED
                break
        
        if action_type & ACTION_TYPE_MASK_PERMISSION_BAN_USERS:
            permission_mask = PERMISSIONS_MASK_BAN
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS:
            permission_mask = PERMISSIONS_MASK_MODERATE_USERS
        elif action_type & ACTION_TYPE_MASK_PERMISSION_KICK_USERS:
            permission_mask = PERMISSIONS_MASK_KICK
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MANAGE_GUILD:
            permission_mask = PERMISSION_MASK_MANAGE_GUILD
        else:
            permission_mask = PERMISSIONS_MASK_ADMINISTRATOR
        
        user = interaction_event.user
        if (guild.permissions_for(user) & permission_mask) != permission_mask:
            error_message = ''.join([*produce_error_message_missing_permission(action_type, True)])
            break
        
        selected_client = select_client_with_permission(client, guild, permission_mask)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(action_type, False)])
            break
        
        if (targets is not None):
            failing = None
            for target in targets:
                if not user.has_higher_role_than_at(target, guild):
                    if failing is None:
                        failing = []
                    failing.append(target)
            
            if (failing is not None):
                error_message = ''.join([
                    *produce_error_message_mod_other_need_higher_role_than(action_type, True, tuple(failing), guild.id)
                ])
                failing = None
                break
            
            failing = None
            for target in targets:
                if not selected_client.has_higher_role_than_at(target, guild):
                    if failing is None:
                        failing = []
                    failing.append(target)
            
            if (failing is not None):
                error_message = ''.join([
                    *produce_error_message_mod_other_need_higher_role_than(action_type, False, tuple(failing), guild.id)
                ])
                failing = None
                break
        
        if notify_user:
            notification_components = build_mod_other_notification_components(action_type, guild, reason, duration)
            for target in targets:
                for notifier_client in iter_select_client_with_shared_guild(user):
                    notification_result_state = await try_notify_user(
                        notifier_client,
                        target,
                        notification_components,
                    )
                    if notification_result_state == NOTIFICATION_RESULT_STATE_SUCCESS:
                        break
                    
                    if notification_result_state == NOTIFICATION_RESULT_STATE_FAILURE_DMS_CLOSED:
                        continue
                    
                    # Bad server connection, if this fails the whole command will fail along the line.
                    if notification_result_state == NOTIFICATION_RESULT_STATE_FAILURE_CONNECTION_OR_SERVER_ISSUE:
                        return
        
        built_reason = build_reason(user, guild.id, reason)
        if (action_type == ACTION_TYPE_BAN):
            for target in targets:
                await selected_client.guild_ban_add(
                    guild,
                    target,
                    delete_message_duration = delete_message_duration,
                    reason = built_reason,
                )
        
        elif (action_type == ACTION_TYPE_UN_BAN):
            for target in targets:
                try:
                    await selected_client.guild_ban_delete(
                        guild,
                        target,
                        reason = built_reason,
                    )
                except DiscordException as exception:
                    if exception.code != ERROR_CODES.unknown_ban:
                        raise
        
        elif (action_type == ACTION_TYPE_BAN_REASON_EDIT):
            for target in targets:
                try:
                    await selected_client.guild_ban_delete(
                        guild,
                        target,
                        reason = built_reason,
                    )
                except DiscordException as exception:
                    if exception.code != ERROR_CODES.unknown_ban:
                        raise
                
                await selected_client.guild_ban_add(
                    guild,
                    target,
                    delete_message_duration = delete_message_duration,
                    reason = built_reason,
                )
        
        elif (action_type == ACTION_TYPE_MUTE):
            if not duration:
                error_message = ERROR_MESSAGE_MUTE_0_SECOND
                break
            
            error_message = None
            for target in targets:
                try:
                    await selected_client.user_guild_profile_edit(
                        guild,
                        target,
                        timeout_duration = duration,
                        reason = built_reason,
                    )
                except DiscordException as exception:
                    if exception.code == ERROR_CODES.unknown_member:
                        error_message = ERROR_MESSAGE_USER_LEFT_MEANWHILE
                        break
                    
                    if exception.code == ERROR_CODES.missing_permissions:
                        error_message = ERROR_MESSAGE_PERMISSION_CHANGE
                        break
                    
                    raise
            
            if (error_message is not None):
                break
        
        elif (action_type == ACTION_TYPE_UN_MUTE):
            error_message = None
            for target in targets:
                try:
                    await selected_client.user_guild_profile_edit(
                        guild,
                        target,
                        timeout_duration = 0,
                        reason = built_reason,
                    )
                except DiscordException as exception:
                    if exception.code == ERROR_CODES.unknown_member:
                        error_message = ERROR_MESSAGE_USER_LEFT_MEANWHILE
                        break
                    
                    if exception.code == ERROR_CODES.missing_permissions:
                        error_message = ERROR_MESSAGE_PERMISSION_CHANGE
                        break
                    
                    raise
            
            if (error_message is not None):
                break
        
        elif (action_type == ACTION_TYPE_KICK):
            for target in targets:
                await selected_client.guild_user_delete(
                    guild,
                    target,
                    reason = built_reason,
                )
        
        elif (action_type == ACTION_TYPE_INVITES_DISABLE):
            if guild.has_feature(GuildFeature.invites_disabled):
                error_message = ERROR_MESSAGE_INVITES_DISABLED
                break
            
            await selected_client.guild_edit(
                guild,
                features = [*guild.iter_features(), GuildFeature.invites_disabled],
                reason = reason,
            )
        
        elif (action_type == ACTION_TYPE_INVITES_ENABLE):
            if not guild.has_feature(GuildFeature.invites_disabled):
                error_message = ERROR_MESSAGE_INVITES_ENABLED
                break
            
            await selected_client.guild_edit(
                guild,
                features = [
                    feature for feature in guild.iter_features() if feature is not GuildFeature.invites_disabled
                ],
                reason = reason,
            )
        
        else:
            # HUHH
            pass
        
        if (action_type == ACTION_TYPE_BAN) or (action_type == ACTION_TYPE_KICK):
            selected_client = select_client_with_permission(client, guild, PERMISSIONS_MASK_VIEW_AUDIT_LOGS)
            if selected_client is None:
                easter_egg_mode = False
            else:
                easter_egg_mode = await should_show_orin(selected_client, guild, user)
        
        elif (action_type == ACTION_TYPE_MUTE):
            easter_egg_mode = should_show_nazrin(duration)
        
        else:
            easter_egg_mode = False
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_mod_other_completion_components(
                action_type, targets, guild, reason, notify_user, delete_message_duration, duration, easter_egg_mode
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )



@COMMAND_MODERATE_OTHER.interactions(name = 'is-banned')
async def command_mod_other_ban_question(
    client,
    interaction_event,
    target : (ClientUserBase, 'Who to check?'),
):
    """
    Are they banned already?
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``ClientUserBase``
        The user to check.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        user = interaction_event.user
        if (guild.permissions_for(user) & PERMISSIONS_MASK_TOP_LIST_USER) != PERMISSIONS_MASK_TOP_LIST_USER:
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_BAN_QUESTION, True)])
            break
        
        selected_client = select_client_with_permission(client, guild, PERMISSIONS_MASK_TOP_LIST_CLIENT)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_BAN_QUESTION, False)])
            break
    
        try:
            ban_entry = await selected_client.guild_ban_get(guild, target)
        except DiscordException as err:
            if err.code != ERROR_CODES.unknown_ban:
                raise
            
            banned = False
            reason = None
        else:
            banned = True
            reason = ban_entry.reason
            if (reason is not None):
                match = REASON_PATTERN.fullmatch(reason)
                if (match is not None):
                    reason = match.group(1)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_mod_ban_question_components(target, guild.id, banned, reason)
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )


@COMMAND_MODERATE_OTHER.interactions(name = 'top-list')
async def command_mod_other_top_list(
    client,
    interaction_event,
    sort_by : (
        [
            (TOP_LIST_NAME_ALL, ACTION_TYPE_NONE),
            (TOP_LIST_NAME_BAN, ACTION_TYPE_BAN),
            (TOP_LIST_NAME_KICK, ACTION_TYPE_KICK),
            (TOP_LIST_NAME_MUTE, ACTION_TYPE_MUTE),
        ],
        'Specific action type to sort by.',
    ) = ACTION_TYPE_NONE,
    days : P(
        int,
        'The days to get.',
        min_value = TOP_LIST_OPTION_DAYS_MIN,
        max_value = TOP_LIST_OPTION_DAYS_MAX,
    ) = TOP_LIST_OPTION_DAYS_MAX,
    page : P(
        int,
        'Page to get..',
        min_value = TOP_LIST_OPTION_PAGE_MIN,
        max_value = TOP_LIST_OPTION_PAGE_MAX,
    ) = TOP_LIST_OPTION_PAGE_MIN,
):
    """
    Shows mod top-list.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sort_by : `int` = `TYPE_ALL`, Optional
        The actions' identifier to sort by.
    
    days : `int` = `DAYS_MAX`, Optional
        The days to request.
    
    page : `int` = `PAGE_MIN`, Optional
        The page to show. (1 based.)
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        if (
            (sort_by != ACTION_TYPE_NONE) and
            (sort_by != ACTION_TYPE_BAN) and
            (sort_by != ACTION_TYPE_KICK) and
            (sort_by != ACTION_TYPE_MUTE)
        ):
            error_message = ERROR_MESSAGE_INVALID_SORT_BY
            break
        
        if (days < TOP_LIST_OPTION_DAYS_MIN) or (days > TOP_LIST_OPTION_DAYS_MAX):
            error_message = ERROR_MESSAGE_INVALID_DAYS
            break
        
        if (page < TOP_LIST_OPTION_PAGE_MIN) or (page > TOP_LIST_OPTION_PAGE_MAX):
            error_message = ERROR_MESSAGE_INVALID_PAGE
            break
        
        page_index = page - 1
        
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        user = interaction_event.user
        if (guild.permissions_for(user) & PERMISSIONS_MASK_TOP_LIST_USER) != PERMISSIONS_MASK_TOP_LIST_USER:
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_TOP_LIST_USER, True)])
            break
        
        selected_client = select_client_with_permission(client, guild, PERMISSIONS_MASK_TOP_LIST_CLIENT)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_TOP_LIST_CLIENT, False)])
            break
        
        entries = await request_top_list(selected_client, guild, sort_by, days)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_mod_top_list_components(user.id, guild, page_index, entries, sort_by, days)
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_PATTERN)
async def handle_mod_other_top_list_page(
    client,
    interaction_event,
    user_id,
    page_index,
    sort_by,
    days,
):
    """
    Handles mod top-list page change interaction
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page to show as a string representing a hexadecimal integer.
    
    sort_by : `str`
        The actions' identifier to sort by as a string representing a hexadecimal integer.
    
    days : `str`
        The days to request as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        sort_by = int(sort_by, 16)
        days = int(days, 16)
    except KeyError:
        return
    
    user = interaction_event.user
    if user_id != user.id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        if (
            (sort_by != ACTION_TYPE_NONE) and
            (sort_by != ACTION_TYPE_BAN) and
            (sort_by != ACTION_TYPE_KICK) and
            (sort_by != ACTION_TYPE_MUTE)
        ):
            sort_by = ACTION_TYPE_NONE
        
        if days < TOP_LIST_OPTION_DAYS_MIN:
            days = TOP_LIST_OPTION_DAYS_MIN
        elif days > TOP_LIST_OPTION_DAYS_MAX:
            days = TOP_LIST_OPTION_DAYS_MAX
        
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        if (guild.permissions_for(user) & PERMISSIONS_MASK_TOP_LIST_USER) != PERMISSIONS_MASK_TOP_LIST_USER:
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_TOP_LIST_USER, True)])
            break
        
        selected_client = select_client_with_permission(client, guild, PERMISSIONS_MASK_TOP_LIST_CLIENT)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(ACTION_TYPE_TOP_LIST_CLIENT, False)])
            break
        
        entries = await request_top_list(selected_client, guild, sort_by, days)
        
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_mod_top_list_components(user.id, guild, page_index, entries, sort_by, days)
        )
        return
    
    await client.interaction_followup_message_create(
        client,
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MOD_TOP_LIST_CLOSE_PATTERN)
async def handle_mod_other_top_list_close(
    client,
    interaction_event,
    user_id,
):
    """
    Handles mod top-list close interaction
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
    except KeyError:
        return
    
    user = interaction_event.user
    if user_id != user.id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        True,
    )
    
    await client.interaction_response_message_delete(
        interaction_event,
    )


COMMAND_MODERATE_SELF = FEATURE_CLIENTS.interactions(
    None,
    name = 'mod-self',
    description = 'Moderate yourself!!!',
    integration_context_types = ['guild'],
    is_global = True,
)


async def mod_self_common(
    client,
    interaction_event,
    action_type,
):
    """
    Common function to moderate an oneself. Well, generally not self.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionNEvent``
        The received interaction event.
    
    action_type : `int`
        Action's type to execute.
    """
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        if action_type & ACTION_TYPE_MASK_PERMISSION_BAN_USERS:
            permission_mask = PERMISSIONS_MASK_BAN
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS:
            permission_mask = PERMISSIONS_MASK_MODERATE_USERS
        elif action_type & ACTION_TYPE_MASK_PERMISSION_KICK_USERS:
            permission_mask = PERMISSIONS_MASK_KICK
        else:
            permission_mask = PERMISSIONS_MASK_ADMINISTRATOR
        
        selected_client = select_client_with_permission(client, guild, permission_mask)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(action_type, False)])
            break
        
        user = interaction_event.user
        if not selected_client.has_higher_role_than_at(user, guild):
            error_message = ''.join([
                *produce_error_message_mod_self_need_higher_role_than(action_type)
            ])
            break
        
        if (action_type == ACTION_TYPE_BAN) or (action_type == PERMISSIONS_MASK_KICK):
            if user.is_boosting(guild.id):
                error_message = ERROR_MESSAGE_FORBIDDEN_FOR_BOOSTERS
                break
        
        await client.interaction_form_send(
            interaction_event,
            build_mod_self_form(action_type, guild, 3600),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@COMMAND_MODERATE_SELF.interactions(name = 'ban')
async def command_mod_self_ban(
    client,
    interaction_event,
):
    """
    Ban yourself!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await mod_self_common(
        client,
        interaction_event,
        ACTION_TYPE_BAN,
    )


@COMMAND_MODERATE_SELF.interactions(name = 'mute')
async def command_mod_self_mute(
    client,
    interaction_event,
):
    """
    Mute yourself!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await mod_self_common(
        client,
        interaction_event,
        ACTION_TYPE_MUTE,
    )


@COMMAND_MODERATE_SELF.interactions(name = 'kick')
async def command_mod_self_kick(
    client,
    interaction_event,
):
    """
    Kick yourself!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await mod_self_common(
        client,
        interaction_event,
        ACTION_TYPE_KICK,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MOD_SELF_PATTERN, target = 'form')
async def handle_mod_self_common(
    client,
    interaction_event,
    action_type,
    *,
    reason : CUSTOM_ID_REASON = None,
    duration : CUSTOM_ID_DURATION = None,
):
    """
    handles a mod self interaction.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    action_type : `str`
        Action type as a string representing a hexadecimal integer.
    
    reason : `None | str` = `None`, Optional (Keyword only)
        Ban reason if any.
    
    duration : `None | str` = `None`, Optional (Keyword only)
        Mute duration.
    """
    try:
        action_type = int(action_type, 16)
    except ValueError:
        return
    
    reason = process_reason(reason)
    duration = 0 if duration is None else min(2419200, parse_duration(duration))
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = ERROR_MESSAGE_GUILD_ONLY
            break
        
        if action_type & ACTION_TYPE_MASK_PERMISSION_BAN_USERS:
            permission_mask = PERMISSIONS_MASK_BAN
        elif action_type & ACTION_TYPE_MASK_PERMISSION_MODERATE_USERS:
            permission_mask = PERMISSIONS_MASK_MODERATE_USERS
        elif action_type & ACTION_TYPE_MASK_PERMISSION_KICK_USERS:
            permission_mask = PERMISSIONS_MASK_KICK
        else:
            permission_mask = PERMISSIONS_MASK_ADMINISTRATOR
        
        selected_client = select_client_with_permission(client, guild, permission_mask)
        if (selected_client is None):
            error_message = ''.join([*produce_error_message_missing_permission(action_type, False)])
            break
        
        user = interaction_event.user
        if not selected_client.has_higher_role_than_at(user, guild):
            error_message = ''.join([
                *produce_error_message_mod_self_need_higher_role_than(action_type)
            ])
            break
        
        if (action_type == ACTION_TYPE_BAN) or (action_type == PERMISSIONS_MASK_KICK):
            if user.is_boosting(guild.id):
                error_message = ERROR_MESSAGE_FORBIDDEN_FOR_BOOSTERS
                break
        
        built_reason = build_reason(user, guild.id, reason)
        if (action_type == ACTION_TYPE_BAN):
            await selected_client.guild_ban_add(
                guild,
                user,
                reason = built_reason,
            )

        elif (action_type == ACTION_TYPE_MUTE):
            if not duration:
                error_message = ERROR_MESSAGE_MUTE_0_SECOND
                break
            
            try:
                await selected_client.user_guild_profile_edit(
                    guild,
                    user,
                    timeout_duration = duration,
                    reason = built_reason,
                )
            except DiscordException as exception:
                if exception.code == ERROR_CODES.missing_permissions:
                    error_message = ERROR_MESSAGE_PERMISSION_CHANGE
                    break
        
                if exception.code != ERROR_CODES.unknown_member:
                    raise
        
        elif (action_type == ACTION_TYPE_KICK):
            await selected_client.guild_user_delete(
                guild,
                user,
                reason = built_reason,
            )
        
        else:
            # HUHH
            pass
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_mod_self_completion_components(
                action_type, user, guild.id, reason, duration
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
