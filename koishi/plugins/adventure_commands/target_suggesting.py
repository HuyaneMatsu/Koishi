__all__ = ()

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from ..adventure_core import TARGETS


def get_best_matching_target(target_ids, value):
    """
    Gets the best matching target for the given value.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter for.
    
    value : `None | str`
        The value to match.
    
    Returns
    -------
    target : ``None | Target``
    """
    if value is None:
        return None
    
    try:
        target_id = int(value, base = 16)
    except ValueError:
        pass
    else:
        for allowed_target_id in target_ids:
            if allowed_target_id == target_id:
                try:
                    target = TARGETS[allowed_target_id]
                except KeyError:
                    break
                
                return target
                    
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    
    best_target = None
    best_match_rate = (1 << 63, 1 << 63)
    
    for allowed_target_id in target_ids:
        try:
            target = TARGETS[allowed_target_id]
        except KeyError:
            continue
        
        match = pattern.search(target.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_rate = (match_start, match.end() - match_start)
        
        if best_match_rate <= match_rate:
            continue
        
        best_target = target
        best_match_rate = match_rate
        continue
    
    return best_target


def _target_match_sort_key_getter(item):
    """
    Gets sort key for a target and match rate pair.
    
    Parameters
    ----------
    item : ``(Target, (int, int, int))``
        Item to get sort key of.
    
    Returns
    -------
    sort_key : `(int, int, int)`
    """
    return item[1]


def get_matching_targets(target_ids, value):
    """
    Gets all the target matching the given value.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter for.
    
    value : `None | str`
        The value to match.
    
    Returns
    -------
    targets : ``list<Target>``
    """
    if value is None:
        targets = []
        
        for allowed_target_id in target_ids:
            try:
                target = TARGETS[allowed_target_id]
            except KeyError:
                continue
            
            targets.append(target)
        
        return targets
    
    try:
        target_id = int(value, base = 16)
    except ValueError:
        pass
    else: 
        for allowed_target_id in target_ids:
            if allowed_target_id == target_id:
                try:
                    target = TARGETS[allowed_target_id]
                except KeyError:
                    break
                
                return [target]
                
    
    pattern = re_compile('.*?'.join(re_escape(character) for character in value), re_ignore_case)
    targets_with_match_rates = []
    
    for index, allowed_target_id in enumerate(target_ids):
        try:
            target = TARGETS[allowed_target_id]
        except KeyError:
            continue
        
        match = pattern.search(target.name)
        if (match is None):
            continue
        
        match_start = match.start()
        match_length = match.end() - match_start
        
        targets_with_match_rates.append((target, (match_start, match_length, index)))
    
    targets_with_match_rates.sort(key = _target_match_sort_key_getter)
    return [item[0] for item in targets_with_match_rates]


def get_target_suggestions(target_ids, value):
    """
    Gets target suggestions for the given value.
    
    Parameters
    ----------
    target_ids : `tuple<int>`
        Target identifiers to filter for.
    
    value : `None | str`
        The value to match.
    
    Returns
    -------
    suggestions : `(str, str)`
    """
    targets = get_matching_targets(target_ids, value)
    del targets[25:]
    return [(target.name, format(target.id, 'x')) for target in targets]
