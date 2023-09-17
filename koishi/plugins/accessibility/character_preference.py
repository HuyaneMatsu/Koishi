__all__ = ()

from hata import Embed


PREFERRED_CHARACTER_MAX = 3


def build_character_listing(character_preferences):
    """
    Builds character listing parts.
    
    Parameters
    ----------
    character_preferences : `None | list<CharacterPreference>`
        The user's character preferences if any.
    
    Returns
    -------
    character_listing : `str`
    """
    character_listing_parts = ['```\n']
    
    character_added = False
    
    if (character_preferences is not None):
        for character_preference in character_preferences:
            character = character_preference.get_character()
            if (character is not None):
                character_listing_parts.append(character.name)
                character_listing_parts.append('\n')
                character_added = True
    
    if not character_added:
        character_listing_parts.append('*none*\n')
    
    character_listing_parts.append('```')
    return ''.join(character_listing_parts)


def build_character_preference_embed(user, character_preferences):
    """
    Builds character preference embed for the given user.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to build the character preference for.
    character_preferences : `None | list<CharacterPreference>`
        The user's character preferences if any.
    """
    return Embed(
        'Character preferences',
        build_character_listing(character_preferences),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_character_preference_change_description(character, added):
    """
    Builds character preference change description.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The touhou character added / removed.
    added : `bool`
        Whether the character preference was added / removed.
    
    Returns
    -------
    description : `str`
    """
    if added:
        description = f'From now on {character.name} is associate with you.'
    else:
        description = f'From now on wont associate {character.name} with you.'
    
    return description


def build_character_preference_change_embed(user, character, added):
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
    embed : ``Embed``
    """
    return Embed(
        'Great success!',
        build_character_preference_change_description(character, added),
    ).add_thumbnail(
        user.avatar_url,
    )
