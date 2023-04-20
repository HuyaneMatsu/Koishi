__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, Embed, parse_custom_emojis_ordered
from hata.ext.slash import abort

from .choice import CHOICE_TYPE_EMOJI, CHOICE_TYPE_REACTION, CHOICE_TYPE_STICKER, Choice
from .embed_builder_base import add_embed_author
from .response_builder import build_initial_response_parts


SLASH_CLIENT: Client

DELETED_EMOJI_RP = re.compile(
    '(?:data\.)?components\[\d+\]\.components\[\d+\]\.options\[(\d+)\]\.emoji\.id\.BUTTON_COMPONENT_INVALID_EMOJI.*'
)


def remove_deleted_emojis(choices, exception):
    """
    Parses the deleted emoji indexes from the given error messages and removes the from the `choices` list.
    
    Parameters
    ----------
    choices : `list` of ``Choice``
        A list of choices in context.
    exception : ``DiscordException``
        The exception received from the discord api.
    
    Returns
    -------
    success : `bool`
        Returns `True` if all error message referenced a removed emoji.
    """
    if exception.code != ERROR_CODES.invalid_form_body:
        return False
    
    error_messages = exception.errors
    if not error_messages:
        return False
    
    choice_indexes_to_remove = []
    
    for error_message in error_messages:
        matched = DELETED_EMOJI_RP.fullmatch(error_message)
        if matched is None:
            return False
    
        choice_indexes_to_remove.append(int(matched.group(1)))
        continue
    
    choice_indexes_to_remove.sort(reverse = True)
    
    for index in choice_indexes_to_remove:
        del choices[index]
    
    return True


def build_embed_entities_deleted(event, target):
    """
    Builds an all sniped entities are deleted embed.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    target : ``Message``
        The interaction's target.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(None, f'*No alive entities where sniped.*')
    add_embed_author(embed, event, target.url, 'entities')
    return embed


def _iter_custom_message_reactions(message):
    """
    Iterates over the given message's custom reactions.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    Yields
    ------
    reaction : ``Emoji``
    """
    reactions = message.reactions
    if (reactions is not None):
        for reaction in reactions.keys():
            if reaction.is_custom_emoji():
                yield reaction


def _build_snipe_choices(message):
    """
    Builds the snipe choices for the given message.
    
    Parameters
    ----------
    message : ``Message``
        The sniped message.
    
    Returns
    -------
    choices : `list` of ``Choice``
    """
    return [
        *(Choice(CHOICE_TYPE_STICKER, sticker) for sticker in message.iter_stickers()),
        *(Choice(CHOICE_TYPE_EMOJI, emoji) for emoji in parse_custom_emojis_ordered(message.content)),
        *(Choice(CHOICE_TYPE_REACTION, emoji) for emoji in _iter_custom_message_reactions(message)),
    ]


@SLASH_CLIENT.interactions(is_global = True, target = 'message')
async def snipe(client, event, target):
    """
    Snipes the emojis, reactions and stickers of the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    target : ``Message``
        the targeted message by the user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    choices = _build_snipe_choices(target)
    if not choices:
        abort('The message has no custom emojis, reactions nor stickers.')

    await client.interaction_application_command_acknowledge(
        event, wait = False, show_for_invoking_user_only = True
    )
    
    while True:
        embed, components = await build_initial_response_parts(client, event, target, choices, True, False)
        
        try:
            await client.interaction_response_message_edit(event, embed = embed, components = components)
        except DiscordException as err:
            if not remove_deleted_emojis(choices, err):
                raise
        else:
            break
        
        if not choices:
            embed = build_embed_entities_deleted(event, target)
            await client.interaction_response_message_edit(event, embed = embed)
            return
