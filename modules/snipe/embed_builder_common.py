__all__ = ()

from hata import Embed

from .cache_emoji import update_emoji_details
from .cache_sticker import get_sticker
from .embed_builder_base import add_embed_author, add_embed_footer, copy_extra_fields, create_base_embed
from .embed_builder_emoji_details import build_emoji_details
from .embed_builder_sticker_details import build_sticker_details


async def update_sticker_details(client, sticker):
    """
    Wrapper around `get_sticker` to update its details as required.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client to update the sticker with.
    sticker : ``Sticker``
        The sticker to update.
    """
    await get_sticker(client, sticker.id)


def embed_builder_factory(entity_detail_updater, detailed_builder, name_lower_case, name_capitalised):
    """
    Creates an embed builder.
    
    Parameters
    ----------
    entity_detail_updater : `CoroutineFunctionType`
        Updates the entity with it's details.
        
        The accepted implementations are:
        - `(Client, Emoji) -> Coroutine<None>`
        - `(Client, Sticker) -> Coroutine<None>`
        
        Actual Implementations:
        - ``update_emoji_details``
        - ``update_sticker_details``
    
    
    detailed_builder : `FunctionType`
        Function to call when detailed embed is built.
        
        The accepted implementations are:
        - `(Emoji, str) -> Embed`
        - `(Sticker, str) -> Embed`
        
        Actual implementations:
        - ``build_emoji_details``
        - ``build_sticker_details``
    
    name_lower_case : `str`
        The entity's lower case name.
    
    name_capitalised : `str`
        The entity's capitalized name.
    
    Returns
    -------
    embed_builder : `CoroutineFunctionType`
        The returned embed builder is implemented as:
        - `(Client, InteractionEvent, Emoji, None | str, bool) -> Coroutine<Embed>`.
        - `(Client, InteractionEvent, Sticker, None | str, bool) -> Coroutine<Embed>`.
    """
    async def embed_builder_generic(client, event, entity, message_url, detailed):
        """
        Generic embed builder.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the interaction event.
        event : ``InteractionEvent``
            The received interaction event.
        entity : ``Emoji``, ``Sticker``
            The entity build embed for.
        message_url : `None`, `str`
            Url to the source message.
        detailed : `bool`
            Whether detailed response should be shown.
        
        Returns
        -------
        embed : ``Embed``
        """
        nonlocal detailed_builder
        nonlocal entity_detail_updater
        nonlocal name_capitalised
        nonlocal name_lower_case
        
        if detailed:
            await entity_detail_updater(client, entity)
            embed = detailed_builder(entity, name_capitalised)
            extra_fields_set = copy_extra_fields(embed, event)
            if extra_fields_set:
                return embed
        
        else:
            embed = create_base_embed(entity, None if entity.url is None else 'Click to open')
            
        add_embed_footer(embed, entity)
        add_embed_author(embed, event, name_lower_case, message_url)
        return embed
    
    return embed_builder_generic


embed_builder_emoji = embed_builder_factory(update_emoji_details, build_emoji_details, 'emoji', 'Emoji')
embed_builder_reaction = embed_builder_factory(update_emoji_details, build_emoji_details, 'reaction', 'Reaction')
embed_builder_sticker = embed_builder_factory(update_sticker_details, build_sticker_details, 'sticker', 'Sticker')
