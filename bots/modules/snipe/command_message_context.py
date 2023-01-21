__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, Embed, parse_custom_emojis_ordered
from hata.ext.slash import abort

from .embed_builder_base import add_embed_author
from .response_builder import build_initial_response_parts_emoji, build_initial_response_parts_reaction
from .response_builder import build_initial_response_sticker


SLASH_CLIENT: Client

DELETED_EMOJI_RP = re.compile(
    '(?:data\.)?components\[\d+\]\.components\[\d+\]\.options\[(\d+)\]\.emoji\.id\.BUTTON_COMPONENT_INVALID_EMOJI.*'
)



def remove_deleted_emojis(emojis, exception):
    """
    Parses the deleted emoji indexes from the given error messages and removes the from the `emojis` list.
    
    Parameters
    ----------
    emojis : `list` of ``Emoji``
        A list of emojis in context.
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
    
    emoji_indexes_to_remove = []
    
    for error_message in error_messages:
        matched = DELETED_EMOJI_RP.fullmatch(error_message)
        if matched is None:
            return False
    
        emoji_indexes_to_remove.append(int(matched.group(1)))
        continue
    
    emoji_indexes_to_remove.sort(reverse = True)
    
    for index in emoji_indexes_to_remove:
        del emojis[index]
    
    return True


def build_embed_entities_deleted_factory(entity_name_lower_case, entity_name_lower_case_plural):
    """
    Returns an embed builder used when all entities were deleted.
    
    Parameters
    ----------
    entity_name_lower_case : `str`
        The entity's name in lower case.
    entity_name_lower_case_plural : `str`
        The entity's name in lower case in plural.
    
    Returns
    -------
    embed_builder : `FunctionType`
        The embed builder implementation is:
        - `(InteractionEvent, Message) -> Embed`
    """
    def build_embed_entities_deleted_generic(event, target):
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
        nonlocal entity_name_lower_case
        nonlocal entity_name_lower_case_plural
        
        embed = Embed(None, f'*No alive {entity_name_lower_case_plural} where sniped.*')
        add_embed_author(embed, event, target.url, entity_name_lower_case)
        return embed
    
    return build_embed_entities_deleted_generic


def respond_with_emojis_factory(response_parts_builder, embed_builder_entities_deleted):
    """
    Returns an emoji based snipe responder.
    
    Parameters
    ----------
    response_parts_builder : `CoroutineFunctionType`
        Response parts builder.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, list<Emoji>, bool, bool) -> Coroutine<Embed, list<Component>>`
    
        Actual implementations:
        - ``build_initial_response_parts_emoji``
        - ``build_initial_response_parts_reaction``
    
    embed_builder_entities_deleted : `FunctionType`
        Embed builder used when all sniped emojis were deleted.
    
        The accepted implementations are:
        - `(InteractionEvent, Message) -> Embed`
        
        Actual implementations:
        - ``build_embed_entities_deleted_emoji``
        -- ``build_embed_entities_deleted_reaction``
    
    Returns
    -------
    responder : `CoroutineFunctionType`
        The responder is implemented as:
        - `(Client, InteractionEvent, Message, list<Emoji>) -> Coroutine`
    """
    async def respond_with_emojis_generic(client, event, target, entities):
        """
        Response on an emoji snipe interaction.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the interaction event.
        event : ``InteractionEvent``
            The received event.
        target : ``Message``
            The targeted entity.
        entities : `list` of ``Emoji``
            The entities to produce response for.
        """
        nonlocal response_parts_builder
        nonlocal embed_builder_entities_deleted
        
        await client.interaction_application_command_acknowledge(
            event, wait = False, show_for_invoking_user_only = True)
        
        while True:
            embed, components = await response_parts_builder(client, event, target, entities, True, False)
            
            try:
                await client.interaction_response_message_edit(event, embed = embed, components = components)
            except DiscordException as err:
                if not remove_deleted_emojis(entities, err):
                    raise
            else:
                break
            
            if not entities:
                embed = embed_builder_entities_deleted(event, target)
                await client.interaction_response_message_edit(event, embed = embed)
                return
    
    return respond_with_emojis_generic


build_embed_entities_deleted_emoji = build_embed_entities_deleted_factory('emoji', 'emojis')
build_embed_entities_deleted_reaction = build_embed_entities_deleted_factory('reaction', 'reactions')


response_with_emojis_emoji = respond_with_emojis_factory(
    build_initial_response_parts_emoji, build_embed_entities_deleted_emoji)

response_with_emojis_reaction = respond_with_emojis_factory(
    build_initial_response_parts_reaction, build_embed_entities_deleted_reaction)


@SLASH_CLIENT.interactions(is_global = True, target = 'message')
async def snipe_emojis(client, event, target):
    """
    Snipes the emojis of the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    target : ``Message``
        the targeted message by the user.
    """
    emojis = parse_custom_emojis_ordered(target.content)
    if not emojis:
        abort('The message has no emojis.')
    
    await response_with_emojis_emoji(client, event, target, emojis)


@SLASH_CLIENT.interactions(is_global = True, target = 'message')
async def snipe_reactions(client, event, target):
    """
    Snipes the reactions of the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    target : ``Message``
        the targeted message by the user.
    """
    reactions = target.reactions
    if (reactions is None) or (not reactions):
        abort('The message has no reactions.')
    
    await response_with_emojis_emoji(client, event, target, [*reactions.keys()])


@SLASH_CLIENT.interactions(is_global = True, target = 'message')
async def snipe_stickers(client, event, target):
    """
    Snipes the stickers of the message.
    
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
    stickers = target.stickers
    if (stickers is None):
        abort('The message has no stickers.')
    
    return await build_initial_response_sticker(client, event, target, [*stickers], True, False)
