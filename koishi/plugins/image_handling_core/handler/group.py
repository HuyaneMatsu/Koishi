__all__ = ('ImageHandlerGroup',)

from itertools import islice

from scarletio import copy_docs

from ....bot_utils.random import random_index

from .base import ImageHandlerBase


def get_handler_weights_with_weight_map(handlers, weight_map):
    """
    Gets handler weights applying a weight map to their weight.
    
    Parameters
    ----------
    handlers : `list` of ``ImageHandlerBase``
        Handlers to get weights for.
    weight_map : `dict<int, int>`
        Weight map to prefer an image source over an other.
    
    Return
    ------
    weights : `list<int>`
    """
    allowed_image_sources = {handler.get_image_source() for handler in handlers}
    
    # Collect value to discard
    discarded_weight_sum = 0.0
    
    for key in [*weight_map.keys()]:
        if key not in allowed_image_sources:
            discarded_weight_sum += weight_map.pop(key)
    
    # Add not present values as 0.0
    for key in allowed_image_sources:
        weight_map.setdefault(key, 0.0)
    
    # Apply discarded sum
    if discarded_weight_sum != 0.0:
        increment_by_value =  discarded_weight_sum / len(allowed_image_sources)
        for key, value in weight_map.items():
            weight_map[key] = value + increment_by_value
    
    return [handler.get_weight() * weight_map[handler.get_image_source()] for handler in handlers]


class ImageHandlerGroup(ImageHandlerBase):
    """
    Handler group which chooses from the added sub-handlers and returns an image of that.
    
    Attributes
    ----------
    _handlers : `list` of ``ImageHandlerBase``
        Registered sub handlers.
    _weights : `list` of `float`
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
        
        weights = [handler.get_weight() for handler in handlers]
        handlers = [*handlers]
        
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
        return await self._get_image_with_weights(client, event, self._weights, acknowledge_parameters)
    
    
    
    @copy_docs(ImageHandlerBase.get_image_weighted)
    async def get_image_weighted(self, client, event, weight_map, **acknowledge_parameters):
        weights = get_handler_weights_with_weight_map(self._handlers, weight_map)
        return await self._get_image_with_weights(client, event, weights, acknowledge_parameters)
    
    
    async def _get_image_with_weights(self, client, event, weights, acknowledge_parameters):
        """
        Gets an image detail with weight for each handler.
        If an image handler cannot produce image is discarded temporarily.
        
        This function is a coroutine.
        
        client : ``Client``
            The respective client who received the event.
        event : `None`, ``InteractionEvent``
            The respective interaction event.
        weights : `list<int>`
            Weights for each handler.
        acknowledge_parameters : `dict<str, object>`
            Additional parameter used when acknowledging.
        
        Returns
        -------
        image_detail : `None`, ``ImageDetail``
        """
        handlers = self._handlers
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
    
    
    @copy_docs(ImageHandlerBase.supports_weight_mapping)
    def supports_weight_mapping(self):
        previous_preferred_image_source = -1
        for handler in self._handlers:
            preferred_image_source = handler.get_image_source()
            if previous_preferred_image_source == -1:
                previous_preferred_image_source = preferred_image_source
                continue
            
            if previous_preferred_image_source != previous_preferred_image_source:
                return True
        
        return False
