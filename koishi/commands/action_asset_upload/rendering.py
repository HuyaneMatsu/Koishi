__all__ = ()


def _render_url_into(into, url):
    """
    Renders an url section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    url : `str`
        The url to render.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('TOUHOU_ACTION_ALL.add(\n    ')
    into.append(repr(url))
    into.append(',\n)')
    return into


def _render_action_internal_into(into, action_tag, source_character, target_character):
    """
    Renders an internal action part.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    action_tag : `str`
        The action tag to render.
    
    source_character : `None | TouhouCharacter`
        Source touhou character.
    
    target_character : `None | TouhouCharacter`
        Target touhou character.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('ACTION_TAG_')
    into.append(action_tag.upper())
    into.append(', ')
    
    if source_character is None:
        character_variable_name = 'None'
    else:
        character_variable_name = source_character.system_name.upper()
    into.append(character_variable_name)
    
    into.append(', ')
    
    if target_character is None:
        character_variable_name = 'None'
    else:
        character_variable_name = target_character.system_name.upper()
    into.append(character_variable_name)
    return into


def _render_single_action_into(into, action_tag, source_character, target_character):
    """
    Renders a single action tags section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    action_tag : `str`
        The action tag to render.
    
    source_character : `None | TouhouCharacter`
        Source touhou character.
    
    target_character : `None | TouhouCharacter`
        Target touhou character.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('.with_action(\n    ')
    into = _render_action_internal_into(into, action_tag, source_character, target_character)
    into.append(',\n)')
    return into


def _render_empty_action_tags_into(into, action_tags):
    """
    Renders an action tags section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    action_tags : `None | set<str>`
        Action tags to render.
    
    Returns
    -------
    into : `list<str>`
    """
    if (action_tags is not None):
        if len(action_tags) == 1:
            into = _render_single_action_into(into, next(iter(action_tags)), None, None)
        else:
            into.append('.with_actions(\n')
            
            for action_tag in sorted(action_tags):
                into.append('    (')
                into = _render_action_internal_into(into, action_tag, None, None)
                into.append('),\n')
            
            into.append(')')
    
    return into


def _render_characters_into(into, characters):
    """
    Renders a characters section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    characters : `None | set<TouhouCharacter>`
        The characters to render.
    
    Returns
    -------
    into : `list<str>`
    """
    if (characters is not None):
        into.append('.with_character')
        if len(characters) > 1:
            into.append('s')
        into.append('(\n')
        
        for character_name in sorted(character.system_name for character in characters):
            into.append('    ')
            into.append(character_name.upper())
            into.append(',\n')
        
        into.append(')')
    
    return into


def _render_creator_into(into, creator):
    """
    Renders a creator section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    creator : `None | str`
        Image creator.
    
    Returns
    -------
    into : `list<str>`
    """
    if (creator is not None):
        into.append('.with_creator(\n    ')
        into.append(repr(creator))
        into.append(',\n)')
    
    return into


def _render_to_do_into(into, unidentified):
    """
    Renders a to-do section.
    
    Parameters
    ----------
    into : `list<str>`
        Container render into.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('# TODO')
    
    if (unidentified is not None):
        for value in unidentified:
            into.append(' ')
            into.append(value)
    
    into.append('\n')
    
    return into


def renderer_single_source(characters, action_tags, unidentified, creator, url):
    """
    Renderer to render a single source action.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    creator : `None | str`
        The image's creator.
    
    url : `str`
        Url to the image.
    """
    into = []
    into = _render_url_into(into, url)
    into = _render_single_action_into(into, next(iter(action_tags)), next(iter(characters)), unidentified)
    into = _render_creator_into(into, creator)
    into.append('\n\n')
    return ''.join(into)


def renderer_default(characters, action_tags, unidentified, creator, url):
    """
    Renderer to render a default action.
    Adds a `TODO` at the start to identify that it needs manual adjustment.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    creator : `None | str`
        The image's creator.
    
    url : `str`
        Url to the image.
    """
    into = []
    into = _render_to_do_into(into, unidentified)
    into = _render_url_into(into, url)
    into = _render_empty_action_tags_into(into, action_tags)
    into = _render_characters_into(into, characters)
    into = _render_creator_into(into, creator)
    into.append('\n\n')
    return ''.join(into)


def is_single_source(characters, action_tags, unidentified):
    """
    Returns whether the given field combination can be used with single source renderer.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    is_single_source : `bool`
    """
    if (characters is None) or (action_tags is None) or (unidentified is not None):
        return False
    
    if len(characters) != 1 or len(action_tags) != 1:
        return False
    
    if next(iter(action_tags)) not in ('cry', 'happy', 'kon', 'stare', 'wave', 'wink'):
        return False
    
    return True


def get_renderer_for(characters, action_tags, unidentified):
    """
    Gets the correct renderer for the given fields.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        Touhou characters.
    
    action_tags : `None | set<str>`
        Action tags.
    
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    renderer : `FunctionType`
    """
    if is_single_source(characters, action_tags, unidentified):
        return renderer_single_source
    
    return renderer_default
