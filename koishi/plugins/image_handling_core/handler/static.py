__all__ = ('ImageHandlerStatic',)

from random import choice

from scarletio import copy_docs

from .base import ImageHandlerBase

from ..image_detail import ImageDetailStatic


class ImageHandlerStatic(ImageHandlerBase):
    """
    Image source for predefined images.
    
    Attributes
    ----------
    _images : `list` of ``ImageDetailBase``
        The registered imaged.
    _source : `int`
        Image source identifier for preference adjustment.
    """
    __slots__ = ('_images', '_source')
    
    def __new__(cls, source):
        """
        Creates a new static image handler.
        
        Parameters
        ---------
        source : `int`
            Image source identifier for preference adjustment.
        """
        self = object.__new__(cls)
        self._images = []
        self._source = source
        return self
    
    
    @copy_docs(ImageHandlerBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._images != other._images:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerBase.get_image)
    async def get_image(self, client, event, **acknowledge_parameters):
        images = self._images
        if images:
            return choice(images)
    
    
    @copy_docs(ImageHandlerBase.get_weight)
    def get_weight(self):
        weight = len(self._images) / 100.0
        if weight > 1.0:
            weight = 1.0
        
        return weight
    
    
    @copy_docs(ImageHandlerBase.is_character_filterable)
    def is_character_filterable(self):
        return True
    
    
    @copy_docs(ImageHandlerBase.iter_character_filterable)
    def iter_character_filterable(self):
        yield from self._images

    
    @copy_docs(ImageHandlerBase.get_image_source)
    def get_image_source(self):
        return self._source
    
    
    def add(self, url):
        """
        Adds a new url as an image to the image handler.
        
        Parameters
        ----------
        url : `str`
            Url to create image detail with.
        
        Returns
        -------
        image_detail : ``ImageDetailStatic``
        """
        image_detail = ImageDetailStatic(url)
        self._images.append(image_detail)
        return image_detail
    
    
    def create_action_subset(self, action_tag):
        """
        Creates a subset of the image handler matching the given action tag.
        
        Parameters
        ----------
        action_tag : `str`
            The action's tag to match.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = type(self)(self._source)
        
        for image in self._images:
            image = image.create_action_subset(action_tag)
            if (image is not None):
                new._images.append(image)
        
        return new
    
    
    def with_images(self, images):
        """
        Returns the image detail extending itself with the given images.
        
        Parameters
        ----------
        images : `list` of ``ImageDetailBase``
            Images to extend self with.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        self._images.extend(images)
        return self
