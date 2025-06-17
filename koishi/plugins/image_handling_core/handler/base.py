__all__ = ('ImageHandlerBase', )

from scarletio import RichAttributeErrorBaseType

from ...user_settings import PREFERRED_IMAGE_SOURCE_NONE


class ImageHandlerBase(RichAttributeErrorBaseType):
    """
    Base image handler.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new mage handler.
        """
        self = object.__new__(cls)
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two image handlers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    async def get_image(self, client, event, **acknowledge_parameters):
        """
        Gets an image's details from the handler.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        event : ``None | InteractionEvent``
            The respective interaction event.
        **acknowledge_parameters : Keyword parameters
            Additional parameter used when acknowledging.
        
        Returns
        -------
        image_detail : `None`, ``ImageDetailBase``
        """
        return None
    
    
    async def get_image_weighted(self, client, event, weight_map, **acknowledge_parameters):
        """
        Gets an image's details from the handler.
        
        This method is a coroutine.
        
        Returns
        -------
        client : ``Client``
            The respective client who received the event.
        event : ``None | InteractionEvent``
            The respective interaction event.
        weight_map : `dict<int, int>`
            Weight map to prefer an image source over an other.
        **acknowledge_parameters : Keyword parameters
            Additional parameter used when acknowledging.
        
        Returns
        -------
        image_detail : `None`, ``ImageDetailBase``
        """
        return await self.get_image(client, event, **acknowledge_parameters)
    
    
    def get_weight(self):
        """
        Returns the wight of the handler. Weights are used when randomly selecting from handlers.
        
        Returns
        -------
        weight : `float`
        """
        return 1.0
    
    
    def is_character_filterable(self):
        """
        Returns whether the image handler supports character filtering.
        
        Returns
        -------
        is_character_filterable : `bool`
        """
        return False
    
    
    def iter_character_filterable(self):
        """
        Iterates over the filterable characters.
        
        This method is an iterable generator.
        
        Yields
        ------
        image_detail : ``ImageDetailBase``
        """
        return
        yield
    
    
    def get_image_source(self):
        """
        Returns the handler's images' source.
        
        Returns
        -------
        image_source : `int`
        """
        return PREFERRED_IMAGE_SOURCE_NONE
    
    
    def supports_weight_mapping(self):
        """
        Returns whether the image handler supports weighting.
        
        Returns
        -------
        supports_weighting : `bool`
        """
        return False
