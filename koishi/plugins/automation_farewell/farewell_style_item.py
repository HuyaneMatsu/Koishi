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
    message_content_builder_localizations : `dict<Locale, FunctionType>`
        Content builder for the farewell messages by locate
    """
    __slots__ = ('image', 'image_creator', 'message_content_builder', 'message_content_builder_localizations')
    
    
    def __new__(cls, image, image_creator, message_content_builder, message_content_builder_localizations = None):
        """
        Creates a new farewell style instance.
        
        Parameters
        ----------
        image : `str`
            Image used when farewelling.
        image_creator : `str`
            Who created the image.
        message_content_builder : `FunctionType`
            Content builder for the messages.
        """
        self = object.__new__(cls)
        self.image = image
        self.image_creator = image_creator
        self.message_content_builder = message_content_builder
        self.message_content_builder_localizations = message_content_builder_localizations
        return self
    
    
    def __repr__(self):
        """Returns the farewell style's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_message_content_builder_localized(self, locale):
        """
        Gets the localized message content builder of the farewell.
        
        Parameters
        ----------
        locale : ``Locate``
            The locale to get message builder for.
        
        Returns
        -------
        message_content_builder : `FunctionType`
        """
        message_content_builder = self.message_content_builder
        message_content_builder_localizations = self.message_content_builder_localizations
        
        if (message_content_builder_localizations is not None):
            message_content_builder = message_content_builder_localizations.get(locale, message_content_builder)
        
        return message_content_builder
