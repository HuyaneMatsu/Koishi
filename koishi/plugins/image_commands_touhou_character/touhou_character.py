__all__ = ()


from hata import Embed

from ..image_handling_core import add_embed_provider
from ..touhou_core import get_familiar_touhou_matches

from .constants import EMBED_COLOR


def build_touhou_character_embed(touhou_character, image_detail):
    """
    Builds a touhou character embed.
    
    Parameters
    ----------
    touhou_character : ``TouhouCharacter``
        The respective touhou character.
    
    image_detail : ``None | ImageDetailBase``
        The image detail to work from.
    
    Returns
    -------
    embed : ``Embed``
    """
    if (image_detail is None):
        embed = Embed(None, '*Could not get any images, please try again later.*', color = EMBED_COLOR)
    
    else:
        embed = Embed(
            touhou_character.name, url = image_detail.url, color = EMBED_COLOR
        ).add_image(
            image_detail.url,
        )
        
        add_embed_provider(embed, image_detail)
    
    return embed


def build_no_match_embed(name):
    """
    Builds embed for the case when the touhou character is not found.
    
    Parameters
    ----------
    name : `str`
        The touhou character's name.
    
    Returns
    -------
    embed : ``Embed`
    """
    embed = Embed('No match', color = EMBED_COLOR)
    
    touhou_characters = get_familiar_touhou_matches(name)
    if touhou_characters:
        field_value_parts = []
        for index, (touhou_character, matched) in enumerate(touhou_characters, 1):
            field_value_parts.append(str(index))
            field_value_parts.append('.: **')
            field_value_parts.append(matched)
            field_value_parts.append('**')
            name = touhou_character.name
            if matched != name:
                field_value_parts.append(' [')
                field_value_parts.append(name)
                field_value_parts.append(']')
            
            field_value_parts.append('\n')
        
        del field_value_parts[-1]
        
        embed.add_field('Close matches:', ''.join(field_value_parts))
    
    return embed


def make_custom_id_of_character(touhou_character):
    """
    Makes custom-id of the given character.
    
    Parameters
    ----------
    touhou_character : ``TouhouCharacter``
        The respective touhou character.
    
    Returns
    -------
    custom_id : `str`
    """
    return f'touhou_character.{touhou_character.system_name}'


class NewTouhouCharacter:
    """
    Represents a component command used to renew a touhou character.
    
    Attributes
    ----------
    handler : ``ImageHandlerBase``
        The handler to use.
    touhou_character : ``TouhouCharacter``
        The respective touhou character.
    """
    __slots__ = ('handler', 'touhou_character')
    
    def __new__(cls, handler, touhou_character):
        """
        Creates a new touhou character renewer.
        
        Parameters
        ----------
        handler : ``ImageHandlerBase``
            The handler to use.
        touhou_character : ``TouhouCharacter``
            The respective touhou character.
        """
        self = object.__new__(cls)
        self.handler = handler
        self.touhou_character = touhou_character
        return self
    
    
    async def __call__(self, client, event):
        """
        Calls the touhou character renew component command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        event : ``InteractionEvent``
            The received interaction event.
        """
        if event.user is not event.message.interaction.user:
            return
         
        cg_get_image = self.handler.cg_get_image()
        
        try:
            image_detail = await cg_get_image.asend(None)
            if (image_detail is None):
                await client.interaction_component_acknowledge(event, False)
                image_detail = await cg_get_image.asend(None)
        
        except StopAsyncIteration:
            image_detail = None
        
        finally:
            cg_get_image.aclose().close()
        
        embed = build_touhou_character_embed(self.touhou_character, image_detail)
        
        if event.is_unanswered():
            function = type(client).interaction_component_message_edit
        else:
            function = type(client).interaction_response_message_edit
        
        await function(
            client,
            event,
            embed = embed,
        )
