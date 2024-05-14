__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, Embed, parse_custom_emojis_ordered
from hata.ext.slash import abort

from .choice import Choice
from .choice_type import ChoiceTypeEmoji, ChoiceTypeReaction, ChoiceTypeSticker
from .embed_builder_base import add_embed_author
from .response_builder import build_initial_response_parts


DELETED_EMOJI_RP = re.compile(
    '(?:data\.)?components\[\d+\]\.components\[\d+\]\.options\[(\d+)\]\.emoji\.id\.BUTTON_COMPONENT_INVALID_EMOJI.*'
)


def remove_deleted_emojis(choices, exception):
    """
    Parses the deleted emoji indexes from the given error messages and removes the from the `choices` list.
    
    Parameters
    ----------
    choices : `list` of ``ChoiceBase``
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
        for reaction in reactions.iter_reactions():
            emoji = reaction.emoji
            if emoji.is_custom_emoji():
                yield emoji


def _build_snipe_choices(message):
    """
    Builds the snipe choices for the given message.
    
    Parameters
    ----------
    message : ``Message``
        The sniped message.
    
    Returns
    -------
    choices : `list` of ``ChoiceBase``
    """
    return [
        *(Choice(sticker, ChoiceTypeSticker) for sticker in message.iter_stickers()),
        *(Choice(emoji, ChoiceTypeEmoji) for emoji in parse_custom_emojis_ordered(message.content)),
        *(Choice(emoji, ChoiceTypeReaction) for emoji in _iter_custom_message_reactions(message)),
    ]


async def respond_snipe_whole_message(client, event, message, show_for_invoking_user_only, detailed):
    """
    Responds on sniping the given message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    message : ``Message``
        The sniped message.
    show_for_invoking_user_only : `bool`
        Whether the message should be only shown for the invoking user.
    detailed : `bool`
        Whether detailed response should be shown.
    """
    choices = _build_snipe_choices(message)
    if not choices:
        abort('The message has no custom emojis, reactions nor stickers.')

    await client.interaction_application_command_acknowledge(
        event, wait = False, show_for_invoking_user_only = show_for_invoking_user_only
    )
    
    while True:
        embed, components, file = await build_initial_response_parts(
            client, event, message, choices, show_for_invoking_user_only, detailed
        )
        
        try:
            await client.interaction_response_message_edit(event, embed = embed, components = components, file = file)
        except DiscordException as err:
            if not remove_deleted_emojis(choices, err):
                raise
        else:
            break
        
        if not choices:
            embed = build_embed_entities_deleted(event, message)
            await client.interaction_response_message_edit(event, embed = embed)
            return
