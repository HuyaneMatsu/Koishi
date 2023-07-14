__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, MessageType, USER_MENTION_RP

from ....bots import SLASH_CLIENT

from .action import COOLDOWN_HANDLER
from .actions import (
    ACTION_BITE, ACTION_BLUSH, ACTION_BULLY, ACTION_CRINGE, ACTION_CRY, ACTION_CUDDLE, ACTION_DANCE, ACTION_GLOMP,
    ACTION_HANDHOLD, ACTION_HAPPY, ACTION_HIGHFIVE, ACTION_HUG, ACTION_KICK, ACTION_KILL, ACTION_KISS, ACTION_LICK,
    ACTION_LIKE, ACTION_NOM, ACTION_PAT, ACTION_POCKY, ACTION_POKE, ACTION_SLAP, ACTION_SMILE, ACTION_SMUG, ACTION_WAVE,
    ACTION_WINK, ACTION_YEET
)


ACTIONS_BY_NAME = {
    'bite': ACTION_BITE,
    'blush': ACTION_BLUSH,
    'bully': ACTION_BULLY,
    'cringe': ACTION_CRINGE,
    'cry': ACTION_CRY,
    'cuddle': ACTION_CUDDLE,
    'dance': ACTION_DANCE,
    'glomp': ACTION_GLOMP,
    'handhold': ACTION_HANDHOLD,
    'happy': ACTION_HAPPY,
    'highfive': ACTION_HIGHFIVE,
    'hug': ACTION_HUG,
    'kick': ACTION_KICK,
    'kill': ACTION_KILL,
    'kiss': ACTION_KISS,
    'lick': ACTION_LICK,
    'like': ACTION_LIKE,
    'nom': ACTION_NOM,
    'pat': ACTION_PAT,
    'pocky-kiss': ACTION_POCKY,
    'poke': ACTION_POKE,
    'slap': ACTION_SLAP,
    'smile': ACTION_SMILE,
    'smug': ACTION_SMUG,
    'wave': ACTION_WAVE,
    'wink': ACTION_WINK,
    'yeet': ACTION_YEET,
}


MAX_ACTION_COMMAND_LENGTH = max(len(name) for name in ACTIONS_BY_NAME.keys())

ACTION_CONTENT_RP = re.compile(f'> {USER_MENTION_RP.pattern} ', re.M | re.U)


def could_respond_in_channel(client, channel):
    """
    Returns whether the client could respond in the channel as intended.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel : ``Channel``
        The respective channel.
    
    Returns
    -------
    could_respond : `bool`
    """
    permissions = channel.cached_permissions_for(client)
    
    # manage messages needed for deleting the message.
    if not permissions.can_manage_messages:
        return False
    
    # send messages depends on channel type.
    if channel.is_in_group_thread():
        can_send_message = permissions.can_send_messages_in_threads
    else:
        can_send_message = permissions.can_send_messages
    if not can_send_message:
        return False
    
    # Everything looks good
    return True


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
    if message.author is not client:
        return False
    
    message_type = message.type
    if message_type is MessageType.slash_command:
        interaction = message.interaction
        if (interaction is not None):
            return interaction.name in ACTIONS_BY_NAME.keys()
    
    # We do not receive nonce for requested or referenced messages, so we cannot match that reliable.
    # Try to match message by structure~
    elif message_type is MessageType.inline_reply:
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
    
    if len(content) > MAX_ACTION_COMMAND_LENGTH:
        return None
    
    content = content.lower().replace(' ', '-').replace('_', '-')
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


@SLASH_CLIENT.events
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
    if message.author.bot:
        return
    
    if message.type is not MessageType.inline_reply:
        return
    
    referenced_message = message.referenced_message
    if referenced_message is None:
        return
    
    if not is_message_action_interaction(client, referenced_message):
        return
    
    if not could_respond_in_channel(client, message.channel):
        return False
    
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
    
    
    # Get context information for generating content (and cooldown)
    allowed_mentions = set()
    client_in_users = False
    user_in_users = False
    
    if target_user is client:
        client_in_users = True
    elif target_user is message.author:
        user_in_users = True
    else:
        allowed_mentions.add(target_user)
    
    
    # Are we on cooldown -> try notify cooldown
    expire_after = COOLDOWN_HANDLER.get_cooldown(message, len(allowed_mentions))
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
    
    # Create response and send
    content, embed = await ACTIONS_BY_NAME[intended_action].create_response_content_and_embed(
        client, None, message.id, message.author, allowed_mentions, client_in_users, user_in_users
    )
    
    try:
        await client.message_create(
            referenced_message, content, allowed_mentions = allowed_mentions, embed = embed, silent = True
        )
    except ConnectionError:
        # No internet connect
        return
    
    except DiscordException as err:
        # If the channel is deleted return
        if err.code not in (
            ERROR_CODES.unknown_channel, # channel deleted
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ERROR_CODES.missing_access, # client removed
        ):
            raise

