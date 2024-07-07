__all__ = ()

from re import M as re_multiline, U as re_unicode, compile as re_compile

from hata import Client, DiscordException, ERROR_CODES, MessageType, Permission, USER_MENTION_RP

from ...bot_utils.multi_client_utils import get_first_client_with_message_create_permissions_from
from ...bots import FEATURE_CLIENTS

from ..blacklist_core import is_user_id_in_blacklist
from ..user_settings import get_one_user_settings, get_preferred_client_in_channel

from .action import COOLDOWN_HANDLER, create_response_content_and_embed, send_action_response_to
from .actions import ACTIONS


ACTIONS_BY_NAME = {}

for action in ACTIONS:
    for name in action.iter_names():
        ACTIONS_BY_NAME[name] = action

# cleanup
del action


MAX_ACTION_COMMAND_LENGTH = max(len(name) for name in ACTIONS_BY_NAME.keys())

ACTION_CONTENT_RP = re_compile(f'> .*?{USER_MENTION_RP.pattern}', re_multiline | re_unicode)
PERMISSION_MANAGE_MESSAGES = Permission().update_by_keys(manage_messages = True)
PERMISSION_IMAGES = Permission().update_by_keys(attach_files = True, embed_links = True)


def is_message_action_interaction(client, message):
    """
    Returns whether the message looks like an action interaction.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    message : ``Message``
        The message to check.
        
        > Note that this is the replied message.
    
    Returns
    -------
    is_message_action_interaction : `bool`
    """
    if message.author not in FEATURE_CLIENTS:
        return False
    
    message_type = message.type
    if message_type is MessageType.slash_command:
        interaction = message.interaction
        if (interaction is not None):
            interaction_name = interaction.name
            return interaction_name in ACTIONS_BY_NAME.keys() or interaction_name == 'action'
    
    # We do not receive nonce for requested or referenced messages, so we cannot match that reliable.
    # Try to match message by structure~
    elif (message_type is MessageType.inline_reply) or (message_type is MessageType.default):
        if (message.content is not None):
            embed = message.embed
            if (embed is not None):
                if (embed.title is None) and (embed.description is None) and (embed.image is not None):
                    return True
    
    return False


def get_intended_action(message):
    """
    Tries to get the intended action from the message's content.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
        
        > Note that this is the received message.
    
    Returns
    -------
    intended_action : `str`
    """
    content = message.content
    if content is None:
        return None
    
    starts_with_slash = content.startswith('/')
        
    if len(content) > (MAX_ACTION_COMMAND_LENGTH + starts_with_slash):
        return None
    
    # Remove slash if we start with it.
    if starts_with_slash:
        content = content[1:]
    
    content = content.casefold().replace(' ', '-').replace('_', '-')
    if content not in ACTIONS_BY_NAME.keys():
        return None
    
    return content


async def get_user_from_referenced_message(client, referenced_message):
    """
    Tries to get the user we want to interact with from the referenced message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    message : ``Message``
        The message to check.
        
        > Note that this is the replied message.
    
    Returns
    -------
    user : `None`, ``ClientUserBase``
    """
    content = referenced_message.content
    if content is None:
        return None
    
    match = ACTION_CONTENT_RP.match(content)
    if match is None:
        return None
    
    user_id = int(match.group(1))
    return await client.user_get(user_id)


@FEATURE_CLIENTS.events
async def message_create(client, message):
    """
    Handles a message create event.
    
    If the received message is a reply to an action interaction and its content is an action's name we try to 
    replace it with a new action interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    message : ``Message``
        The created message.
    """
    if client is not get_first_client_with_message_create_permissions_from(
        message.channel, FEATURE_CLIENTS, PERMISSION_MANAGE_MESSAGES
    ):
        return
    
    if message.author.bot or is_user_id_in_blacklist(message.author.id):
        return
    
    if message.type is not MessageType.inline_reply:
        return
    
    referenced_message = message.referenced_message
    if referenced_message is None:
        return
    
    if not is_message_action_interaction(client, referenced_message):
        return
    
    intended_action = get_intended_action(message)
    if (intended_action is None):
        return False
    
    target_user = await get_user_from_referenced_message(client, referenced_message)
    if (target_user is None):
        return
    
    
    # Delete created message
    try:
        await client.message_delete(message)
    except ConnectionError:
        # No internet connection
        return
    
    except DiscordException as err:
        # If the channel is deleted return
        if err.code in (
            ERROR_CODES.unknown_channel, # channel deleted
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ERROR_CODES.missing_access, # client removed
        ):
            return
        
        # if message deleted is fine, else raise
        if err.code != ERROR_CODES.unknown_message:
            raise
    
    # Select client based on user settings if available.
    user_settings = await get_one_user_settings(message.author.id)
    client = get_preferred_client_in_channel(
        message.channel, user_settings.preferred_client_id, client, PERMISSION_IMAGES
    )
    
    # Get context information for generating content (and cooldown)
    targets = set()
    client_in_users = False
    user_in_users = False
    
    if target_user is client:
        client_in_users = True
    elif target_user is message.author:
        user_in_users = True
    else:
        targets.add(target_user)
    
    
    # Are we on cooldown -> try notify cooldown
    expire_after = COOLDOWN_HANDLER.get_cooldown(message, len(targets))
    if expire_after > 0.0:
        try:
            private_channel = await client.channel_private_create(message.author)
        except ConnectionError:
            # No internet connect
            return
        
        try:
            await client.message_create(
                private_channel,
                f'{client.name} got bored of enacting your {intended_action}-s try again in {expire_after:.2f} seconds.',
            )
        except ConnectionError:
            # No internet connection
            return
        
        except DiscordException as err:
            # do nothing if the user has dm-s disabled
            if err.code != ERROR_CODES.cannot_message_user:
                raise
        
        return
    
    allowed_mentions = [*targets, message.author, client]
    # Create response and send
    action = ACTIONS_BY_NAME[intended_action]
    content, embed = await create_response_content_and_embed(
        action, client, None, message.guild_id, message.author, targets, client_in_users, user_in_users, allowed_mentions,
    )
    
    await send_action_response_to(client, referenced_message, content, embed, allowed_mentions)
