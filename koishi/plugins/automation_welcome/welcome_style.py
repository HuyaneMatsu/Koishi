__all__ = ('WelcomeStyle',)

from scarletio import RichAttributeErrorBaseType


class WelcomeStyle(RichAttributeErrorBaseType):
    """
    Stores a welcome style.
    
    Attributes
    ----------
    images : `tuple<str>`
        Images used when welcoming.
    message_content_builders : `tuple<FunctionType>`
        Content builders for the welcome messages.
    name : `str`
        The welcome style's name.
    reply_styles : `tuple<ReplyStyle>`
        Reply styles.
    """
    __slots__ = ('images',  'message_content_builders', 'name', 'reply_styles')
    
    
    def __new__(cls, name, message_content_builders, images, reply_styles):
        """
        Creates a new welcome style instance.
        
        Parameters
        ----------
        name : `str`
            The welcome style's name.
        message_content_builders : `tuple<FunctionType>`
            Content builders for the messages.
        images : `tuple<str>`
            Images used when welcoming.
        reply_styles : `tuple<FunctionType>`
            Content builders for the reply messages.
        """
        self = object.__new__(cls)
        self.images = images
        self.message_content_builders = message_content_builders
        self.name = name
        self.reply_styles = reply_styles
        return self
    
    
    def __repr__(self):
        """Returns the welcome style's representation."""
        return ''.join(['<', self.__class__.__name__, ' name = ', repr(self.name), '>'])
