__all__ = ()

from hata.ext.slash import abort

from ...bot_utils.user_getter import get_user

from ..relationship_slots_core import (
    build_component_invoke_relationship_slot_purchase_other, build_component_invoke_relationship_slot_purchase_self
)
from ..relationships_core import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_WAIFU, select_relationship
)

from .embed_builders import (
    build_failure_embed_already_proposing, build_failure_embed_already_related,
    build_failure_embed_insufficient_available_balance, build_failure_embed_insufficient_investment,
    build_failure_embed_insufficient_relationship_slots, build_failure_embed_self_propose,
    build_failure_embed_target_relationship_creation_disallowed, build_failure_embed_they_already_have_mama,
    build_failure_embed_they_already_have_mistress, build_failure_embed_they_already_have_waifu,
    build_failure_embed_you_already_have_mama, build_failure_embed_you_already_have_mistress,
    build_failure_embed_you_already_have_waifu, build_failure_embed_you_already_have_waifu_request
) 


def check_self_propose(source_user, target_user):
    """
    Checks whether source user is the same as the target user.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    Raises
    ------
    InteractionAbortedError
    """
    if source_user is not target_user:
        return
    
    abort(
        embed = build_failure_embed_self_propose(),
    )


def check_insufficient_available_balance(available_balance, investment):
    """
    Checks whether the available is insufficient.
    
    Parameters
    ----------
    available_balance : `int`
        The user' available balance.
    
    investment : `int`
        Investment to propose with.
    
    Raises
    ------
    InteractionAbortedError
    """
    if available_balance >= investment:
        return
    
    abort(
        embed = build_failure_embed_insufficient_available_balance(available_balance, investment),
    )


def check_already_related(relationship_listing, checked_at_creation, source_user, target_user, guild_id):
    """
    Checks whether the two users are already related.
    
    Parameters
    ----------
    relationship_listing : `None | list<Relationship>`
        The relationship_listing of one of the users.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (relationship_listing is None):
        return
    
    source_user_id = source_user.id
    target_user_id = target_user.id
    
    for relationship in relationship_listing:
        if relationship.source_user_id == source_user_id and relationship.target_user_id == target_user_id:
            outgoing = True
            break
        
        if relationship.target_user_id == source_user_id and relationship.source_user_id == target_user_id:
            outgoing = False
            break
    else:
        return
    
    abort(
        embed = build_failure_embed_already_related(
            relationship.relationship_type, outgoing, checked_at_creation, target_user, guild_id
        ),
    )


async def async_check_source_already_has_waifu(
    relationship_type, source_relationship_listing, checked_at_creation, source_user, target_user, guild_id
):
    """
    Checks whether the source user already has a waifu.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    source_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the source user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_type != RELATIONSHIP_TYPE_WAIFU:
        return
    
    relationship = select_relationship(source_user.id, RELATIONSHIP_TYPE_WAIFU, source_relationship_listing)
    if relationship is None:
        return
    
    waifu_id = relationship.source_user_id
    if waifu_id == source_user.id:
        waifu_id = relationship.target_user_id
    waifu = await get_user(waifu_id)
    
    if checked_at_creation:
        user = target_user
        embed_builder = build_failure_embed_you_already_have_waifu
    else:
        user = source_user
        embed_builder = build_failure_embed_they_already_have_waifu
    
    abort(
        embed = embed_builder(waifu, user, guild_id),
    )


def check_insufficient_relationship_slots(relationship_count, relationship_request_count, relationship_slots):
    """
    Checks whether the user has insufficient relationship slots.
    
    Parameters
    ----------
    relationship_count : `int`
        How much relationships the user has.
    
    relationship_request_count : `int`
        How much relationship requests the user has.
    
    relationship_slots : `int`
        How much relationships the user can have.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (relationship_count + relationship_request_count) < relationship_slots:
        return
    
    abort(
        embed = build_failure_embed_insufficient_relationship_slots(
            relationship_count, relationship_request_count, relationship_slots
        ),
        components = build_component_invoke_relationship_slot_purchase_self(),
    )


def check_already_proposing(source_relationship_request_listing, target_user, guild_id):
    """
    Checks whether the source user is already proposing to the target one.
    
    Parameters
    ----------
    source_relationship_request_listing : `None | list<RelationshipRequest>`
        The relationship requests of the source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (source_relationship_request_listing is None):
        return
    
    for relationship_request in source_relationship_request_listing:
        if relationship_request.target_user_id == target_user.id:
            break
    else:
        return
    
    abort(
        embed = build_failure_embed_already_proposing(
            relationship_request.relationship_type,
            relationship_request.investment,
            target_user,
            guild_id,
        ),
    )


def check_can_propose_to_bot(target_user, target_relationship_count, target_relationship_slots, guild_id):
    """
    Checks whether the source user is already proposing to the target one.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The target user.
    
    target_relationship_count : `int`
        The amount of relationships the target user have.
    
    target_relationship_slots : `int`
        The amount of relationships the target user can have.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if not target_user.bot:
        return
    
    if target_relationship_count < target_relationship_slots:
        return
    
    abort(
        embed = build_failure_embed_target_relationship_creation_disallowed(target_user, guild_id),
        components = build_component_invoke_relationship_slot_purchase_other(target_user.id),
    )


async def async_check_source_already_has_waifu_request(
    relationship_type, source_relationship_request_listing, target_user, guild_id
):
    """
    Checks whether the source user already has a waifu request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    source_relationship_request_listing : `None | list<RelationshipRequest>`
        The relationship requests of the source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (
        relationship_type != RELATIONSHIP_TYPE_WAIFU or
        (source_relationship_request_listing is None)
    ):
        return
    
    for relationship_request in source_relationship_request_listing:
        if relationship_request.relationship_type == RELATIONSHIP_TYPE_WAIFU:
            break
    else:
        return
    
    source_waifu = await get_user(relationship_request.target_user_id)
    
    abort(
        embed = build_failure_embed_you_already_have_waifu_request(source_waifu, target_user, guild_id),
    )


async def async_check_target_already_has_waifu(
    relationship_type, target_relationship_listing, checked_at_creation, source_user, target_user, guild_id
):
    """
    Checks whether the target user already has a waifu.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    target_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_type != RELATIONSHIP_TYPE_WAIFU:
        return
    
    relationship = select_relationship(target_user.id, RELATIONSHIP_TYPE_WAIFU, target_relationship_listing)
    if relationship is None:
        return
    
    waifu_id = relationship.source_user_id
    if waifu_id == target_user.id:
        waifu_id = relationship.target_user_id
    waifu = await get_user(waifu_id)
    
    if checked_at_creation:
        user = target_user
        embed_builder = build_failure_embed_they_already_have_waifu
    else:
        user = source_user
        embed_builder = build_failure_embed_you_already_have_waifu
    
    abort(
        embed = embed_builder(waifu, user, guild_id),
    )


async def async_check_target_already_has_mistress(
    relationship_type, target_relationship_listing, checked_at_creation, source_user, target_user, guild_id
):
    """
    Checks whether the target user already has a mistress.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    target_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_type != RELATIONSHIP_TYPE_MISTRESS:
        return
    
    relationship = select_relationship(target_user.id, RELATIONSHIP_TYPE_MISTRESS, target_relationship_listing)
    if relationship is None:
        return
    
    mistress_id = relationship.source_user_id
    if mistress_id == target_user.id:
        mistress_id = relationship.target_user_id
    mistress = await get_user(mistress_id)
    
    if checked_at_creation:
        user = target_user
        embed_builder = build_failure_embed_they_already_have_mistress
    else:
        user = source_user
        embed_builder = build_failure_embed_you_already_have_mistress
    
    abort(
        embed = embed_builder(mistress, user, guild_id),
    )


async def async_check_target_already_has_mama(
    relationship_type, target_relationship_listing, checked_at_creation, source_user, target_user, guild_id
):
    """
    Checks whether the target user already has a mama.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    target_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_type != RELATIONSHIP_TYPE_MAMA:
        return
    
    relationship = select_relationship(target_user.id, RELATIONSHIP_TYPE_MAMA, target_relationship_listing)
    if relationship is None:
        return
    
    mama_id = relationship.source_user_id
    if mama_id == target_user.id:
        mama_id = relationship.target_user_id
    mama = await get_user(mama_id)
    
    if checked_at_creation:
        user = target_user
        embed_builder = build_failure_embed_they_already_have_mama
    else:
        user = source_user
        embed_builder = build_failure_embed_you_already_have_mama
    
    abort(
        embed = embed_builder(mama, user, guild_id),
    )


def check_insufficient_investment(relationship_value, investment):
    """
    Checks whether the user's investment is insufficient.
    
    Parameters
    ----------
    relationship_value : `int`
        The minimal value the user needs to propose with to start the relationship.
    
    investment : `int`
        Investment to propose with.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_value <= investment:
        return
    
    return abort(
        embed = build_failure_embed_insufficient_investment(relationship_value, investment)
    )
