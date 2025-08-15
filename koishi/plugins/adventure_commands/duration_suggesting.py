__all__ = ()

from ..adventure_core import build_duration_suggestion

from re import I as re_ignore_case, compile as re_compile, escape as re_escape


def _duration_suggestion_sort_key_getter(item):
    """
    Gets sort key for a duration suggestion and sort match rate pair.
    
    Parameters
    ----------
    item : `((str, str), (int, int, int))`
        Item to get sort key of.
    
    Returns
    -------
    sort_key : `(int, int, int)`
    """
    return item[1]


def get_duration_suggestions(durations, value):
    """
    Gets the duration suggestions.
    
    Parameters
    ----------
    durations : `tuple<int>`
        Durations to get suggestions for.
    
    value : `None | str`
        Value to match for.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    duration_suggestions = [(build_duration_suggestion(duration), format(duration, 'x')) for duration in durations]
    if value is None:
        return duration_suggestions
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    
    duration_suggestions_with_match_rates = []
    
    for index, item in enumerate(duration_suggestions):
        match = pattern.search(item[0])
        if (match is None):
            continue
        
        match_start = match.start()
        match_length = match.end() - match_start
        
        duration_suggestions_with_match_rates.append((item, (match_start, match_length, index)))
    
    duration_suggestions_with_match_rates.sort(key = _duration_suggestion_sort_key_getter)
    return [item[0] for item in duration_suggestions_with_match_rates]
