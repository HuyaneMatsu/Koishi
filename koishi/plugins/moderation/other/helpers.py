__all__ = ()

from functools import partial as partial_func

from hata import DiscordException, ERROR_CODES, Embed, Permission
from hata.ext.slash import abort, wait_for_component_interaction

from ..shared_helpers import add_reason_field

from .constants import COMPONENT__CANCEL, COMPONENT__ROW


def check_required_permissions_only_guild(guild):
    """
    Checks whether the guild is not `None`.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild where the action would be executed.
    """
    if guild is None:
        abort('Guild only command.')


def check_required_permissions_only_user(event, required_permission, required_permissions_name):
    """
    Checks whether the user has the required permissions.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    required_permission : ``Permission``
        The required permissions to execute the action.
    required_permissions_name : `str`
       The name of the required permissions.
    """
    if (event.user_permissions & required_permission) != required_permission:
        abort(f'You must have {required_permissions_name} permission to use this command.')


def check_required_permissions_only_client(client, guild, required_permission, required_permissions_name):
    """
    Checks whether the client has the required permissions.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild where the action would be executed.
    required_permission : ``Permission``
        The required permissions to execute the action.
    required_permissions_name : `str`
       The name of the required permissions.
    """
    if (guild.cached_permissions_for(client) & required_permission) != required_permission:
        abort(f'{client.name_at(guild)} requires {required_permissions_name} permission for this action.')


def check_required_permissions_only(client, event, guild, required_permission, word_config):
    """
    Checks whether only the permissions requirements are met.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild where the action would be executed.
    required_permission : ``Permission``
        The required permissions to execute the action.
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    """
    check_required_permissions_only_guild(guild)
    check_required_permissions_only_user(event, required_permission, word_config.permission)
    check_required_permissions_only_client(client, guild, required_permission, word_config.permission)


def check_required_permissions(client, event, guild, user, required_permission, word_config):
    """
    Checks whether the permissions requirements are met to execute the action.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild where the action would be executed.
    user : ``ClientUserBase``
        The user in context.
    required_permission : ``Permission``
        The required permissions to execute the action.
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    """
    check_required_permissions_only(client, event, guild, required_permission, word_config)
    
    if not event.user.has_higher_role_than_at(user, guild):
        abort(f'You must have higher role than the person to be {word_config.to_be}.')
    
    if not client.has_higher_role_than_at(user, guild):
        abort(f'I must have higher role than the person to be {word_config.to_be}.')


def check_user(user, event):
    """
    Checks whether the given user and the event's user match.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The command's original invoker.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    allow : `bool`
    """
    return user is event.user


def build_action_completed_embed(user, guild_id, embed_builder, word_config, note, *position_parameters):
    """
    Builds an action done embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user on who the action was executed.
    
    guild_id : `int`
        The local guild's identifier.
    
    embed_builder : `FunctionType``
        Base embed builder.
    
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    
    note : `None | str`
        Note to set to the message.
    
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = embed_builder(
        user,
        'Hecatia yeah!',
        f'**{user.name_at(guild_id)}** has been {word_config.to_be}.',
        *position_parameters,
    )
    
    if (note is not None):
        embed.add_footer(note)
    
    return embed


def build_action_failed_embed(user, guild_id, embed_builder, word_config, note, *position_parameters):
    """
    Builds an action not done embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user on who the action was executed.
    
    guild_id : `int`
        The local guild's identifier.
    
    embed_builder : `FunctionType``
        Base embed builder.
    
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    
    note : `None | str`
        Note to set to the message.
    
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = embed_builder(
        user,
        'Oh snap..',
        f'Failed to {word_config.name!s} **{user.name_at(guild_id)}**.',
        *position_parameters,
    )
    
    if (note is not None):
        embed.add_footer(note)
    
    return embed


def build_cannot_regret_embed(user, guild_id, reason, action):
    """
    Builds a regret embed when the client detects that the respective user is not applicable for the actions.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `str`
        Regret-ban reason.
    
    action : `str`
        The action's name within its `-ed` form.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Denied',
        (
            f'You cannot regret {action} **{user.name_at(guild_id)}**.\n'
            f'Was the action different, or is it is already too late?!'
        )
    )
    
    add_reason_field(embed, reason)
    return embed


async def confirm_action(client, event, guild, user, embed_builder, word_config, *positional_parameters):
    """
    Sends a confirmation message and waits till the user confirms it. If the user confirmed the action returns the
    confirmation interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild where the action is being executed.
    user : ``User``
        The user in context.
    embed_builder : `FunctionType``
        Base embed builder.
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    component_interaction : ``None | InteractionEvent``
    """
    message = await client.interaction_followup_message_create(
        event,
        allowed_mentions = None,
        components = COMPONENT__ROW,
        embed = embed_builder(
            user,
            'Confirmation',
            (
                f'Are you sure to {word_config.name} **{user.name_at(event.guild_id)}** '
                f'{word_config.connector} **{guild.name}**?'
            ),
            *positional_parameters,
        ),
    )
    
    try:
        component_interaction = await wait_for_component_interaction(
            message, timeout = 300.0, check = partial_func(check_user, event.user)
        )
    except TimeoutError:
        # Edit the source message with the source interaction
        try:
            await client.interaction_response_message_edit(
                event,
                allowed_mentions = None,
                components = None,
                embed = embed_builder(
                    user,
                    'Timeout',
                    (
                        f'**{user.name_at(event.guild_id)}** was not {word_config.to_be} '
                        f'{word_config.connector} **{guild.name}**.'
                    ),
                    *positional_parameters,
                ),
            )
        except ConnectionError:
            pass
        
        except DiscordException as exception:
            if (
                (exception.status < 500) and
                (
                    exception.code not in (
                        ERROR_CODES.unknown_message, # message already deleted
                    )
                )
            ):
                raise
        
        return None
    
    if component_interaction.component % COMPONENT__CANCEL:
        # Edit the source message with the component interaction
        await client.interaction_component_message_edit(
            component_interaction,
            allowed_mentions = None,
            components = None,
            embed = embed_builder(
                user,
                'Cancelled',
                (
                    f'**{user.name_at(event.guild_id)}** was not {word_config.to_be} {word_config.connector} '
                    f'**{guild.name}**.'
                ),
                *positional_parameters,
            ),
        )
        return None
    
    # Acknowledge the event so we wont need to in the main command
    await client.interaction_component_acknowledge(component_interaction, False)
    
    return component_interaction


async def notify_user_action(client, guild, user, embed_builder, *position_parameters):
    """
    Notifies the user about the action in context.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild where the action is being executed.
    user : ``User``
        The user in context.
    embed_builder : `FunctionType``
        Base embed builder.
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    notify_note : `None`, `str`
        Notes about how the notification went.
    """
    # Ignore bot notifications.
    if user.bot:
        return
    
    try:
        channel = await client.channel_private_create(user)
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return # We cannot help no internet
        
        raise
    
    embed, components = embed_builder(guild, *position_parameters)
    try:
        await client.message_create(
            channel,
            embed = embed,
            components = components,
        )
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return # We cannot help no internet
        
        if isinstance(err, DiscordException) and (err.code == ERROR_CODES.cannot_message_user):
            return 'Notification cannot be delivered: user has DM disabled.'
        
        raise
