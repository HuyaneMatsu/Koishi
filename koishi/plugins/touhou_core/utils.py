__all__ = (
    'get_familiar_touhou_matches', 'get_familiar_touhou_matches_from', 'get_touhou_character_like',
    'get_touhou_character_like_from', 'get_touhou_character_names_like', 'get_touhou_character_names_like_from'
)

from difflib import get_close_matches
from re import compile as re_compile, I as re_ignore_case, U as re_unicode, escape as re_escape

from .character import TOUHOU_CHARACTER_LOOKUP, TOUHOU_CHARACTER_NAMES


def _build_allowed_names_and_lookup_map(characters):
    """
    Builds allowed names for filtering names and lookup map for resolving the best match.
    Used for custom character set queries.
    
    Parameters
    ----------
    characters : `list<TouhouCharacter>`
        Characters to build the output for.
    
    Returns
    -------
    allowed_names : `list<str>`
        Names to match from.
    lookup_map : `dict<str, TouhouCharacter>
        Character lookup map.
    """
    allowed_names = []
    lookup_map = {}
    
    for character in characters:
        for name in character.iter_names():
            name = name.casefold()
            allowed_names.append(name)
            lookup_map[name] = character
    
    return allowed_names, lookup_map


def _get_touhou_character_like_from(name, allowed_names, lookup_map):
    """
    Gets the touhou character with the most familiar name.
    
    Parameters
    ----------
    name : `str`
        Input value.
    allowed_names : `list<str>`
        Names to match from.
    lookup_map : `dict<str, TouhouCharacter>
        Character lookup map.
    
    Returns
    -------
    matched : `None | TouhouCharacter`
    """
    name_length = len(name)
    if name_length == 0:
        return None
    
    name = name.replace('-', ' ').replace('_', ' ').casefold()
    
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2 + (10 - name_length) * 0.02
    
    matcheds = get_close_matches(
        name,
        allowed_names,
        n = 1,
        cutoff = 1.0 - diversity,
    )
    
    if matcheds:
        return lookup_map[matcheds[0]]


def _iter_names_like(name, allowed_names):
    """
    Iterates over familiar names to the given one.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Names to match.
    allowed_names : `list<str>`
        Names to match from.
    
    Yields
    ------
    character_name : `str`
    """
    matcher = re_compile(re_escape(name), re_ignore_case | re_unicode)
    
    for character_name in allowed_names:
        if (matcher.match(character_name) is not None):
            yield character_name

    value_length = len(name)
    if value_length < 3:
        return
    
    if len(name) > 10:
        value_length = 10
    
    diversity = 0.2 + (10 - value_length) * 0.02
    
    yield from get_close_matches(
        name,
        allowed_names,
        n = 25,
        cutoff = 1.0 - diversity,
    )


def _get_touhou_character_names_like_from(name, allowed_names, lookup_map):
    """
    Gets the touhou characters that have familiar names to the given one.
    
    Parameters
    ----------
    name : `str`
        Input value.
    allowed_names : `list<str>`
        Names to match from.
    lookup_map : `dict<str, TouhouCharacter>
        Character lookup map.
    
    Returns
    -------
    matches : `list<str>`
    """
    unique = []
    characters = set()
    
    for name in _iter_names_like(name, allowed_names):
        character = lookup_map[name]
        if character in characters:
            continue
        
        characters.add(character)
        unique.append(name)
        if len(unique) < 25:
            continue
        
        break
    
    return unique


def _get_familiar_touhou_matches_from(name,  allowed_names, lookup_map):
    """
    Gets touhou characters with familiar name to the given one.
    
    Parameters
    ----------
    name : `str`
        Input value.
    allowed_names : `list<str>`
        Names to match from.
    lookup_map : `dict<str, TouhouCharacter>
        Character lookup map.
    
    Returns
    -------
    touhou_characters : `list<(TouhouCharacter, str)>`
    """
    name_length = len(name)
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2 + (10 - name_length) * 0.02
    
    matcheds = get_close_matches(
        name,
        allowed_names,
        n = 10,
        cutoff = 1.0 - diversity,
    )
    
    return [(lookup_map[matched], matched) for matched in matcheds]


def get_touhou_character_like(name):
    """
    Gets the touhou character with the most familiar name.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    matched : `None | TouhouCharacter`
    """
    return _get_touhou_character_like_from(name, TOUHOU_CHARACTER_NAMES, TOUHOU_CHARACTER_LOOKUP)


def get_touhou_character_like_from(name, characters):
    """
    Gets the touhou character with the most familiar name.
    Matches from the given characters only.
    
    Parameters
    ----------
    name : `str`
        Input value.
    characters : `list<TouhouCharacter>`
        Characters to build the output for.
    
    Returns
    -------
    matched : `None | TouhouCharacter`
    """
    return _get_touhou_character_like_from(name, *_build_allowed_names_and_lookup_map(characters))


def get_touhou_character_names_like(name):
    """
    Gets the touhou characters' names who's name match the given input.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    unique : `list<str>`
    """
    return _get_touhou_character_names_like_from(name, TOUHOU_CHARACTER_NAMES, TOUHOU_CHARACTER_LOOKUP)


def get_touhou_character_names_like_from(name, characters):
    """
    Gets the touhou characters' names who's name match the given input.
    Matches from the given characters only.
    
    Parameters
    ----------
    name : `str`
        Input value.
    characters : `list<TouhouCharacter>`
        Characters to build the output for.
    
    Returns
    -------
    unique : `list<str>`
    """
    return _get_touhou_character_names_like_from(name, *_build_allowed_names_and_lookup_map(characters))


def get_familiar_touhou_matches(name):
    """
    Gets touhou characters with familiar name to the given one.
    Can be used to generate suggestions.
    
    Parameters
    ----------
    name : `str`
        Input value.
    
    Returns
    -------
    touhou_characters : `list<(TouhouCharacter, str)>`
    """
    return _get_familiar_touhou_matches_from(name, TOUHOU_CHARACTER_NAMES, TOUHOU_CHARACTER_LOOKUP)


def get_familiar_touhou_matches_from(name, characters):
    """
    Gets touhou characters with familiar name to the given one.
    Matches from the given characters only.
    Can be used to generate suggestions.
    
    Parameters
    ----------
    name : `str`
        Input value.
    characters : `list<TouhouCharacter>`
        Characters to build the output for.
    
    Returns
    -------
    touhou_characters : `list<(TouhouCharacter, str)>`
    """
    return _get_familiar_touhou_matches_from(name, *_build_allowed_names_and_lookup_map(characters))
