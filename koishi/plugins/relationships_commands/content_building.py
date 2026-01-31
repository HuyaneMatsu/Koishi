__all__ = ()


from math import floor

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..relationships_core import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS,
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU, get_affinity_multiplier,
    get_relationship_request_type_concept, get_relationship_type_name_basic
)

from .constants import (
    ACTION_NAME_UNKNOWN, RELATIONSHIP_LISTING_MODE_LEGACY, RELATIONSHIP_LISTING_MODE_LONG,
    RELATIONSHIP_LISTING_MODE_WIDE
)


def _get_relationship_request_action_concept(relationship_type):
    """
    Helper function to get relationship request action concept name.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    Returns
    -------
    concept : `str`
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'marry'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'have a blood-pact with'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'adopt'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'employ'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return concept


def _get_relationship_request_concept(relationship_type):
    """
    Helper function to get relationship request concept name.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    Returns
    -------
    concept : `str`
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'big sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'mama'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'mistress'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return concept


def _get_relationship_request_concept_reversed(relationship_type):
    """
    Helper function to get relationship request concept name.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    Returns
    -------
    concept : `str`
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'little sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'daughter'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'maid'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return concept


def produce_break_up_success_description(target_user, source_received, target_received, guild_id):
    """
    Produces divorce success confirmation.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    source_received : `int`
        The amount of balance the source user received.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'You have broke up with '
    yield target_user.name_at(guild_id)
    yield '.'
    
    if source_received > 0 or target_received > 0:
        yield '\n'
        
        if source_received > 0:
            yield '\nYou received '
            yield str(source_received)
            yield ' '
            yield EMOJI__HEART_CURRENCY.as_emoji
            yield ' after investing much into the relationship.'
        
        if target_received > 0:
            yield '\nThey received '
            yield str(target_received)
            yield ' '
            yield EMOJI__HEART_CURRENCY.as_emoji
            yield ' after investing much into the relationship.'


def produce_relationship_request_header(relationship_type, outgoing, user_name, investment):
    """
    Produces relationship request header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    outgoing : `bool`
        Whether the request is outgoing.
    
    user_name : `str`
        The displayed user's name.
    
    investment : `int`
        The source user's investment.
    
    Yields
    ------
    part : `str`
    """
    yield get_relationship_request_type_concept(relationship_type, True)
    yield ' '
    yield ('towards' if outgoing else 'from')
    yield ' '
    yield user_name
    yield ' ('
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ')'


def produce_relationship_request_accepted_description(relationship_type, investment, source_user, guild_id):
    """
    Produces relationship request accepted description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' is now your '
    yield _get_relationship_request_concept(relationship_type)
    yield '.\nNow you are '
    yield get_relationship_type_name_basic(
        RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    )
    yield ' and '
    yield get_relationship_type_name_basic(relationship_type)
    yield '.\nYou received half of their investment ('
    yield str(investment >> 1)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ').'


def produce_relationship_request_rejected_description(relationship_type, investment, source_user, guild_id):
    """
    Produces relationship request rejected description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'You rejected '
    yield source_user.name_at(guild_id)
    yield '\'s '
    yield get_relationship_request_type_concept(relationship_type, False)
    yield '.\nTheir '
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' investment have been unallocated.'


def produce_relationship_request_cancelled_description(relationship_type, investment, target_user, guild_id):
    """
    Produces relationship request cancelled description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'You cancelled your '
    yield get_relationship_request_type_concept(relationship_type, False)
    yield ' towards '
    yield target_user.name_at(guild_id)
    yield  '.\nYour '
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' investment have been unallocated.'


def produce_break_up_notification_description(source_user, target_received, guild_id):
    """
    Produces break up notification description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who divorced.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' broke up with you.'
    
    if target_received > 0:
        yield '\n\nYou received '
        yield str(target_received)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
        yield ' after investing much into the relationship.'


def produce_relationship_request_accept_notification_description(relationship_type, investment, target_user, guild_id):
    """
    Produces break up notification description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who accepted the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield target_user.name_at(guild_id)
    yield ' accepting your proposal, is now your '
    yield _get_relationship_request_concept_reversed(relationship_type)
    yield '.\nNow you are '
    yield get_relationship_type_name_basic(relationship_type)
    yield ' and '
    yield get_relationship_type_name_basic(
        RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    )
    yield '.\nThey received half of your investment ('
    yield str(investment >> 1)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ').'


def produce_relationship_request_reject_notification_description(relationship_type, investment, target_user, guild_id):
    """
    Produces break up notification description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who rejected the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield target_user.name_at(guild_id)
    yield ' rejected becoming your '
    yield _get_relationship_request_concept_reversed(relationship_type)
    yield '.\nYour '
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' have been unallocated.'


def produce_relationship_request_creation_notification_description(
    relationship_type, investment, source_user, guild_id
):
    """
    Builds relationship request creation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' wants to '
    yield _get_relationship_request_action_concept(relationship_type)
    yield ' you.\nThey are proposing with '
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_relationship_request_cancellation_notification_description(
    relationship_type, investment, source_user, guild_id
):
    """
    Builds relationship request creation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' cancelled their '
    yield get_relationship_request_type_concept(relationship_type, False)
    yield ' towards you, with investment of '
    yield str(investment)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_relationship_listing_header(
    target_user,
    guild_id,
    relationship_value,
    relationship_divorces,
    relationship_slots,
    relationship_count,
    relationship_proposal_count,
    relationship_listing_mode,
    page_index,
):
    """
    Produces relationship listing header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user, who's relationships are shown.
    
    guild_id : `int`
        The local guild's identifier.
    
    relationship_value : `int`
        The targeted user's relationships value.
    
    relationship_divorces : `int`
        The targeted user's break up count.
    
    relationship_slots : `int`
        The targeted user's relationship slot count.
    
    relationship_count : `int`
        The amount of relationships the targeted user has.
    
    relationship_proposal_count : `int`
        The amount of outgoing proposals the targeted user has.
    
    relationship_listing_mode : `int`
        The mode to render as.
    
    page_index : `int`
        The displayed page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield target_user.name_at(guild_id)
    yield '\'s relationship info\n\nListing mode: '
    if relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LEGACY:
        relationship_listing_mode_name = 'legacy'
    elif relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LONG:
        relationship_listing_mode_name = 'long'
    elif relationship_listing_mode == RELATIONSHIP_LISTING_MODE_WIDE:
        relationship_listing_mode_name = 'wide'
    else:
        relationship_listing_mode_name = 'unknown'
    yield relationship_listing_mode_name
    
    yield '; Page: '
    yield str(page_index + 1)
    yield '\nValue: '
    yield str(floor(relationship_value * 1.1))
    yield ' - '
    yield str(floor(relationship_value * 2.1))
    yield '; Break-ups: '
    yield str(relationship_divorces)
    yield '; Slots: '
    if relationship_proposal_count:
        yield str(relationship_count + relationship_proposal_count)
        yield ' ('
        yield str(relationship_count)
        yield ' + '
        yield str(relationship_proposal_count)
        yield ')'
    else:
        yield str(relationship_count)
    
    yield ' / '
    yield str(relationship_slots)
    


def produce_relationship_listing_footer(source_user, target_user, guild_id, relationship_value):
    """
    Produces relationship listing footer.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user invoking the interation.
    
    target_user : ``ClientUserBase``
        The user, who's relationships are shown.
    
    guild_id : `int`
        The local guild's identifier.
    
    relationship_value : `int`
        The targeted user's relationships value.
    
    Yields
    ------
    part : `str`
    """
    yield 'To propose to '
    yield target_user.name_at(guild_id)
    yield ' you need at least '
    yield str(floor(get_affinity_multiplier(source_user.id, target_user.id) * relationship_value))
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'
