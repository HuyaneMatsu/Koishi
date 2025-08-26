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
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __repr__(self):
        """Returns repr(self)."""
        return ''.join(['<', type(self).__name__, *self._produce_representation_middle(), '>'])
    
    
    def _produce_representation_middle(self):
        """
        Helper function for generating representation of the image handler.
        
        This function is an iterable generator.
        
        Yields
        ------
        part : `str`
        """
        return
        yield
    
    
    async def cg_get_image(self):
        """
        Gets an image's details from the handler.
        
        This method is a coroutine generator.
        
        Returns
        -------
        image_detail : `None | ImageDetailBase``
        """
        return
        yield
    
    
    async def cg_get_image_weighted(self, weight_map):
        """
        Gets an image's details from the handler.
        
        This method is a coroutine generator.
        
        Returns
        -------
        weight_map : `dict<int, float>`
            Weight map to prefer an image source over an other.
        
        Returns
        -------
        image_detail : ``None | ImageDetailBase``
        """
        async for image_detail in self.cg_get_image():
            yield image_detail
    
    
    def get_weight(self):
        """
        Returns the weight of the handler. Weights are used when randomly selecting from handlers.
        
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
