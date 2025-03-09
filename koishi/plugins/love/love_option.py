__all__ = ()

from scarletio import RichAttributeErrorBaseType


class LoveOption(RichAttributeErrorBaseType):
    """
    Represents a love option.
    
    Attributes
    ----------
    name : `str`
        The name of the option.
    
    text : `str`
        Text to use.
    
    titles : `tuple<str>`
        Titles to choose from.
    """
    __slots__ = ('name', 'text', 'titles')
    
    def __new__(cls, name, titles, text):
        """
        Creates a new love option.
        
        Parameters
        ----------
        name : `str`
            The name of the option.
        
        text : `str`
            Text to use.
        
        titles : `tuple<str>`
            Titles to choose from.
        """
        self = object.__new__(cls)
        self.name = name
        self.text = text
        self.titles = titles
        return self
    
    
    def __repr__(self):
        """Returns repr(self)"""
        return f'<<{type(self).__name__} name = {self.name!r}>'
