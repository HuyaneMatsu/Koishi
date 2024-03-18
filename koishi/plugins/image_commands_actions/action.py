__all__ = ()

from random import random

from hata import ClientUserBase, DiscordException, Embed, Emoji, ERROR_CODES
from hata.ext.slash import abort

from ..embed_image_refresh import schedule_image_refresh
from ..image_handling_core import add_embed_provider

from .cooldown import CooldownHandler

from .character_preference import get_preferred_image


EMOJI_FLUSHED = Emoji.precreate(965960651853926480)

COOLDOWN_HANDLER = CooldownHandler('user', 1800, 20)


def get_allowed_users(client, event, input_targets):
    """
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    input_targets : `tuple` of ``ClientUserBase``
        The input users to the command.
    
    Returns
    -------
    targets : `set<Role | ClientUserBase>`
        The mentioned users and roles by the event.
    client_in_users : `bool`
        Whether the client is in the mentioned users.
    user_in_users : `bool`
        Whether the user in in the mentioned users as well.
    allowed_mentions : `list<ClientUserBase>`
        Allowed mentions.
    """
    targets = {target for target in input_targets if target is not None}
    
    try:
        targets.remove(event.user)
    except KeyError:
        user_in_users = False
    else:
        user_in_users = True
    
    try:
        targets.remove(client)
    except KeyError:
        client_in_users = False
    else:
        client_in_users = True
    
    # Add back `event.user` and `client`, so discord client wont derp out by not showing them up as intended.
    allowed_mentions = [
        event.user,
        client,
        *(target for target in targets if isinstance(target, ClientUserBase)),
    ]
    
    return targets, client_in_users, user_in_users, allowed_mentions


def build_response(client, verb, source_user, targets, client_in_targets):
    """
    Builds action response text and allowed mentions.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    verb : `str`
        The verb to use in the response.
    source_user : ``ClientUserBase``
        The user source user who invoked the event.
    targets : `set<Role | ClientUserBase>`
        The mentioned users and roles by the event.
    client_in_targets : `bool`
        Whether the client is in the mentioned targets.
    
    Returns
    -------
    response : `str`
    """
    targets = [*targets]
    
    response_parts = ['> ']
    
    user_count = len(targets)
    if (user_count == 0) and (not client_in_targets):
        response_parts.append(client.mention)
    else:
        response_parts.append(source_user.mention)
    
    response_parts.append(' ')
    response_parts.append(verb)
    response_parts.append(' ')
    
    if user_count == 0:
        if client_in_targets:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(source_user.mention)
    
    elif user_count == 1 and not client_in_targets:
        response_parts.append(targets[0].mention)
    
    else:
        for user in targets[: - (2 - client_in_targets)]:
            response_parts.append(user.mention)
            response_parts.append(', ')
        
        response_parts.append(targets[- (2 - client_in_targets)].mention)
        response_parts.append(' and ')
        
        if client_in_targets:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(targets[-1].mention)
    
    return ''.join(response_parts)


def build_response_self(verb, source_user):
    """
    Builds action response text and allowed mentions.
    
    Parameters
    ----------
    verb : `str`
        The verb to use in the response.
    source_user : ``ClientUserBase``
        The user source user who invoked the event.
    
    Returns
    -------
    response : `str`
    """
    if random() < 0.2:
        target_word = 'herself'
    else:
        target_word = 'themselves'
    
    sign_chance = random()
    if sign_chance < 0.1:
        end_sign = '!!'
    elif sign_chance < 0.55:
        end_sign = '!?'
    else:
        end_sign = '?!'
    
    return ''.join(['> ', source_user.mention, ' ', verb, ' ', target_word, ' ', end_sign])


async def send_action_response_with_interaction_event(client, event, content, embed, allowed_mentions):
    """
    Sends action response with the given interaction event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The interaction event to respond to.
    content : `str`
        Response content.
    embed : ``Embed``
        Response embed.
    allowed_mentions : `list<ClientUserBase>`
        The users to ping.
    
    Returns
    -------
    success : `bool`
    
    Raises
    ------
    DiscordException
        Unexpected exception from Discord.
    """
    try:
        if event.is_unanswered():
            await client.interaction_response_message_create(
                event, content, allowed_mentions = allowed_mentions, embed = embed, silent = True
            )
        else:
            await client.interaction_response_message_edit(
                event, content, allowed_mentions = allowed_mentions, embed = embed
            )
    except ConnectionError:
        # No internet access
        return False
    
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_interaction:
            return False
        
        raise
    
    # Request the message back, so we can update its embed as required.
    try:
        message = await client.interaction_response_message_get(event)
    except ConnectionError:
        pass
    
    except DiscordException as err:
        if err.code != ERROR_CODES.unknown_interaction:
            raise
    
    else:
        schedule_image_refresh(client, message, event)
    
    return True


def can_send_response_to_channel(client, channel):
    """
    Returns whether response can be sent to the given channel.
    
    Parameters
    ----------
    client : ``Client``
        The client to check for.
    channel : ``Channel``
        The channel to check.
    
    Returns
    -------
    can_send_response : `bool`
    """
    permissions = channel.cached_permissions_for(client)
    
    # send messages depends on channel type.
    if channel.is_in_group_thread():
        can_send_message = permissions.can_send_messages_in_threads
    else:
        can_send_message = permissions.can_send_messages
    if not can_send_message:
        return False
    
    return True


async def send_action_response_to(client, channel_or_message, content, embed, allowed_mentions):
    """
    Sends action response to the given channel, or a reply on the given message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    channel_or_message : `Channel | Message`
        Channel to send the response to. Or a message to reply on.
    content : `str`
        Response content.
    embed : ``Embed``
        Response embed.
    allowed_mentions : `set<ClientUserBase>`
        The users to ping.
    
    Returns
    -------
    success : `bool`
    
    Raises
    ------
    DiscordException
        Unexpected exception from Discord.
    """
    try:
        message = await client.message_create(
            channel_or_message, content, allowed_mentions = allowed_mentions, embed = embed, silent = True
        )
    except ConnectionError:
        # No internet access
        return False
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.unknown_message, # Replied message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ERROR_CODES.cannot_message_user, # user has dm-s disallowed
        ):
            return False
        
        raise
    
    schedule_image_refresh(client, message)
    return True


async def send_action_response(client, event, content, embed, allowed_mentions):
    """
    Sends action response as interaction response and then to the channel if fails.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    content : `str`
        Response content.
    embed : ``Embed``
        Response embed.
    allowed_mentions : `set<ClientUserBase>`
        The users to ping.
    
    Returns
    -------
    success : `bool`
    
    Raises
    ------
    DiscordException
        Unexpected exception from Discord.
    """
    # Try interaction
    if await send_action_response_with_interaction_event(client, event, content, embed, allowed_mentions):
        return True
    
    # Try channel
    channel = event.channel
    if can_send_response_to_channel(client, channel):
        if await send_action_response_to(client, channel, content, embed, allowed_mentions):
            return True
    
    return False


class Action:
    """
    Represents an action.
    
    Attributes
    ----------
    handler : ``ImageHandlerBase``
        Image handler to use when invoking self-action.
    handler : ``ImageHandlerBase``
        Image handler to use.
    verb : `str`
        Verb used in the action.
    """
    __slots__ = ('handler', 'handler_self', 'verb')
    
    def __new__(cls, handler, verb, *, handler_self = None):
        """
        Creates a new action.
        
        Parameters
        ----------
        handler : ``ImageHandlerBase``
            Image handler to use.
        verb : `str`
            Verb used in the action.
        handler_self : `None`, ``ImageHandlerBase`` = `None`, Optional (Keyword only)
            Image handler to use when invoking self-action.
        """
        self = object.__new__(cls)
        self.handler = handler
        self.handler_self = handler_self
        self.verb = verb
        return self
    
    
    async def __call__(
        self,
        client,
        event,
        target_00: ('mentionable', 'Select someone.', 'target-1') = None,
        target_01: ('mentionable', 'Select someone', 'target-2') = None,
        target_02: ('mentionable', 'Select someone', 'target-3') = None,
        target_03: ('mentionable', 'Select someone', 'target-4') = None,
        target_04: ('mentionable', 'Select someone', 'target-5') = None,
        target_05: ('mentionable', 'Select someone', 'target-6') = None,
        target_06: ('mentionable', 'Select someone', 'target-7') = None,
        target_07: ('mentionable', 'Select someone', 'target-8') = None,
        target_08: ('mentionable', 'Select someone', 'target-9') = None,
        target_09: ('mentionable', 'Select someone', 'target-10') = None,
        target_10: ('mentionable', 'Select someone', 'target-11') = None,
        target_11: ('mentionable', 'Select someone', 'target-12') = None,
        target_12: ('mentionable', 'Select someone', 'target-13') = None,
        target_13: ('mentionable', 'Select someone', 'target-14') = None,
        target_14: ('mentionable', 'Select someone', 'target-15') = None,
        target_15: ('mentionable', 'Select someone', 'target-16') = None,
        target_16: ('mentionable', 'Select someone', 'target-17') = None,
        target_17: ('mentionable', 'Select someone', 'target-18') = None,
        target_18: ('mentionable', 'Select someone', 'target-19') = None,
        target_19: ('mentionable', 'Select someone', 'target-20') = None,
        target_20: ('mentionable', 'Select someone', 'target-21') = None,
        target_21: ('mentionable', 'Select someone', 'target-22') = None,
        target_22: ('mentionable', 'Select someone', 'target-23') = None,
        target_23: ('mentionable', 'Select someone', 'target-24') = None,
        target_24: ('mentionable', 'Select someone', 'target-25') = None,
    ):
        """
        Calls the action command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        event : ``InteractionEvent``
            The received interaction event.
        user_{n} : `None`, ``ClientUserBase`` = `None`, Optional
            Additional users to pat.
        
        Raises
        ------
        DiscordException
            Unexpected exception from Discord.
        """
        guild_id = event.guild_id
        if not guild_id:
            abort('Guild only command')
        
        targets, client_in_users, user_in_users, allowed_mentions = get_allowed_users(
            client,
            event,
            (
                target_00, target_01, target_02, target_03, target_04, target_05, target_06, target_07, target_08,
                target_09, target_10, target_11, target_12, target_13, target_14, target_15, target_16, target_17,
                target_18, target_19, target_20, target_21, target_22, target_23, target_24
            ),
        )
        
        expire_after = COOLDOWN_HANDLER.get_cooldown(event, len(targets))
        if expire_after > 0.0:
            abort(
                f'{client.name_at(event.guild_id)} got bored of enacting your {event.interaction.name} try again in '
                f'{expire_after:.2f} seconds.'
            )
        
        content, embed = await self.create_response_content_and_embed(
            client, event, event.guild_id, event.user, targets, client_in_users, user_in_users, allowed_mentions
        )
        
        await send_action_response(client, event, content, embed, allowed_mentions)

    
    async def create_response_content_and_embed(
        self, client, event, guild_id, source_user, targets, client_in_users, user_in_users, allowed_mentions
    ):
        """
        Creates response content and embed.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        event : `None`, ``InteractionEvent``
            The received interaction event if called from a command.
        guild_id : `int`
            The guild's identifier where the command was called from.
        source_user : ``ClientUserBase``
            The user source user who invoked the event.
        targets : `set<Role | ClientUserBase>`
            Target entities.
        client_in_users : `bool`
            Whether the client is in the mentioned users.
        user_in_users : `bool`
            Whether the user in in the mentioned users as well.
        allowed_mentions : `list<ClientUserBase>`
            The allowed mentions.
        
        Returns
        -------
        content : `str`
            Response content.
        embed : ``Embed``
            Response embed.
        """
        if (
            user_in_users and
            (not targets) and
            (self.handler_self is not None)
            and ((random() < 0.5) if client_in_users else True)
        ):
            content = build_response_self(self.verb, source_user)
            handler = self.handler_self
            
        else:
            content = build_response(client, self.verb, source_user, targets, client_in_users)
            handler = self.handler
        
        # Use goto
        while True:
            if handler.is_character_filterable():
                image_detail = await get_preferred_image(handler, source_user, targets)
                if (image_detail is not None):
                    break
        
            image_detail = await handler.get_image(
                client, event, content = content, allowed_mentions = allowed_mentions, silent = True,
            )
            break
        
        # Get color
        if (not targets) and (not client_in_users):
            color = client.color_at(guild_id)
        else:
            color = source_user.color_at(guild_id)
        
        
        if image_detail is None:
            embed = Embed(
                None,
                '*Could not get any images, please try again later.*',
                color = color,
            )
        
        else:
            embed = Embed(
                color = color,
            ).add_image(
                image_detail.url,
            )
            
            add_embed_provider(embed, image_detail)
        
        return content, embed
