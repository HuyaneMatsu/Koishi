__all__ = ()

from re import I as re_ignore_case, compile as re_compile, escape as re_escape


from ..adventure_core import LOCATIONS, LOCATIONS_ALLOWED


def get_best_matching_location(value, user_level):
    """
    Gets the best matching location for the given value.
    
    Parameters
    ----------
    value : `None | str`
        The value to match.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    location : ``None | Location``
    """
    if value is None:
        return None
    
    try:
        location_id = int(value, base = 16)
    except ValueError:
        pass
    else: 
        try:
            location = LOCATIONS[location_id]
        except KeyError:
            pass
        else:
            if location.level > user_level:
                return None
            
            return location
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    
    best_location = None
    best_match_rate = (1 << 63, 1 << 63)
    
    for location in LOCATIONS_ALLOWED:
        if location.level > user_level:
            continue
        
        match = pattern.search(location.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_rate = (match_start, match.end() - match_start)
        
        if best_match_rate <= match_rate:
            continue
        
        best_location = location
        best_match_rate = match_rate
        continue
    
    return best_location


def _location_match_sort_key_getter(item):
    """
    Gets sort key for a location and match rate pair.
    
    Parameters
    ----------
    item : ``(Location, (int, int, int))``
        Item to get sort key of.
    
    Returns
    -------
    sort_key : `(int, int, int)`
    """
    return item[1]


def get_matching_locations(value, user_level):
    """
    Gets all the location matching the given value.
    
    Parameters
    ----------
    value : `None | str`
        The value to match.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    locations : ``list<Location>``
    """
    if value is None:
        return [location for location in LOCATIONS_ALLOWED if location.level <= user_level]
    
    try:
        location_id = int(value, base = 16)
    except ValueError:
        pass
    else: 
        try:
            location = LOCATIONS[location_id]
        except KeyError:
            pass
        else:
            if location.level > user_level:
                return []
            
            return [location]
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    locations_with_match_rates = []
    
    for index, location in enumerate(LOCATIONS_ALLOWED):
        if location.level > user_level:
            continue
        
        match = pattern.search(location.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_length = match.end() - match_start
        
        locations_with_match_rates.append((location, (match_start, match_length, index)))
    
    locations_with_match_rates.sort(key = _location_match_sort_key_getter)
    return [item[0] for item in locations_with_match_rates]


def get_location_suggestions(value, user_level):
    """
    Gets location suggestions for the given value.
    
    Parameters
    ----------
    value : `None | str`
        The value to match.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    locations = get_matching_locations(value, user_level)
    del locations[25:]
    return [(location.name, format(location.id, 'x')) for location in locations]
