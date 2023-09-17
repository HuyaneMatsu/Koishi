__all__ = ('ImageHandlerBase', )


from scarletio import RichAttributeErrorBaseType


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
        Gets an image's url from the handler.
        
        This method is a coroutine.
        
        Returns
        -------
        url : `None`, ``ImageDetail``
            Returns `None` if image request failed.
        client : ``Client``
            The respective client who received the event.
        event : `None`, ``InteractionEvent``
            The respective interaction event.
        **acknowledge_parameters : Keyword parameters
            Additional parameter used when acknowledging.
        
        Returns
        -------
        image : ``ImageDetail``
        """
        return None
    
    
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
        image_detail : ``ImageDetail``
        """
        return
        yield
