__all__ = ()

from random import choice, random

from ..touhou_character_preference import get_more_touhou_character_preference


OPTIMAL_GROUP_LENGTH = 10


async def get_preferred_image(image_handler, source_user, target_users):
    """
    This function is a coroutine.
    
    Parameters
    ----------
    image_handler : `ImageHandlerBase`
        Image handler.
    source_user : ``ClientUserBase``
        Source user.
    target_users : `list<ClientUserBase>`
        Target users(s).
    
    Returns
    -------
    selected : `None | ImageDetail`
        The selected image detail.
    """
    character_preferences = await get_more_touhou_character_preference(
        [source_user.id, *(user.id for user in target_users)],
    )
    if character_preferences is None:
        return None
    
    source_and_target_system_names = process_character_preferences(character_preferences, source_user)
    match_groups = get_match_groups(image_handler, *source_and_target_system_names)
    return select_from_match_groups(match_groups)


def process_character_preferences(character_preferences, source_user):
    """
    Processes character preferences grouping them into source characters to match and target characters to match.
    
    Parameters
    ----------
    character_preferences : `list<CharacterPreference>`
        Character preferences to process.
    
    Returns
    -------
    source_character_system_names : `None | set<str>`
    target_character_system_names : `None | set<str>`
    """
    source_user_id = source_user.id
    source_character_system_names = None
    target_character_system_names = None
    
    for character_preference in character_preferences:
        if character_preference.user_id == source_user_id:
            if source_character_system_names is None:
                source_character_system_names = set()
            
            source_character_system_names.add(character_preference.system_name)
        else:
            if target_character_system_names is None:
                target_character_system_names = set()
            
            target_character_system_names.add(character_preference.system_name)
    
    return source_character_system_names, target_character_system_names
    

def get_match_groups(image_handler, source_character_system_names, target_character_system_names):
    """
    Gets match groups.
    
    Parameters
    ----------
    image_handler : `ImageHandlerBase`
        Image handler.
    source_character_system_names : `None | set<str>`
        Character system names to match the source user.
    target_character_system_names : `None | set<str>`
        Character system names to match the target user.
    
    Returns
    -------
    match_groups : `tuple<list<ImageDetail>>`
        A tuple of image details. Image details at higher position in the tuple are matched better.
    """
    match_groups = ([], [])
    
    for image_detail in image_handler.iter_character_filterable():
        match_level = -1
        
        if (source_character_system_names is not None):
            match_level += any(
                (system_name in source_character_system_names) for system_name in
                image_detail.iter_source_character_system_names()
            )
        
        if (target_character_system_names is not None):
            match_level += any(
                (system_name in target_character_system_names) for system_name in
                image_detail.iter_target_character_system_names()
            )
        
        if match_level > -1:
            match_groups[match_level].append(image_detail)
    
    return match_groups


def select_from_match_groups(match_groups):
    """
    Selects an image from the match groups.
    
    Parameters
    ----------
    match_groups : `tuple<list<ImageDetail>>`
        A tuple of image details.
    
    Returns
    -------
    selected : `None | ImageDetail`
        The selected image detail.
    """
    for match_group in reversed(match_groups):
        match_group_length = len(match_group)
        if match_group_length >= OPTIMAL_GROUP_LENGTH or (random() * OPTIMAL_GROUP_LENGTH < match_group_length):
            return choice(match_group)
