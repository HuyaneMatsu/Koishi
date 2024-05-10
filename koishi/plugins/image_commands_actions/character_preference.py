__all__ = ()

from random import choice, random

from ...bot_utils.random import random_index

from ..image_handling_core import ImageDetailMatcherContextSensitive
from ..touhou_character_preference import get_more_touhou_character_preference


OPTIMAL_GROUP_LENGTH = 6


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
    selected : `None | ImageDetailBase`
        The selected image detail.
    """
    character_preferences = await get_more_touhou_character_preference(
        [source_user.id, *(user.id for user in target_users)],
    )
    if character_preferences is None:
        return None
    
    source_and_target_system_names = process_character_preferences(character_preferences, source_user)
    matcher = ImageDetailMatcherContextSensitive(*source_and_target_system_names)
    
    match_groups = get_match_groups(image_handler, matcher)
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


def get_match_groups(image_handler, matcher):
    """
    Gets match groups.
    
    Parameters
    ----------
    image_handler : `ImageHandlerBase`
        Image handler.
    matcher : ``ImageDetailMatcherBase``
        Matcher to use.
    
    Returns
    -------
    match_groups_by_weight : `dict<int, list<ImageDetailBase>>`
        The matched image details by weight.
    """
    match_groups_by_weight = {}
    
    for image_detail in image_handler.iter_character_filterable():
        match_rate = matcher.get_match_rate(image_detail)
        if match_rate <= 0:
            continue
        
        try:
            image_details = match_groups_by_weight[match_rate]
        except KeyError:
            image_details = []
            match_groups_by_weight[match_rate] = image_details
        
        image_details.append(image_detail)
    
    return match_groups_by_weight


def select_from_match_groups(match_groups_by_weight):
    """
    Selects an image from the match groups.
    
    Parameters
    ----------
    match_groups : `tuple<list<ImageDetailBase>>`
        A tuple of image details.
    
    Returns
    -------
    match_groups_by_weight : `dict<int, list<ImageDetailBase>>`
        The selected image detail.
    """
    if not match_groups_by_weight:
        return
    
    weights = []
    image_groups = []
    counter = 0
    
    for weight, images in sorted(match_groups_by_weight.items()):
        weights.append(weight * len(images))
        image_groups.append(images)
        counter += len(images)
        
        if counter >= OPTIMAL_GROUP_LENGTH:
            break
        
        continue
    
    else:
    # If we dont have enough images, randomly return
        if random() * OPTIMAL_GROUP_LENGTH > counter:
            return
    
    # Select image based on weights
    return choice(image_groups[random_index(weights)])
