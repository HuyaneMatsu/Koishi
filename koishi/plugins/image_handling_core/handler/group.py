__all__ = ('ImageHandlerGroup',)

from itertools import islice

from scarletio import copy_docs

from ....bot_utils.random import random_index

from .base import ImageHandlerBase


class ImageHandlerGroup(ImageHandlerBase):
    """
    Handler group which chooses from the added sub-handlers and returns an image of that.
    
    Attributes
    ----------
    _handlers : ``ImageHandlerBase``
        Registered sub handlers.
    _weights : `tuple` of `float`
        The weight of each handler.
    """
    __slots__ = ('_handlers', '_weights')
    
    def __new__(cls, *handlers):
        """
        Creates a new handler group.
        
        Parameters
        ----------
        *handlers : ``ImageHandlerBase``
            Handler to group.
        """
        handler_count = len(handlers)
        if handler_count == 0:
            return ImageHandlerBase()
        
        if handler_count == 1:
            return handlers[0]
        
        weights = (*(handler.get_weight() for handler in handlers),)
        
        self = object.__new__(cls)
        self._handlers = handlers
        self._weights = weights
        return self
    
    
    @copy_docs(ImageHandlerBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._handlers != other._handlers:
            return False
        
        if self._weights != other._weights:
            return False
        
        return True

    
    @copy_docs(ImageHandlerBase.get_image)
    async def get_image(self, client, event, **acknowledge_parameters):
        handlers = self._handlers
        weights = self._weights
        
        while True:
            index = random_index(weights)
            if index == -1:
                return None
            
            handler = handlers[index]
            image_detail = await handler.get_image(client, event, **acknowledge_parameters)
            if (image_detail is not None):
                return image_detail
            
            handlers = [*islice(handlers, 0, index), *islice(handlers, index + 1, None)]
            weights = [*islice(weights, 0, index), *islice(weights, index + 1, None)]
            continue
    
    
    @copy_docs(ImageHandlerBase.is_character_filterable)
    def is_character_filterable(self):
        for handler in self._handlers:
            if handler.is_character_filterable():
                return True
        
        return False
    
    
    @copy_docs(ImageHandlerBase.iter_character_filterable)
    def iter_character_filterable(self):
        for handler in self._handlers:
            yield from handler.iter_character_filterable()
