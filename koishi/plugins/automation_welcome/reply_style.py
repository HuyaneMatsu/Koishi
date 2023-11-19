__all__ = ('ReplyStyle',)

from scarletio import RichAttributeErrorBaseType


class ReplyStyle(RichAttributeErrorBaseType):
    """
    Stores a reply style.
    
    Attributes
    ----------
    button_content : `str`
        Content appearing on the reply button.
    button_emoji : ``Emoji``
        Emoji appearing on the reply button.
    reply_content_builder : `FunctionType`
        Content builder for the reply messages.
    """
    __slots__ = ('button_content', 'button_emoji', 'reply_content_builder')
    
    
    def __new__(cls, button_content, button_emoji, reply_content_builder):
        """
        Creates a new reply style instance.
        
        Parameters
        ----------
        button_content : `str`
            Content appearing on the reply button.
        button_emoji : ``Emoji``
            Emoji appearing on the reply button.
        reply_content_builder : `FunctionType`
            Content builder for the reply messages.
        """
        self = object.__new__(cls)
        self.button_content = button_content
        self.button_emoji = button_emoji
        self.reply_content_builder = reply_content_builder
        return self
    
    
    def __repr__(self):
        """Returns the reply style's representation."""
        return ''.join(['<', self.__class__.__name__, '>'])
