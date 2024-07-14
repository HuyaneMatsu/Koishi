__all__ = ('FarewellStyleItem',)

from scarletio import RichAttributeErrorBaseType


class FarewellStyleItem(RichAttributeErrorBaseType):
    """
    Stores a farewell style§s item.
    
    Attributes
    ----------
    image : `str`
        Image used when farewelling.
    image_creator : `str`
        Who created the image.
    message_content_builder : `FunctionType`
        Content builder for the farewell messages.
    """
    __slots__ = ('image', 'image_creator', 'message_content_builder')
    
    
    def __new__(cls, message_content_builder, image, image_creator):
        """
        Creates a new farewell style instance.
        
        Parameters
        ----------
        message_content_builder : `FunctionType`
            Content builder for the messages.
        image : `str`
            Image used when farewelling.
        image_creator : `str`
            Who created the image.
        """
        self = object.__new__(cls)
        self.image = image
        self.image_creator = image_creator
        self.message_content_builder = message_content_builder
        return self
    
    
    def __repr__(self):
        """Returns the farewell style's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append('>')
        return ''.join(repr_parts)
