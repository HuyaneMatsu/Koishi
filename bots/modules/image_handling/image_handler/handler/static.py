__all__ = ('ImageHandlerStatic',)

from random import choice

from scarletio import copy_docs

from .base import ImageHandlerBase


class ImageHandlerStatic(ImageHandlerBase):
    """
    Image source for predefined images.
    
    Attributes
    ----------
    _images : `list` of ``ImageDetail``
    """
    __slots__ = ('_images', )
    
    def __new__(cls, images):
        """
        Creates a new static image handler.
        
        Parameters
        ---------
        images : `list` of ``ImageDetail``
            The images to return values from if required.
        """
        self = object.__new__(cls)
        self._images = images
        return self
    
    
    @copy_docs(ImageHandlerBase.get_image)
    async def get_image(self, client, event, **acknowledge_parameters):
        images = self._images
        if images:
            return choice(images)
    
    
    @copy_docs(ImageHandlerBase.get_weight)
    async def get_weight(self):
        weight = len(self._images) / 100.0
        if weight > 1.0:
            weight = 1.0
        
        return weight
