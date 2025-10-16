__all__ = ()

from scarletio import RichAttributeErrorBaseType


class TextWallFont(RichAttributeErrorBaseType):
    """
    Represents a font for the text wall command.
    
    Attributes
    ----------
    character_resolution_table : `dict<str, bytes>`
        Character to value index resolution table.
    
    site_height : `int`
        The height of each character in the font.
    
    size_width : `int`
        The width of each character in the font.
    
    name : `str`
        The name of the font.
    """
    __slots__ = ('character_resolution_table', 'name', 'size_height', 'size_width')
    
    def __new__(cls, name, size_width, size_height, character_resolution_table):
        """
        Creates a new text wall font instance.
        
        Parameters
        ----------
        name : `str`
            The name of the font.
        
        size_width : `int`
            The width of each character in the font.
        
        site_height : `int`
            The height of each character in the font.
        
        character_resolution_table : `dict<str, bytes>`
            Character to value index resolution table.
        """
        self = object.__new__(cls)
        self.character_resolution_table = character_resolution_table
        self.name = name
        self.size_width = size_width
        self.size_height = size_height
        return self
    
    
    def __repr__(self):
        """Returns repr(self)-"""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
