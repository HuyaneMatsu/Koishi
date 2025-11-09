__all__ = ()

from itertools import islice

from .constants import ACHIEVEMENTS


def parse_input(content):
    """
    Parses the input content.
    
    Parameters
    ----------
    content : `str`
        Content to parse.
    
    Returns
    -------
    user_owned_achievements : `set<str>`
    """
    lines = content.splitlines()
    
    empty_line_count_start = 0
    for line in lines:
        if line:
            break
        
        empty_line_count_start += 1
        continue
    
    empty_line_count_end = 0
    for line in reversed(lines):
        if line:
            break
        
        empty_line_count_end += 1
        continue
    
    return {*islice(lines, empty_line_count_start, len(lines) - empty_line_count_end, 3)}


def build_output(user_owned_achievements):
    """
    Builds output file content.
    
    Parameters
    ----------
    user_owned_achievements : `set<str>`
        The achievements owned by the user.
    
    Returns
    -------
    output : `str`
    """
    return '\n'.join([
        ('Yes' if achievement_name in user_owned_achievements else 'No')
        for achievement_name in ACHIEVEMENTS
    ])
