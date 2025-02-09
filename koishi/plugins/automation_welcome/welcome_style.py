__all__ = ('WelcomeStyle',)

from scarletio import RichAttributeErrorBaseType


class WelcomeStyle(RichAttributeErrorBaseType):
    """
    Stores a welcome style.
    
    Attributes
    ----------
    client_id : `int`
        Client identifier to associate with the welcome style.
    
    image_creator : `str`
        Who created the images.
    
    images : `tuple<str>`
        Images used when welcoming.
    
    message_content_builders : `tuple<FunctionType>`
        Content builders for the welcome messages.
    
    name : `str`
        The welcome style's name.
    
    reply_styles : `tuple<WelcomeStyleReply>`
        Reply styles.
    """
    __slots__ = ('client_id', 'image_creator', 'images', 'message_content_builders', 'name', 'reply_styles')
    
    
    def __new__(cls, name, client_id, message_content_builders, images, image_creator, reply_styles):
        """
        Creates a new welcome style instance.
        
        Parameters
        ----------
        name : `str`
            The welcome style's name.
        
        client_id : `int`
            Client identifier to associate with the welcome style.
        
        message_content_builders : `tuple<FunctionType>`
            Content builders for the messages.
        
        images : `tuple<str>`
            Images used when welcoming.
        
        image_creator : `str`
            Who created the images.
        
        reply_styles : `tuple<FunctionType>`
            Content builders for the reply messages.
        """
        self = object.__new__(cls)
        self.client_id = client_id
        self.images = images
        self.image_creator = image_creator
        self.message_content_builders = message_content_builders
        self.name = name
        self.reply_styles = reply_styles
        return self
    
    
    def __repr__(self):
        """Returns the welcome style's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
