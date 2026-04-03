__all__ = ('build_character_preference_change_components', 'build_character_preference_components',)

from hata import Embed, create_text_display


def produce_character_listing(character_preferences):
    """
    Produces character listing parts.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    character_preferences : ``None | list<CharacterPreference>``
        The user's character preferences if any.
    
    Yields
    -------
    part : `str`
    """
    character_added = False
    
    if (character_preferences is not None):
        for character_preference in character_preferences:
            character = character_preference.get_character()
            if (character is None):
                continue
            
            if character_added:
                yield '\n'
            else:
                character_added = True
            
            yield character.name
    
    if not character_added:
        yield '*none*'


def build_character_preference_components(character_preferences):
    """
    Builds character preference embed for the given user.
    
    Parameters
    ----------
    character_preferences : ``None | list<CharacterPreference>``
        The user's character preferences if any.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_character_listing(character_preferences)]),
        ),
    ]


def produce_character_preference_change_description(character, added):
    """
    Produces character preference change description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The touhou character added / removed.
    
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    part : `str`
    """
    yield 'From now on '
    
    if not added:
        yield 'wont associate '
    
    yield '**'
    yield character.name
    yield '**'
    
    if added:
        yield ' is associate'
    
    yield ' with you.'


def build_character_preference_change_components(character, added):
    """
    Builds character preference change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's character preference were changed.
    
    character : ``TouhouCharacter``
        The touhou character added / removed.
    
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_character_preference_change_description(character, added)]),
        ),
    ]
