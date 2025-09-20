__all__ = ()


ACTION_TAGS_SINGLE_SOURCE = ('cry', 'happy', 'kon', 'stare', 'wave', 'wink')
ACTION_TAGS_SELF_TARGET = ('pocky_self', 'feed_self')
ACTION_TAGS_CROSS_TARGET = ('handhold',)


def _produce_url(url):
    """
    Produces an url section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    url : `str`
        The url to produce.
    
    Yields
    ------
    part : `str`
    """
    yield 'TOUHOU_ACTION_ALL.add(\n    '
    yield repr(url)
    yield ',\n)'


def _produce_action_internal(action_tag, source_character, target_character):
    """
    produces an internal action part.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    source_character : `None | TouhouCharacter`
        Source touhou character.
    
    target_character : `None | TouhouCharacter`
        Target touhou character.
    
    Yields
    ------
    part : `str`
    """
    yield 'ACTION_TAG_'
    yield action_tag.upper()
    yield ', '
    
    if source_character is None:
        character_variable_name = 'None'
    else:
        character_variable_name = source_character.system_name.upper()
    yield character_variable_name
    
    yield ', '
    
    if target_character is None:
        character_variable_name = 'None'
    else:
        character_variable_name = target_character.system_name.upper()
    yield character_variable_name


def _produce_single_action(action_tag, source_character, target_character):
    """
    Produces a single action tags section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_tag : `str`
        The action tag to produce.
    
    source_character : `None | TouhouCharacter`
        Source touhou character.
    
    target_character : `None | TouhouCharacter`
        Target touhou character.
    
    Yields
    ------
    part : `str`
    """
    yield '.with_action(\n    '
    yield from _produce_action_internal(action_tag, source_character, target_character)
    yield ',\n)'


def _produce_multiple_action(*items):
    """
    Produces a multiple action tags section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    *items : `(str, None | TouhouCharacter, None | TouhouCharacter)`
        Action items to produce.
    
    Yields
    ------
    part : `str`
    """
    yield '.with_actions(\n'
    for item in items:
        yield '    ('
        yield from _produce_action_internal(*item)
        yield '),\n'
    yield ')'


def _produce_empty_action_tags(action_tags):
    """
    Renders an action tags section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    action_tags : `None | set<str>`
        Action tags to produce.
    
    Yields
    ------
    part : `str`
    """
    if (action_tags is not None):
        if len(action_tags) == 1:
            yield from _produce_single_action(next(iter(action_tags)), None, None)
        else:
            yield '.with_actions(\n'
            
            for action_tag in sorted(action_tags):
                yield '    ('
                yield from _produce_action_internal(action_tag, None, None)
                yield '),\n'
            
            yield ')'


def _produce_characters(characters):
    """
    Renders a characters section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        The characters to produce.
    
    Yields
    ------
    part : `str`
    """
    if (characters is not None):
        yield '.with_character'
        if len(characters) > 1:
            yield 's'
        yield '(\n'
        
        for character_name in sorted(character.system_name for character in characters):
            yield '    '
            yield character_name.upper()
            yield ',\n'
        
        yield ')'


def _produce_creator(creator):
    """
    Renders a creator section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    creator : `None | str`
        Image creator.
    
    Yields
    ------
    part : `str`
    """
    if (creator is not None):
        yield '.with_creator(\n    '
        yield repr(creator)
        yield ',\n)'


def _produce_to_do(unidentified):
    """
    Renders a to-do section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Yields
    ------
    part : `str`
    """
    yield '# TODO'
    
    if (unidentified is not None):
        for value in sorted(unidentified):
            yield ' '
            yield value
    
    yield '\n'


def producer_single_source(characters, action_tags, unidentified, creator, url):
    """
    Produces a single source action.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_url(url)
    character = next(iter(characters))
    yield from _produce_single_action(next(iter(action_tags)), character, None)
    yield from _produce_creator(creator)
    yield '\n\n'


def producer_self_target(characters, action_tags, unidentified, creator, url):
    """
    Produces a self targeting action.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_url(url)
    character = next(iter(characters))
    yield from _produce_single_action(next(iter(action_tags)), character, character)
    yield from _produce_creator(creator)
    yield '\n\n'


def producer_cross_target(characters, action_tags, unidentified, creator, url):
    """
    Produces a cross targeting action.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_url( url)
    
    character_0, character_1 = characters
    if character_0.system_name > character_1.system_name:
        character_0, character_1 = character_1, character_0
    
    tag, = action_tags
        
    yield from _produce_multiple_action(
        (tag, character_0, character_1),
        (tag, character_1, character_0),
    )
    yield from _produce_creator(creator)
    yield '\n\n'


def producer_default(characters, action_tags, unidentified, creator, url):
    """
    Produces a default action.
    Adds a `TODO` at the start to identify that it needs manual adjustment.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_to_do(unidentified)
    yield from _produce_url(url)
    yield from _produce_empty_action_tags(action_tags)
    yield from _produce_characters(characters)
    yield from _produce_creator(creator)
    yield '\n\n'


def is_single_source(characters, action_tags, unidentified):
    """
    Returns whether the given field combination can be used with a single source no target producer.
    
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
    
    if next(iter(action_tags)) not in ACTION_TAGS_SINGLE_SOURCE:
        return False
    
    return True


def is_self_target(characters, action_tags, unidentified):
    """
    Returns whether the given field combination can be used with self targeting producer.
    
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
    is_self_target : `bool`
    """
    if (characters is None) or (action_tags is None) or (unidentified is not None):
        return False
    
    if len(characters) != 1 or len(action_tags) != 1:
        return False
    
    if next(iter(action_tags)) not in ACTION_TAGS_SELF_TARGET:
        return False
        
    return True


def is_cross_target(characters, action_tags, unidentified):
    """
    Returns whether the given field combination can be used with cross targeting producer.
    
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
    is_cross_target : `bool`
    """
    if (characters is None) or (action_tags is None) or (unidentified is not None):
        return False
    
    if len(characters) != 2 or len(action_tags) != 1:
        return False
    
    if next(iter(action_tags)) not in ACTION_TAGS_CROSS_TARGET:
        return False
        
    return True


def get_producer_for(characters, action_tags, unidentified):
    """
    Gets the correct producer for the given fields.
    
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
    producer : `GeneratorFunctionType`
    """
    if is_single_source(characters, action_tags, unidentified):
        return producer_single_source
    
    if is_self_target(characters, action_tags, unidentified):
        return producer_self_target
    
    if is_cross_target(characters, action_tags, unidentified):
        return producer_cross_target
    
    return producer_default
