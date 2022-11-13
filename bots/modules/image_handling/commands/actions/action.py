__all__ = ()

from random import random

from hata import Embed, Emoji
from hata.ext.slash import abort

from ...cooldown import CooldownHandler
from ...helpers import add_provider


EMOJI_FLUSHED = Emoji.precreate(965960651853926480)

COOLDOWN_HANDLER = CooldownHandler('user', 1800, 30)


def get_allowed_users(client, event, input_users):
    """
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    input_users : `tuple` of ``ClientUserBase``
        The input users to the command.
    
    Returns
    -------
    allowed_users : `set` of ``ClientUserBase``
        The mentioned users by the event.
    client_in_users : `bool`
        Whether the client is in the mentioned users.
    """
    users = set()
    for user in input_users:
        if user is not None:
            users.add(user)
    
    users.discard(event.user)
    try:
        users.remove(client)
    except KeyError:
        client_in_users = False
    else:
        client_in_users = True
    
    return users, client_in_users


def build_response(client, event, verb, users, client_in_users):
    """
    Builds action response text and allowed mentions.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    verb : `str`
        The verb to use in the response.
    users : `set` of ``ClientUserBase``
        The mentioned users by the event.
    client_in_users : `bool`
        Whether the client is in the mentioned users.
    
    Returns
    -------
    response : `str`
    """
    users = [*users]
    
    response_parts = ['> ']
    
    user_count = len(users)
    if (user_count == 0) and (not client_in_users):
        response_parts.append(client.mention)
    else:
        response_parts.append(event.user.mention)
    
    response_parts.append(' ')
    response_parts.append(verb)
    response_parts.append(' ')
    
    if user_count == 0:
        if client_in_users:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(event.user.mention)
    
    elif user_count == 1 and not client_in_users:
            response_parts.append(users[0].mention)
    
    else:
        for user in users[: - (2 - client_in_users)]:
            response_parts.append(user.mention)
            response_parts.append(', ')
        
        response_parts.append(users[- (2 - client_in_users)].mention)
        response_parts.append(' and ')
        
        if client_in_users:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(users[-1].mention)
    
    response = ''.join(response_parts)
    
    return response


class Action:
    """
    Represents an action.
    
    Attributes
    ----------
    handler : ``ImageHandlerBase``
        Image handler to use.
    verb : `str`
        Verb used in the action.
    """
    __slots__ = ('handler', 'verb')
    
    def __new__(cls, handler, verb):
        """
        Creates a new action.
        
        Parameters
        ----------
        handler : ``ImageHandlerBase``
            Image handler to use.
        verb : `str`
            Verb used in the action.
        """
        self = object.__new__(cls)
        self.verb = verb
        self.handler = handler
        return self
    
    
    async def __call__(
        self,
        client,
        event,
        user_00: ('user', 'Select someone.', 'user-1') = None,
        user_01: ('user', 'Select someone', 'user-2') = None,
        user_02: ('user', 'Select someone', 'user-3') = None,
        user_03: ('user', 'Select someone', 'user-4') = None,
        user_04: ('user', 'Select someone', 'user-5') = None,
        user_05: ('user', 'Select someone', 'user-6') = None,
        user_06: ('user', 'Select someone', 'user-7') = None,
        user_07: ('user', 'Select someone', 'user-8') = None,
        user_08: ('user', 'Select someone', 'user-9') = None,
        user_09: ('user', 'Select someone', 'user-10') = None,
        user_10: ('user', 'Select someone', 'user-11') = None,
        user_11: ('user', 'Select someone', 'user-12') = None,
        user_12: ('user', 'Select someone', 'user-13') = None,
        user_13: ('user', 'Select someone', 'user-14') = None,
        user_14: ('user', 'Select someone', 'user-15') = None,
        user_15: ('user', 'Select someone', 'user-16') = None,
        user_16: ('user', 'Select someone', 'user-17') = None,
        user_17: ('user', 'Select someone', 'user-18') = None,
        user_18: ('user', 'Select someone', 'user-19') = None,
        user_19: ('user', 'Select someone', 'user-20') = None,
        user_20: ('user', 'Select someone', 'user-21') = None,
        user_21: ('user', 'Select someone', 'user-22') = None,
        user_22: ('user', 'Select someone', 'user-23') = None,
        user_23: ('user', 'Select someone', 'user-24') = None,
        user_24: ('user', 'Select someone', 'user-25') = None,
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
        """
        guild_id = event.guild_id
        if not guild_id:
            abort('Guild only command')
        
        allowed_mentions, client_in_users = get_allowed_users(
            client,
            event,
            (
                user_00, user_01, user_02, user_03, user_04, user_05, user_06, user_07, user_08, user_09,
                user_10, user_11, user_12, user_13, user_14, user_15, user_16, user_17, user_18, user_19,
                user_20, user_21, user_22, user_23, user_24
            ),
        )
        
        expire_after = COOLDOWN_HANDLER.get_cooldown(event, len(allowed_mentions))
        if expire_after > 0.0:
            abort(
                f'Koishi got bored of enacting your {event.interaction.name} try again in {expire_after:.2f} seconds.'
            )
        
        response = build_response(
            client, event, self.verb, allowed_mentions, client_in_users
        )
        
        image_detail = await self.handler.get_image(
            client, event, content = response, allowed_mentions = allowed_mentions
        )
        
        color = (event.id >> 22) & 0xffffff
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
            
            add_provider(embed, image_detail)
        
        
        if event.is_unanswered():
            function = type(client).interaction_response_message_create
        else:
            function = type(client).interaction_response_message_edit
        
        await function(client, event, response, embed = embed, allowed_mentions = allowed_mentions)
