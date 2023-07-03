__all__ = ()

from random import random

from hata import Embed, Emoji
from hata.ext.slash import abort

from ..cooldown import CooldownHandler
from ..helpers import add_provider


EMOJI_FLUSHED = Emoji.precreate(965960651853926480)

COOLDOWN_HANDLER = CooldownHandler('user', 1800, 20)


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
    user_in_users : `bool`
        Whether the user in in the mentioned users as well.
    """
    users = set()
    for user in input_users:
        if user is not None:
            users.add(user)
    
    try:
        users.remove(event.user)
    except KeyError:
        user_in_users = False
    else:
        user_in_users = True
    
    try:
        users.remove(client)
    except KeyError:
        client_in_users = False
    else:
        client_in_users = True
    
    return users, client_in_users, user_in_users


def build_response(client, verb, source_user, users, client_in_users):
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
        response_parts.append(source_user.mention)
    
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
            response_parts.append(source_user.mention)
    
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
        
        allowed_mentions, client_in_users, user_in_users = get_allowed_users(
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
                f'{client.name_at(event.guild_id)} got bored of enacting your {event.interaction.name} try again in '
                f'{expire_after:.2f} seconds.'
            )
        
        content, embed = await self.create_response_content_and_embed(
            client, event, event.id, event.user, allowed_mentions, client_in_users, user_in_users
        )
        
        if event.is_unanswered():
            await client.interaction_response_message_create(
                event, content, allowed_mentions = allowed_mentions, embed = embed, silent = True
            )
        else:
            await client.interaction_response_message_edit(
                event, content, allowed_mentions = allowed_mentions, embed = embed
            )
    
    
    async def create_response_content_and_embed(
        self, client, event, color_seed, source_user, allowed_mentions, client_in_users, user_in_users
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
        color_seed : `int`
            Seed to generate the embed color from.
        source_user : ``ClientUserBase``
            The user source user who invoked the event.
        allowed_users : `set` of ``ClientUserBase``
            The mentioned users by the event.
        client_in_users : `bool`
            Whether the client is in the mentioned users.
        user_in_users : `bool`
            Whether the user in in the mentioned users as well.
        
        Returns
        -------
        content : `str`
            Response content.
        embed : ``Embed``
            Response embed.
        """
        if (
            user_in_users and
            (not allowed_mentions) and
            (self.handler_self is not None)
            and ((random() < 0.5) if client_in_users else True)
        ):
            content = build_response_self(self.verb, source_user)
            handler = self.handler_self
            
        else:
            content = build_response(client, self.verb, source_user, allowed_mentions, client_in_users)
            handler = self.handler
        
        image_detail = await handler.get_image(
            client, event, content = content, allowed_mentions = allowed_mentions, silent = True,
        )
        
        color = (color_seed >> 22) & 0xffffff
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
        
        return content, embed
