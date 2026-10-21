__all__ = ()


STRIP_STATE_UNCLOSED = 1
STRIP_STATE_EMPTY = 2
STRIP_STATE_SUCCESS = 3


def strip_content(content):
    """
    Strips the content to its code itself.
    
    Parameters
    ----------
    content : `str`
    
    Returns
    -------
    strip_result_and_content : `(int, None | str)`
    """
    content_length  = len(content)
    
    if not content_length:
        return STRIP_STATE_EMPTY, None
    
    if (content_length >= 6) and content.startswith('```'):
        start = len('```')
        
        for possible_prefix in ('python\n', 'py3\n', 'py\n', '\n'):
            possible_prefix_length = len(possible_prefix)
            if (
                (content_length >= start + 3 + possible_prefix_length) and
                (content[start : start + possible_prefix_length] == possible_prefix)
            ):
                start += possible_prefix_length
                break
        
        end = content.find('```', start)
        if end == -1:
            return STRIP_STATE_UNCLOSED, None
        
        if content[end - 1] == '\n':
            end -= 1
        
        content = content[start:end]
        
    elif (content_length >= 2) and content.startswith('`'):
        start = len('`')
        
        scan_end_index = content.find('\n')
        if scan_end_index == -1:
            scan_end_index = content_length
        
        end = content.find('`', start, scan_end_index)
        if end == -1:
            return STRIP_STATE_UNCLOSED, None
        
        content = content[start:end]
    
    if content.isspace():
        return STRIP_STATE_EMPTY, None
    
    return STRIP_STATE_SUCCESS, content
