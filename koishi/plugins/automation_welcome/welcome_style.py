__all__ = ('WelcomeStyle',)

from scarletio import RichAttributeErrorBaseType


class WelcomeStyle(RichAttributeErrorBaseType):
    """
    Stores a welcome style.
    
    Attributes
    ----------
    button_contents : `tuple<str>`
        Contents appearing on the welcome button.
    button_emoji : ``Emoji``
        Emoji appearing on the welcome button.
    images : `tuple<str>`
        Images used when welcoming.
    message_content_builders : `tuple<FunctionType>`
        Content builders for the welcome messages.
    name : `str`
        The welcome style's name.
    reply_content_builders : `tuple<FunctionType>`
        Content builders for the reply messages.
    """
    __slots__ = (
        'button_contents', 'button_emoji', 'images',  'message_content_builders', 'name', 'reply_content_builders'
    )
    
    
    def __new__(cls, name, message_content_builders, images, button_emoji, button_contents, reply_content_builders):
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
        button_emoji : ``Emoji``
            Emoji appearing on the welcome button.
        button_contents : `tuple<str>`
            Contents appearing on the welcome button.
        reply_content_builders : `tuple<FunctionType>`
            Content builders for the reply messages.
        """
        self = object.__new__(cls)
        self.button_contents = button_contents
        self.button_emoji = button_emoji
        self.images = images
        self.message_content_builders = message_content_builders
        self.name = name
        self.reply_content_builders = reply_content_builders
        return self
    
    
    def __repr__(self):
        """Returns the welcome style's representation."""
        return ''.join(['<', self.__class__.__name__, ' name = ', repr(self.name), '>'])
