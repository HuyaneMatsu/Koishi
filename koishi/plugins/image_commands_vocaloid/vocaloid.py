__all__ = ()

from hata import Embed

from ..image_handling_core import add_embed_provider

from .constants import EMBED_COLOR


VOCALOID_CHARACTERS = {
    'Aoki': 'aoki',
    'Diva': 'diva',
    'Fukase': 'fukase',
    'Gumi': 'gumi',
    'IA': 'ia',
    'Kaito': 'kaito',
    'Len': 'len',
    'Lily': 'lily',
    'Luka': 'luka',
    'Mayu': 'mayu',
    'Meiko': 'meiko',
    'Miki': 'miki',
    'Miku': 'miku',
    'Rin': 'rin',
    'Teto': 'teto',
    'Una': 'una',
    'Yukari': 'yukari',
    'ZOLA': 'zola',
}

VOCALOID_CHARACTER_TO_FULL_NAME = {
    'aoki': 'Aoki Lapis',
    'diva': 'ProjectDiva',
    'fukase': 'Fukase',
    'gumi': 'Gumi',
    'ia': 'IA',
    'kaito': 'Kaito',
    'len': 'Kagamine Len',
    'lily': 'Lily',
    'luka': 'Megurine Luka',
    'mayu': 'Mayu',
    'meiko': 'Meiko',
    'miki': 'SFA2 Miki',
    'miku': 'Hatsune Miku',
    'rin': 'Kagamine Rin',
    'teto': 'Kasane Teto',
    'una': 'Otomachi Una',
    'yukari': 'Yuzuki Yukari',
    'zola': 'ZOLA',
}


def make_custom_id_of_vocaloid(vocaloid_system_name):
    """
    Makes custom-id of the given vocaloid character.
    
    Parameters
    ----------
    vocaloid_system_name : `str`
        The respective vocaloid's system name.
    
    Returns
    -------
    custom_id : `str`
    """
    return f'vocaloid_image.{vocaloid_system_name}'


def build_vocaloid_embed(character, image_detail):
    """
    Builds a vocaloid embed.
    
    Parameters
    ----------
    character : `str`
        The vocaloid character's system name.
    image_detail : ``ImageDetailBase``
        The image detail to work from.
    
    Returns
    -------
    embed : ``Embed``
    """
    if (image_detail is None):
        embed = Embed(None, '*Could not get any images, please try again later.*', color = EMBED_COLOR)
    
    else:
        embed = Embed(
            VOCALOID_CHARACTER_TO_FULL_NAME[character], url = image_detail.url, color = EMBED_COLOR
        ).add_image(
            image_detail.url,
        )
        
        add_embed_provider(embed, image_detail)
    
    return embed


class NewVocaloid:
    """
    Represents a component command used to renew a vocaloid character.
    
    Attributes
    ----------
    character : `str`
        The respective vocaloid character.
    handler : ``ImageHandlerBase``
        The handler to use.
    """
    __slots__ = ('character', 'handler')
    
    def __new__(cls, handler, character):
        """
        Creates a new vocaloid character renewer.
        
        Parameters
        ----------
        character : `str`
            The respective vocaloid character's system name.
        handler : ``ImageHandlerBase``
            The handler to use.
        """
        self = object.__new__(cls)
        self.character = character
        self.handler = handler
        return self
    
    
    async def __call__(self, client, event):
        """
        Calls the vocaloid character renew component command.
        
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
        
        image_detail = await self.handler.get_image(client, event)
        
        embed = build_vocaloid_embed(self.character, image_detail)
        
        if event.is_unanswered():
            function = type(client).interaction_component_message_edit
        else:
            function = type(client).interaction_response_message_edit
        
        await function(
            client,
            event,
            embed = embed,
        )
