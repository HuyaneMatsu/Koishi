__all__ = ()

from hata import Embed, create_button
from hata.ext.slash import abort

from ..image_handling_core import ImageHandlerWaifuPics, add_embed_provider

from .constants import EMOJI_NEW, EMBED_COLOR


def build_waifu_embed(image_detail):
    """
    Builds a waifu embed.
    
    Parameters
    ----------
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
            'link', url = image_detail.url, color = EMBED_COLOR
        ).add_image(
            image_detail.url,
        )
        
        add_embed_provider(embed, image_detail)
    
    return embed


class Waifu:
    """
    Represents a waifu command's choice.
    
    Attributes
    ----------
    custom_id : `str`
        The `custom-id` used to identify the command's component.
    handler : ``ImageHandlerWaifuPics``
        The handler to use.
    safe : `bool`
        Whether to request safe image.
    waifu_type : `str`
        The waifu's type.
    """
    __slots__ = ('custom_id', 'handler', 'safe', 'waifu_type')
    
    def __new__(cls, waifu_type, safe):
        """
        Creates a new waifu command.
        
        Parameters
        ----------
        waifu_type : `str`
            The waifu's type.
        
        safe : `bool`
            Whether to request safe images.
        """
        handler = ImageHandlerWaifuPics(waifu_type, safe)
        custom_id = f'waifu.{"" if safe else "n"}sfv.{waifu_type}'
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.handler = handler
        self.safe = safe
        self.waifu_type = waifu_type
        
        
        return self
    
    
    async def __call__(self, client, event):
        """
        Calls the waifu command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        
        event : ``InteractionEvent``
            The received interaction event.
        """
        if event.guild_id == 0:
            abort('Guild only command')
        
        if (not self.safe) and (not event.channel.nsfw):
            abort('Nsfw channel only!')
        
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
        
        embed = build_waifu_embed(image_detail)
        
        if image_detail is None:
            components = None
        else:
            components = create_button(
                emoji = EMOJI_NEW,
                custom_id = self.custom_id,
            )
        
        if event.is_unanswered():
            function = type(client).interaction_response_message_create
        else:
            function = type(client).interaction_response_message_edit
        
        await function(
            client,
            event,
            embed = embed,
            components = components
        )
    
    
    def get_renew_command(self):
        """
        Returns a waifu renewer command. These can be added as component command with the ``Waifu``'s type.
        
        Returns
        -------
        renew_command : ``NewWaifu``
        """
        return NewWaifu(self.handler)


class NewWaifu:
    """
    Represents a component command used to renew a waifu.
    
    Attributes
    ----------
    handler : ``ImageHandlerWaifuPics``
        The handler to use.
    """
    __slots__ = ('handler',)
    
    def __new__(cls, handler):
        """
        Creates a new waifu renewer.
        
        Parameters
        ----------
        handler : ``ImageHandlerWaifuPics``
            The handler to use.
        """
        self = object.__new__(cls)
        self.handler = handler
        return self
    
    
    async def __call__(self, client, event):
        """
        Calls the waifu renew component command.
        
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
        
        embed = build_waifu_embed(image_detail)
        
        if event.is_unanswered():
            function = type(client).interaction_component_message_edit
        else:
            function = type(client).interaction_response_message_edit
        
        await function(
            client,
            event,
            embed = embed,
        )
