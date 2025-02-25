__all__ = ('can_gift', 'can_gift_with_request', 'identify_targeted_user',)

from ...bot_utils.constants import ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__ELEVATED

from ..relationships_core import (
    get_extender_relationship_and_relationship_and_user_like_at, get_relationship_to_deepen
)


def can_gift(source_user, relationship):
    """
    Returns whether the source user can gift to the target user.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    relationship : `None | Relationship`
        The relationship connecting the two users (can be extend).
    
    Returns
    -------
    can_gift : `bool`
    """
    return (
        (relationship is not None) or
        source_user.has_role(ROLE__SUPPORT__ELEVATED) or
        source_user.has_role(ROLE__SUPPORT__BOOSTER)
    )


async def can_gift_with_request(source_user, target_user):
    """
    Requests whether the source user can gift the target user (by identifier).
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    target_user : ``ClientUserBase``
        The gifted user.
    
    Returns
    -------
    can_gift : `bool`
    """
    relationship_to_deepen = await get_relationship_to_deepen(source_user.id, target_user.id)
    return can_gift(source_user, relationship_to_deepen)


async def identify_targeted_user(source_user, target_related_name, target_user, guild_id):
    """
    Identifies the target user from the given context.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is identifying the target user.
    
    target_related_name : `None | str`
        The targeted related user's name.
    
    target_user : `None | ClientUserBase``
        The targeted user's name.
    
    guild_id : `int`
        The targeted guild's name.
    
    Returns
    -------
    target_user : `None | ClientUserBase`
        The targeted user.
    
    relationship_to_deepen : `None | Relationship`
        The relationship to deepen by the action.
    """
    if source_user is target_user:
        target_user = None
    
    if (target_user is not None):
        relationship_to_deepen = await get_relationship_to_deepen(source_user.id, target_user.id)
    
    elif (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                source_user.id, target_related_name, guild_id
            )
        )
        
        if extender_relationship is None:
            relationship_to_deepen = relationship
        else:
            relationship_to_deepen = extender_relationship
    
    else:
        relationship_to_deepen = None
    
    return target_user, relationship_to_deepen
