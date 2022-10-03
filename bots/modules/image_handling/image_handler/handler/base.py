__all__ = ('ImageHandlerBase', )

class ImageHandlerBase:
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
