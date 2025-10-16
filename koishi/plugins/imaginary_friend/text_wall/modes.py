__all__ = ()

from .mode import TextWallMode


def split_no_split(text):
    """
    Does not split.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    split : `list<str>`
    """
    return [text]


def split_by_character(text):
    """
    Splitter function to split the text by character.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    split : `list<str>`
    """
    return [*text]


def split_by_word(text):
    """
    Splitter function to split by word.
    
    Parameters
    ----------
    text : `str`
        Text to split.
    
    Returns
    -------
    split : `list<str>`
    """
    return text.split()


def produce_vertical(font, text, replace_resolution_table):
    """
    Produces output vertically.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    font : ``TextWallFont``
        Text wall font to use,
    
    text : `str`
        text to produce from
    
    replace_resolution_table : `tuple<str>`
        Character used to produce the replace output.
    
    Yields
    ------
    part : `str`
    """
    character_resolution_table = font.character_resolution_table
    size_width = font.size_width
    size_height = font.size_height
    
    
    for character_index in range(len(text)):
        data = character_resolution_table[text[character_index]]
        
        if character_index:
            yield '\n'
        
        for font_line_start_index in range(0, size_width * size_height, size_width):
            if font_line_start_index:
                yield '\n'
            
            for index in data[font_line_start_index : font_line_start_index + size_width]:
                yield replace_resolution_table[index]


def produce_horizontal(font, text, replace_resolution_table):
    """
    Produces output horizontally.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    font : ``TextWallFont``
        Text wall font to use,
    
    text : `str`
        text to produce from
    
    replace_resolution_table : `tuple<str>`
        Character used to produce the replace output.
    
    Yields
    ------
    part : `str`
    """
    character_resolution_table = font.character_resolution_table
    size_width = font.size_width
    size_height = font.size_height
    
    
    for font_line_start_index in range(0, size_width * size_height, size_width):
        if font_line_start_index:
            yield '\n'
            
        for character in text:
            data = character_resolution_table[character]
            for index in data[font_line_start_index : font_line_start_index + size_width]:
                yield replace_resolution_table[index]


def build_vertical(font, text, replace_resolution_table):
    """
    Builds output vertical.
    
    Parameters
    ----------
    font : ``TextWallFont``
        Text wall font to use,
    
    text : `str`
        text to produce from
    
    replace_resolution_table : `tuple<str>`
        Character used to produce the replace output.
    
    Returns
    -------
    output : `str`
    """
    return ''.join([*produce_vertical(font, text, replace_resolution_table)])


def build_horizontal(font, text, replace_resolution_table):
    """
    Builds output horizontally.
    
    Parameters
    ----------
    font : ``TextWallFont``
        Text wall font to use,
    
    text : `str`
        text to produce from
    
    replace_resolution_table : `tuple<str>`
        Character used to produce the replace output.
    
    Returns
    -------
    output : `str`
    """
    return ''.join([*produce_horizontal(font, text, replace_resolution_table)])


MODE_BY_CHARACTER = TextWallMode(
    'by character',
    split_by_character,
    build_vertical,
)


MODE_HORIZONTAL_BY_WORD = TextWallMode(
    'horizontal by word',
    split_by_word,
    build_horizontal,
)


MODE_VERTICAL_BY_WORD = TextWallMode(
    'vertical by word',
    split_by_word,
    build_vertical,
)


MODE_HORIZONTAL = TextWallMode(
    'horizontal',
    split_no_split,
    build_horizontal,
)


MODE_VERTICAL = TextWallMode(
    'vertical',
    split_no_split,
    build_vertical,
)


MODES = (
    MODE_BY_CHARACTER,
    MODE_HORIZONTAL_BY_WORD,
    MODE_VERTICAL_BY_WORD,
    MODE_HORIZONTAL,
    MODE_VERTICAL,
)
