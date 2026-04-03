__all__ = ()

def merge_results(results_0, results_1):
    """
    Merges results.
    
    Parameters
    ----------
    results_0 : `None | list<CharacterPreference>`
        Results to merge.
    results_1 : `None | list<CharacterPreference>`
        Results to merge.
    
    Returns
    -------
    results : `None | list<CharacterPreference>`
    """
    if results_0 is None:
        return results_1
    
    if results_1 is None:
        return results_0
    
    results_0.extend(results_1)
    return results_0


def should_add_touhou_character_preference(character_preferences, character):
    """
    Checks whether touhou character preference should be added.
    
    Parameters
    ----------
    character_preferences : `None | list<CharacterPreference>`
        The user's actual character preferences.
    character : ``TouhouCharacter``
        Touhou character to add as a preference.
    
    Returns
    -------
    should_add : `bool`
    """
    if character_preferences is None:
        return True
    
    system_name = character.system_name
    for character_preference in character_preferences:
        if system_name == character_preference.system_name:
            return False
    
    return True


def should_remove_touhou_character_preference(character_preferences, character):
    """
    Checks which touhou character preference should be removed.
    
    Parameters
    ----------
    character_preferences : `None | list<CharacterPreference>`
        The user's actual character preferences.
    character : ``TouhouCharacter``
        Touhou character to add as a preference.
    
    Returns
    -------
    should_remove : `None | CharacterPreference`
    """
    if character_preferences is None:
        return None
    
    system_name = character.system_name
    for character_preference in character_preferences:
        if system_name == character_preference.system_name:
            return character_preference
    
    return None
