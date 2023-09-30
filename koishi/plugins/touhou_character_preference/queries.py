__all__ = (
    'add_touhou_character_to_preference',  'get_one_touhou_character_preference',
    'get_one_touhou_character_preference_with_connector', 'get_more_touhou_character_preference',
    'get_more_touhou_character_preference_with_connector', 'remove_touhou_character_from_preference',
)

from scarletio import copy_docs

from ...bot_utils.models import CHARACTER_PREFERENCE_TABLE, DB_ENGINE, character_preference_model

from .cache import (
    add_to_cache, get_more_from_cache, get_one_from_cache, put_more_to_cache, put_one_to_cache, remove_from_cache
)
from .character_preference import CharacterPreference
from .helpers import merge_results, should_add_touhou_character_preference, should_remove_touhou_character_preference


async def get_one_touhou_character_preference(user_id):
    """
    Gets character preference for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the preference for.
    
    Returns
    -------
    character_preferences : `None | list<CharacterPreference>`
    """
    character_preferences, miss = get_one_from_cache(user_id)
    if miss:
        character_preferences = await _query_one_touhou_character_preference(user_id)
        put_one_to_cache(user_id, character_preferences)
    
    return character_preferences


async def _query_one_touhou_character_preference(user_id):
    """
    Queries character preference for the given user identifier.
    used by ``get_one_touhou_character_preference`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the preference for.
    
    Returns
    -------
    character_preferences : `None | list<CharacterPreference>`
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_one_touhou_character_preference_with_connector(user_id, connector)


if DB_ENGINE is None:
    @copy_docs(_query_one_touhou_character_preference)
    async def _query_one_touhou_character_preference(user_id):
        return None


async def get_one_touhou_character_preference_with_connector(user_id, connector):
    """
    Gets character preference with the given connector for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the preference for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    character_preferences : `None | list<CharacterPreference>`
    """
    character_preferences, miss = get_one_from_cache(user_id)
    if miss:
        character_preferences = await _query_one_touhou_character_preference_with_connector(user_id, connector)
        put_one_to_cache(user_id, character_preferences)
    
    return character_preferences


async def _query_one_touhou_character_preference_with_connector(user_id, connector):
    """
    Queries character preference with the given connector for the given user identifier.
    used by ``get_one_touhou_character_preference_with_connector`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the preference for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    character_preferences : `None | list<CharacterPreference>`
    """
    response = await connector.execute(
        CHARACTER_PREFERENCE_TABLE.select().where(
            character_preference_model.user_id == user_id,
        )
    )
    
    if response.rowcount:
        entries = await response.fetchall()
        result = [CharacterPreference.from_entry(entry) for entry in entries]
    else:
        result = None
    
    return result


if DB_ENGINE is None:
    @copy_docs(_query_one_touhou_character_preference_with_connector)
    async def _query_one_touhou_character_preference_with_connector(user_id, connector):
        return None


async def get_more_touhou_character_preference(user_ids):
    """
    Gets character preferences for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the preference for.
    
    Returns
    -------
    character_preferences : `None | list<CharacterPreference>`
    """
    character_preferences, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge = await _query_more_touhou_character_preference(misses)
        put_more_to_cache(misses, to_merge)
        character_preferences = merge_results(character_preferences, to_merge)
    
    return character_preferences 


async def _query_more_touhou_character_preference(user_ids):
    """
    gets character preferences for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the preference for.
    
    Returns
    -------
    character_preferences : `None`, ``CharacterPreference``
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_more_touhou_character_preference_with_connector(user_ids, connector)


if DB_ENGINE is None:
    @copy_docs(_query_more_touhou_character_preference)
    async def _query_more_touhou_character_preference(user_ids, connector):
        return None


async def get_more_touhou_character_preference_with_connector(user_ids, connector):
    """
    Gets character preferences with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the preference for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    character_preferences : `None`, ``CharacterPreference``
    """

    character_preferences, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge = await _query_more_touhou_character_preference_with_connector(misses, connector)
        put_more_to_cache(misses, to_merge)
        character_preferences = merge_results(character_preferences, to_merge)
    
    return character_preferences 


async def _query_more_touhou_character_preference_with_connector(user_ids, connector):
    """
    Queries character preferences with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the preference for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    character_preferences : `None`, ``CharacterPreference``
    """
    response = await connector.execute(
        CHARACTER_PREFERENCE_TABLE.select().where(
            character_preference_model.user_id.in_(
                user_ids,
            ),
        )
    )
    
    if response.rowcount:
        entries = await response.fetchall()
        results = [CharacterPreference.from_entry(entry) for entry in entries]
    else:
        results = None
    
    return results


if DB_ENGINE is None:
    @copy_docs(_query_more_touhou_character_preference_with_connector)
    async def _query_more_touhou_character_preference_with_connector(user_ids, connector):
        return None


async def add_touhou_character_to_preference(user_id, character):
    """
    Adds the touhou character to the user's preference.
    If the character is already in teh user's preference does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    character : ``TouhouCharacter``
        The character to add to the preference.
    """
    character_preferences = await get_one_touhou_character_preference(user_id)
    if should_add_touhou_character_preference(character_preferences, character):
        character_preference = CharacterPreference(user_id, character.system_name)
        await _add_touhou_character_preference(character_preference)
        add_to_cache(character_preference)


async def _add_touhou_character_preference(character_preference):
    """
    Adds a character preference to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    character_preference : ``CharacterPreference``
        The character preference to add.
    """
    async with DB_ENGINE.connect() as connector:
        entry_id = character_preference.entry_id
        if entry_id == -1:
            # Add if new.
            response = await connector.execute(
                CHARACTER_PREFERENCE_TABLE.insert().values(
                    user_id = character_preference.user_id,
                    system_name = character_preference.system_name,
                ).returning(    
                    character_preference_model.id,
                )
            )
            
            # Update `.entry_id`
            entry = await response.fetchone()
            character_preference.entry_id = entry[0]
        
        else:
            # Update if exists. This branch should not happen.
            await connector.execute(
                CHARACTER_PREFERENCE_TABLE.update(
                    character_preference_model.id == entry_id,
                ).values(
                    user_id = character_preference.user_id,
                    system_name = character_preference.system_name,
                )
            )


if DB_ENGINE is None:
    @copy_docs(_add_touhou_character_preference)
    async def _add_touhou_character_preference(character_preference):
        return None


async def remove_touhou_character_from_preference(user_id, character):
    """
    Removes the touhou character from the user's preference.
    If the character isn ot in the preference, does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    character : ``TouhouCharacter``
        The character to remove from the preference.
    """
    character_preferences = await get_one_touhou_character_preference(user_id)
    character_preference =  should_remove_touhou_character_preference(character_preferences, character)
    if (character_preference is not None):
        await _remove_touhou_character_preference(character_preference)
        remove_from_cache(character_preference)


async def _remove_touhou_character_preference(character_preference):
    """
    Adds a character preference to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    character_preference : ``CharacterPreference``
        The character preference to add.
    """
    entry_id = character_preference.entry_id
    # Do nothing if the entry doesnt exists.
    if entry_id == -1:
        return
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            CHARACTER_PREFERENCE_TABLE.delete().where(
                character_preference_model.id == entry_id,
            )
        )


if DB_ENGINE is None:
    @copy_docs(_remove_touhou_character_preference)
    async def _remove_touhou_character_preference(character_preference):
        return None
