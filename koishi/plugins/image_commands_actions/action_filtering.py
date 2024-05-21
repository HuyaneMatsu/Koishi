__all__ = ()

from ..image_handling_core import ImageDetailMatcherCustom
from ..touhou_core import get_touhou_character_like, get_touhou_character_names_like_from

from .actions import ACTIONS
from .asset_listings import TOUHOU_ACTION_ALL


SELF_CALL_POSTFIX = ' (self)'

PARAMETER_WILD_CARD = 'null'

PARAMETER_NAME_ACTION_TAG = 'action'
PARAMETER_NAME_SOURCE = 'source'
PARAMETER_NAME_TARGET = 'target'
PARAMETER_NAME_NAME = 'image'


ACTION_TAG_TO_ACTION = {}
ACTION_NAME_TO_TAG = {}
ACTION_TAG_TO_NAME = {}

for action in ACTIONS:
    action_tag = action.get_action_tag()
    if (action_tag is not None):
        name = action.name
        ACTION_NAME_TO_TAG[name] = action_tag
        ACTION_TAG_TO_NAME[action_tag] = name
        ACTION_TAG_TO_ACTION[action_tag] = action
    
    action_tag = action.get_action_tag_self()
    if (action_tag is not None):
        name = action.name + SELF_CALL_POSTFIX
        ACTION_NAME_TO_TAG[name] = action_tag
        ACTION_TAG_TO_NAME[action_tag] = name
        ACTION_TAG_TO_ACTION[action_tag] = action


# cleanup
del action
del action_tag
del name


def get_selected_action_tag(action_tag_name):
    """
    Gets the selected name from the given parameters.
    
    Parameters
    ----------
    action_tag_name : `None | str`
        Action tag name to get action tag for.
    
    Returns
    -------
    action_tag : `None | str`
    """
    if (action_tag_name is None):
        return None
    
    action_tag_name = action_tag_name.casefold()
    if action_tag_name == PARAMETER_WILD_CARD:
        return None
    
    action_tag = ACTION_NAME_TO_TAG.get('action_tag_name', None)
    if (action_tag is not None):
        return action_tag
    
    action_tags = []
    for action_name, action_tag in ACTION_NAME_TO_TAG.items():
        if action_name.startswith(action_tag_name):
            action_tags.append(action_tag)
    
    if not action_tags:
        return
    
    action_tags.sort()
    return action_tags[0]


def get_selected_character(character_name):
    """
    Gets the selected touhou character from the given parameters.
    
    Parameters
    ----------
    character_name : `None | str`
        Character name to get character for.
    
    Returns
    -------
    character : `None | TouhouCharacter`
    """
    if (character_name is None):
        return None
    
    character_name = character_name.casefold()
    if character_name == PARAMETER_WILD_CARD:
        return None
    
    return get_touhou_character_like(character_name)


def get_selected_name(name):
    """
    Gets the selected name from the given parameters.
    
    Parameters
    ----------
    name : `None | str`
        Image name.
    
    Returns
    -------
    name : `None | str`
    """
    if name is None:
        return None
    
    name = name.casefold()
    if name == PARAMETER_WILD_CARD:
        return None
    
    return name


def get_image_details_from_parameters(parameters):
    """
    Filters the applicable image details for the given parameters.
    
    Parameters
    ----------
    parameters : `dict<str, object>`
        Parameters to filter for.
    
    Returns
    -------
    source : `None | TouhouCharacter`
    target : `None | TouhouCharacter`
    image_details : `list<ImageDetailBase>`
    """
    action_tag = get_selected_action_tag(parameters.get(PARAMETER_NAME_ACTION_TAG, None))
    source = get_selected_character(parameters.get(PARAMETER_NAME_SOURCE, None))
    target = get_selected_character(parameters.get(PARAMETER_NAME_TARGET, None))
    name = get_selected_name(parameters.get(PARAMETER_NAME_NAME, None))
    
    matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    image_details = [
        image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
        if matcher.get_match_rate(image_detail)
    ]
    return source, target, image_details


def get_character_suggestions(characters, allow_wild_card, input_value):
    """
    Gets character suggestions for the given characters.
    
    Parameters
    ----------
    characters : `set<TouhouCharacter>`
        Characters to auto complete from.
    allow_wild_card : `bool`
        Whether wild card option is allowed.
    input_value : `None`, `str`
        Characters to auto complete from.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    if not characters:
        if allow_wild_card:
            return [PARAMETER_WILD_CARD]
        
        return None
    
    if input_value is None:
        suggestions = sorted(character.name for character in characters)
        suggestions.insert(0, PARAMETER_WILD_CARD)
        return suggestions
    
    return get_touhou_character_names_like_from(input_value, characters)


async def autocomplete_action_tag(event, input_value):
    """
    Auto completes the given action tag.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    input_value : `None`, `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None`, `list<str>`
    """
    parameters = event.get_non_focused_values()
    
    # This parameter is propagated first to the user, so we expect that they fill this first too.
    if not parameters:
        if input_value is None:
            suggestions = sorted(ACTION_NAME_TO_TAG.keys())
            suggestions.insert(0, PARAMETER_WILD_CARD)
            return suggestions
        
        return sorted(
            action_tag_name for action_tag_name in ACTION_NAME_TO_TAG.keys()
            if action_tag_name.startswith(input_value)
        )
    
    source, target, image_details = get_image_details_from_parameters(parameters)
    
    action_tags = set()
    for image_detail in image_details:
        for action in image_detail.iter_actions():
            action_tags.add(action.tag)
    
    if not action_tags:
        return None
    
    action_tag_names = [
        action_tag_name for action_tag_name
        in (ACTION_TAG_TO_NAME.get(action_tag, None) for action_tag in action_tags) 
        if (action_tag_name is not None)
    ]
    if input_value is None:
        action_tag_names.sort()
        action_tag_names.insert(0, PARAMETER_WILD_CARD)
        return action_tag_names
    
    return sorted(
        action_tag_name for action_tag_name in action_tag_names
        if action_tag_name.startswith(input_value)
    )


async def autocomplete_source(event, input_value):
    """
    Auto completes the given source.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    input_value : `None`, `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None`, `list<str>`
    """
    source, target, image_details = get_image_details_from_parameters(event.get_non_focused_values())
    
    characters = set()
    allow_wild_card = False
    
    for image_detail in image_details:
        for action in image_detail.iter_actions():
            action_source = action.source
            if (action_source is None):
                allow_wild_card = True
                continue
            
            if (target is not None) and (target is not action.target):
                continue
            
            characters.add(action_source)
    
    return get_character_suggestions(characters, allow_wild_card, input_value)


async def autocomplete_target(event, input_value):
    """
    Auto completes the given target.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    input_value : `None`, `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None`, `list<str>`
    """
    source, target, image_details = get_image_details_from_parameters(event.get_non_focused_values())
    
    characters = set()
    allow_wild_card = False
    
    for image_detail in image_details:
        for action in image_detail.iter_actions():
            action_target = action.target
            if (action_target is None):
                allow_wild_card = True
                continue
            
            if (source is not None) and (source is not action.source):
                continue
            
            characters.add(action_target)
    
    return get_character_suggestions(characters, allow_wild_card, input_value)


async def autocomplete_name(event, input_value):
    """
    Auto completes the given name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    input_value : `None`, `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None`, `list<str>`
    """
    source, target, image_details = get_image_details_from_parameters(event.get_non_focused_values())
    
    names = [image_detail.name for image_detail in image_details]
    
    if not names:
        return None
    
    if input_value is None:
        names.sort()
        names.insert(0, PARAMETER_WILD_CARD)
        return names
    
    return sorted(name for name in names if name.startswith(input_value))


def _image_detail_sort_key(image_detail):
    """
    Sort key used for image detail sorting by name.
    
    Parameters
    ----------
    image_detail : ``ImageDetailBase``
        Image detail to get its sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return image_detail.name


def get_action_and_image_detail(action_tag_name, source_character_name, target_character_name, image_name):
    """
    Gets action and the first matching image detail.
    
    Parameters
    ----------
    action_tag_name : `None | str`
        Selected action tag name.
    source_character_name : `None | str`
        Name of the source character.
    target_character_name : `None | str`
        Name of the target character.
    image_name : `None | str`
        The name of the image.
    
    Returns
    -------
    action : `None | Action`
    image_detail : `None | ImageDetailBase`
    """
    action_tag = get_selected_action_tag(action_tag_name)
    action = ACTION_TAG_TO_ACTION.get(action_tag, None)
    
    source = get_selected_character(source_character_name)
    target = get_selected_character(target_character_name)
    name = get_selected_name(image_name)
    
    matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    image_details = [
        image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
        if matcher.get_match_rate(image_detail)
    ]
    if not image_details:
        image_detail = None
    else:
        image_details.sort(key = _image_detail_sort_key)
        image_detail = image_details[0]
        
        if action is None:
            for action in image_detail.iter_actions():
                action = ACTION_TAG_TO_ACTION.get(action.tag, None)
                break
    
    return action, image_detail
