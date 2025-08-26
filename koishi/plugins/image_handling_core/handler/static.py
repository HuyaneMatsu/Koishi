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
    _images : ``list<ImageDetailBase>``
        The registered imaged.
    
    _source : `int`
        Image source identifier for preference adjustment.
    """
    __slots__ = ('_images', '_source')
    
    def __new__(cls, source, images):
        """
        Creates a new static image handler.
        
        Parameters
        ---------
        source : `int`
            Image source identifier for preference adjustment.
        
        images : ``None | list<ImageDetailBase>``
            Images to register.
        """
        self = object.__new__(cls)
        self._images = [] if (images is None) else images
        self._source = source
        return self
    
    
    @copy_docs(ImageHandlerBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # images
        if self._images != other._images:
            return False
        
        # source
        if self._source != other._source:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerBase.cg_get_image)
    async def cg_get_image(self):
        images = self._images
        if images:
            yield choice(images)
        
        return
    
    
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
        return type(self)(
            self._source,
            [
                image for image in
                (image.create_action_subset(action_tag) for image in self._images)
                if (image is not None)
            ],
        )
