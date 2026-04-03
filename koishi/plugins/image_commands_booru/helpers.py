__all__ = ()

from .constants import NOTE_TAG_RP, SPACE_CHARACTERS, TAG_SPLIT


SPACE_CHARACTERS_STRING = ''.join(SPACE_CHARACTERS)


def split_down_full_tags(input_value):
    """
    Returns whether the input should be auto completed.
    
    Parameters
    ----------
    input_value : `str`
        The input value to split.
    
    Returns
    -------
    full_tags : `None`, `str`
        Already prompted input.
    
    input_last : `None | str`
        The last tag we are auto completing now.
    """
    # If input ends with space, we do not split anything down.
    if input_value.endswith(SPACE_CHARACTERS):
        return input_value, None
    
    for index, character in zip(reversed(range(len(input_value) + 1)), reversed(input_value)):
        if character in SPACE_CHARACTERS:
            break
    else:
        return None, input_value
    
    
    input_last = input_value[index:]
    if (NOTE_TAG_RP.fullmatch(input_last) is not None):
        return input_value, None
    
    full_tags = input_value[:index].strip(SPACE_CHARACTERS_STRING)
    if not full_tags:
        full_tags = None
    
    return full_tags, input_last


def quote_tag_safe_booru(raw_tag):
    """
    Unquotes a safe-booru raw tag.
    
    Parameters
    ----------
    raw_tag : `str`
        The tag to process.
    
    Returns
    -------
    tag : `str`
    """
    # For now we only know about this one. If there will be more, we should modify the logic.
    return raw_tag.replace('\'', '&#039')


def iter_split_tags_safe_booru(raw_tags):
    """
    Splits the given safe-booru tags.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    raw_tags : `str`
        The raw tags to split.
    
    Yields
    -------
    tag : `str`
    """
    tags = set()
    
    for raw_tag in TAG_SPLIT.findall(raw_tags):
        if NOTE_TAG_RP.fullmatch(raw_tag) is None:
            raw_tag = quote_tag_safe_booru(raw_tag)
            tags.add(raw_tag)
    
    return tags


def iter_split_tags_gel_booru(raw_tags):
    """
    Splits the given gel-booru tags.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    raw_tags : `str`
        The raw tags to split.
    
    Yields
    -------
    tag : `str`
    """
    tags = set()
    
    for raw_tag in TAG_SPLIT.findall(raw_tags):
        if NOTE_TAG_RP.fullmatch(raw_tag) is None:
            tags.add(raw_tag)
    
    return tags


def split_tags(raw_tags, safe):
    """
    Splits the given tags
    
    Parameters
    ----------
    raw_tags : `iterable<None | str>
        The raw tags to split.
    
    safe : `bool`
        Whether to use `safe-booru` splitting or nah.
    
    Returns
    -------
    tags : `set<str>`
    """
    if safe:
        splitter = iter_split_tags_safe_booru
    else:
        splitter = iter_split_tags_gel_booru
    
    tags = set()
    
    for raw_tag in raw_tags:
        if raw_tag is not None:
            tags.update(splitter(raw_tag))
    
    return tags

