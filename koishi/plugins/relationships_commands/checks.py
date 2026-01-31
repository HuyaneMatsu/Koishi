__all__ = ()

from hata import create_row, create_text_display

from ...bot_utils.user_getter import get_user
from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ..gift_common import can_gift_with_request
from ..relationship_slots_core import (
    build_component_invoke_relationship_slot_purchase_other, build_component_invoke_relationship_slot_purchase_self
)
from ..relationships_core import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_WAIFU, select_relationship,
    RELATIONSHIP_TYPE_RELATIONSHIPS, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_NONE,
    RELATIONSHIP_TYPE_UNSET
)

from .constants import ACTION_NAME_UNKNOWN


def check_self_propose(source_user, target_user):
    """
    Checks whether source user is the same as the target user.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if source_user is not target_user:
        return
    
    return [
        create_text_display('You cannot propose to yourself.')
    ]


def check_insufficient_available_balance(available_balance, investment):
    """
    Checks whether the available is insufficient.
    
    Parameters
    ----------
    available_balance : `int`
        The user' available balance.
    
    investment : `int`
        Investment to propose with.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if available_balance >= investment:
        return
    
    return [
        create_text_display(
            f'You have {available_balance} available {EMOJI__HEART_CURRENCY} '
            f'which is lower than {investment} {EMOJI__HEART_CURRENCY}.'
        ),
    ]


def check_already_related(
    relationship_type, relationship, checked_at_creation, source_user, target_user, guild_id
):
    """
    Checks whether the two users are already related.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
    
    relationship : ``None | Relationship``
        The existing relationship between the two users.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if (relationship is None):
        return
    
    existing_relationship_type = relationship.relationship_type
    
    if (relationship.source_user_id == source_user.id) ^ checked_at_creation:
        existing_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(
            existing_relationship_type, RELATIONSHIP_TYPE_NONE
        )
    
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        if existing_relationship_type & RELATIONSHIP_TYPE_WAIFU:
            concept = 'married to'
        else:
            concept = None
    elif (relationship_type == RELATIONSHIP_TYPE_SISTER_LIL) or (relationship_type == RELATIONSHIP_TYPE_SISTER_BIG):
        if existing_relationship_type & RELATIONSHIP_TYPE_SISTER_LIL:
            concept = 'the little sister of'
        elif existing_relationship_type & RELATIONSHIP_TYPE_SISTER_BIG:
            concept = 'the big sister of'
        else:
            concept = None
    elif (relationship_type == RELATIONSHIP_TYPE_MAMA) or (relationship_type == RELATIONSHIP_TYPE_DAUGHTER):
        if existing_relationship_type & RELATIONSHIP_TYPE_MAMA:
            concept = 'the mama of'
        elif existing_relationship_type & RELATIONSHIP_TYPE_DAUGHTER:
            concept = 'the daughter of'
        else:
            concept = None
    elif (relationship_type == RELATIONSHIP_TYPE_MAMA) or (relationship_type == RELATIONSHIP_TYPE_DAUGHTER):
        if existing_relationship_type & RELATIONSHIP_TYPE_MISTRESS:
            concept = 'the mistress of'
        elif existing_relationship_type & RELATIONSHIP_TYPE_MAID:
            concept = 'the maid of'
        else:
            concept = None
    elif (relationship_type == RELATIONSHIP_TYPE_UNSET):
        if existing_relationship_type & RELATIONSHIP_TYPE_UNSET:
            concept = 'related to'
        else:
            concept = None
    else:
        concept = None
    
    if (concept is None):
        return
    
    return [
        create_text_display(
            f'You are already {concept} {target_user.name_at(guild_id)}.'
        ),
    ]


async def async_check_source_already_has_waifu(
    relationship_type, source_relationship_listing, checked_at_creation, source_user, guild_id
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
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
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
    
    return [
        create_text_display(
            f'{"You" if checked_at_creation else source_user.name_at(guild_id)} '
            f'{"are" if checked_at_creation else "is"} already married to {waifu.name_at(guild_id)}!'
        ),
    ]


def check_insufficient_relationship_slots(
    relationship_count, relationship_request_count, already_related, relationship_slots
):
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
    
    already_related : `bool`
        Whether the two users are already related.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if (max(relationship_count - already_related, 0) + relationship_request_count) < relationship_slots:
        return
    
    return [
        create_text_display(
            f'You do not have enough available relationship slots.\n'
            f'You have {relationship_slots} relationship slots from which '
            f'{relationship_count} is occupied by relationships and '
            f'{relationship_request_count} is occupied by relationship requests.'
        ),
        create_row(
            build_component_invoke_relationship_slot_purchase_self(),
        ),
    ]


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
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if (source_relationship_request_listing is None):
        return
    
    for relationship_request in source_relationship_request_listing:
        if relationship_request.target_user_id == target_user.id:
            break
    else:
        return
    
    relationship_type = relationship_request.relationship_type
    investment = relationship_request.investment
    
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'a marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'a blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'an adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'an employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return [
        create_text_display(
            f'You have already sent {concept} towards {target_user.name_at(guild_id)} '
            f'with {investment} {EMOJI__HEART_CURRENCY}.\n'
            f'Cancel the old proposal before reissuing a new one.'
        ),
    ]


async def async_check_can_propose_to_bot(
    source_user, target_user, target_relationship_count, target_relationship_slots, guild_id
):
    """
    Checks whether the source user is already proposing to the target one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    target_relationship_count : `int`
        The amount of relationships the target user have.
    
    target_relationship_slots : `int`
        The amount of relationships the target user can have.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if not target_user.bot:
        return
    
    if target_relationship_count < target_relationship_slots:
        return
    
    components = [
        create_text_display(
            f'{target_user.name_at(guild_id)} is disallowed to create relationships.\n'
            f'Therefore creating a proposal towards them is not allowed.'
        ),
    ]
    
    if (await can_gift_with_request(source_user, target_user)):
        components.append(
            create_row(
                build_component_invoke_relationship_slot_purchase_other(target_user.id),
            ),
        )
    
    return components


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
    
    Returns
    -------
    error_components : ``None | list<Component>``
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
    
    return [
        create_text_display(
            f'What would {source_waifu.name_at(guild_id)} say if they would know about '
            f'{target_user.name_at(guild_id)}?'
        ),
    ]


async def async_check_target_already_has_waifu(
    relationship_type, target_relationship_listing, checked_at_creation, target_user, guild_id
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
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
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
    
    return [
        create_text_display(
            f'{target_user.name_at(guild_id) if checked_at_creation else "You"} '
            f'{"is" if checked_at_creation else "are"} already married to {waifu.name_at(guild_id)}!'
        ),
    ]


async def async_check_target_already_has_mistress(
    relationship_type, target_relationship_listing, checked_at_creation, target_user, guild_id
):
    """
    Checks whether the target user already has a mistress.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    target_relationship_listing : ``None | list<Relationship>``
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
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
    
    # Yupp, python does not allow inlining this into the f string
    target_postfix = '\'s' if checked_at_creation else ''
    
    return [
        create_text_display(
            f'{target_user.name_at(guild_id) if checked_at_creation else "Your"}{target_postfix} '
            f'mistress is {mistress.name_at(guild_id)}, therefore they cannot serve you.'
        ),
    ]


async def async_check_target_already_has_mama(
    relationship_type, target_relationship_listing, checked_at_creation, target_user, guild_id
):
    """
    Checks whether the target user already has a mama.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
     
    target_relationship_listing : ``None | list<Relationship>``
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    error_components : ``None | list<Component>``
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
    
    # Yupp, python does not allow inlining this into the f string
    target_postfix = '\'s' if checked_at_creation else ''
    
    return [
        create_text_display(
            f'{target_user.name_at(guild_id) if checked_at_creation else "Your"}{target_postfix} '
            f'mama is {mama.name_at(guild_id)}, therefore you cannot adopt them.'
        ),
    ]


def check_insufficient_investment(relationship_value, investment):
    """
    Checks whether the user's investment is insufficient.
    
    Parameters
    ----------
    relationship_value : `int`
        The minimal value the user needs to propose with to start the relationship.
    
    investment : `int`
        Investment to propose with.
    
    Returns
    -------
    error_components : ``None | list<Component>``
    """
    if relationship_value <= investment:
        return
    
    return [
        create_text_display(
            f'Your investment {investment} {EMOJI__HEART_CURRENCY} is lower than the required '
            f'{relationship_value} {EMOJI__HEART_CURRENCY}.'
        )
    ]
