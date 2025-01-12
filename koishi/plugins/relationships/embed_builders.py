__all__ = ()

from itertools import chain
from math import floor

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import ACTION_NAME_UNKNOWN
from .helpers import calculate_relationship_value, get_affinity_multiplier
from .relationship_types import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MASTER,
    RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL,
    RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU, get_relationship_type_name
)


def build_failure_embed_self_propose():
    """
    Builds a failure embed for the case when the user is trying to propose to themselves.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Self targeting not allowed',
        (
            'You cannot propose to yourself.'
        ),
    )


def build_failure_embed_insufficient_available_balance(available_balance, investment):
    """
    Builds a failure embed for the case when available balance is lower than the investment.
    
    Parameters
    ----------
    available_balance : `int`
        Available balance.
    
    investment : `int`
        The amount of balance to propose with.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient available balance',
        (
            f'You have {available_balance} available {EMOJI__HEART_CURRENCY} '
            f'which is lower than {investment} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_failure_embed_you_already_have_waifu(waifu, user, guild_id):
    """
    Builds a failure embed for the case when the current user already has a waifu
    
    Parameters
    ----------
    waifu : ``ClientUserBase``
        The current waifu.
    
    user : ``ClientUserBase``
        The user on the other end.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'You already have a waifu',
        (
            f'What would {waifu.name_at(guild_id)} say if they would know about '
            f'{user.name_at(guild_id)}?'
        ),
    )


def build_failure_embed_already_proposing(relationship_type, investment, target_user, guild_id):
    """
    Builds a failure embed for the case when the user is already proposing.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'a marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'a blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'an adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'an employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'You are already proposing',
        (
            f'You have already sent {concept} towards {target_user.name_at(guild_id)} '
            f'with {investment} {EMOJI__HEART_CURRENCY}.\n'
            f'Cancel the old proposal before reissuing a new one.'
        ),
    )


def build_failure_embed_already_related(relationship_type, outgoing, checked_at_creation, user, guild_id):
    """
    Builds a failure embed for the case when the users are already related.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    outgoing : `bool`
        Whether the relationship is outgoing.
    
    checked_at_creation : `bool`
        Whether we are building a failure embed for creation (or accetage).
    
    user : ``ClientUserBase``
        The related user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    if outgoing ^ checked_at_creation:
        relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'married to'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_LIL:
        concept = 'the little sister of'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'the big sister of'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'the mama of'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'the master of'
    elif relationship_type == RELATIONSHIP_TYPE_MAID:
        concept = 'the maid of'
    elif relationship_type == RELATIONSHIP_TYPE_DAUGHTER:
        concept = 'the daughter of'
    elif relationship_type == RELATIONSHIP_TYPE_UNSET:
        concept = 'related to'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    if checked_at_creation:
        recommended_action = 'reissuing a new'
    else:
        recommended_action = 'accepting their'
    
    return Embed(
        'You are already related',
        (
            f'You are already {concept} {user.name_at(guild_id)}.\n'
            f'Divorce them before {recommended_action} proposal.'
        ),
    )


def build_failure_embed_they_already_have_waifu(waifu, user, guild_id):
    """
    Builds a failure embed for the case when they already have waifu.
    
    Parameters
    ----------
    waifu : ``ClientUserBase``
        The current waifu.
    
    user : ``ClientUserBase``
        The user with waifu.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'They already have a waifu',
        (
            f'{user.name_at(guild_id)} is already married to {waifu.name_at(guild_id)}!!'
        ),
    )


def build_failure_embed_you_already_have_waifu_request(waifu_subject, user, guild_id):
    """
    Builds a failure embed for the case when the user already has a waifu request.
    
    Parameters
    ----------
    waifu_subject : ``ClientUserBase``
        The already requested waifu.
    
    user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'You already have a waifu request',
        (
            f'What would {waifu_subject.name_at(guild_id)} say if they would know about '
            f'{user.name_at(guild_id)}?'
        ),
    )


def build_failure_embed_insufficient_relationship_slots(
    relationship_count, relationship_request_count, relationship_slots
):
    """
    Builds a failure embed for the case when the user does not have enough relationship slots.
    
    Parameters
    ----------
    relationship_count : `int`
        How much relationships the user has.
    
    relationship_request_count : `int`
        How much relationship requests the user has.
    
    relationship_slots : `int`
        How much relationships the user can have.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient relationship slots',
        (
            f'You do not have enough available relationship slots.\n'
            f'You have {relationship_slots} relationship slots from which '
            f'{relationship_count} is occupied by relationships and '
            f'{relationship_request_count} is occupied by relationship requests.'
        ),
    )


def build_failure_embed_you_already_have_master(master, user, guild_id):
    """
    Builds a failure embed for the case when you already have a master.
    
    Parameters
    ----------
    master : ``ClientUserBase``
        The current master.
    
    user : ``ClientUserBase``
        The user who has master.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'You already have a master',
        (
            f'{master.name_at(guild_id)} would surely not be pleased if they would know about '
            f'{user.name_at(guild_id)}.'
        ),
    )


def build_failure_embed_they_already_have_master(master, user, guild_id):
    """
    Builds a failure embed for the case when they already have a master.
    
    Parameters
    ----------
    master : ``ClientUserBase``
        The current master.
    
    user : ``ClientUserBase``
        The user who has master.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'They already have a master',
        (
            f'{user.name_at(guild_id)}\'s master is {master.name_at(guild_id)}, '
            f'therefore they cannot serve you.'
        ),
    )


def build_failure_embed_you_already_have_mama(mama, user, guild_id):
    """
    Builds a failure embed for the case when you already have a mama.
    
    Parameters
    ----------
    mama : ``ClientUserBase``
        The current mama.
    
    user : ``ClientUserBase``
        The user who has mama.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'You already have a mama',
        (
            f'{mama.name_at(guild_id)} would send you to your dark room, so you don\'t ever think about '
            f'{user.name_at(guild_id)}.'
        ),
    )


def build_failure_embed_they_already_have_mama(mama, user, guild_id):
    """
    Builds a failure embed for the case when they already have a mama.
    
    Parameters
    ----------
    mama : ``ClientUserBase``
        The current mama.
    
    user : ``ClientUserBase``
        The user who has mama.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'They already have a mama',
        (
            f'{user.name_at(guild_id)}\'s mama is {mama.name_at(guild_id)}, '
            f'therefore you cannot adopt them.'
        ),
    )


def build_failure_embed_insufficient_investment(relationship_value, investment):
    """
    Builds a failure embed for the case when the relation cost is greater than the investment.
    
    Parameters
    ----------
    relationship_value : `int`
        The required balance to engage the relationship with.
    
    investment : `int`
        The amount of balance to propose with.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient investment',
        (
            f'Your investment {investment} {EMOJI__HEART_CURRENCY} is lower than the required'
            f'{relationship_value} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_success_embed_request_created(relationship_type, investment, target_user, guild_id):
    """
    Builds a success embed when a request is created.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'a marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'a blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'an adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'an employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'Relationship request created',
        (
            f'You sent {concept} to {target_user.name_at(guild_id)} '
            f'with {investment} {EMOJI__HEART_CURRENCY}'
        ),
    )


def build_success_embed_request_cancelled(relationship_type, investment, target_user, guild_id):
    """
    Builds a success embed when a request is cancelled.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'Relationship request cancelled',
        (
            f'You cancelled your {concept} towards {target_user.name_at(guild_id)}.\n'
            f'Your {investment} {EMOJI__HEART_CURRENCY} investment have been refunded.'
        ),
    )


def build_success_embed_request_rejected(relationship_type, investment, source_user, guild_id):
    """
    Builds a success embed when a request is rejected.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The source use who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'Relationship request rejected',
        (
            f'You rejected {source_user.name_at(guild_id)}\'s {concept}.\n'
            f'Their {investment} {EMOJI__HEART_CURRENCY} investment have been refunded.'
        ),
    )


def build_success_embed_request_accepted(relationship_type, investment, source_user, guild_id):
    """
    Builds a success embed when a request is accepted.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The source use who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'big sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'mama'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'master'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    relationship_name_source = get_relationship_type_name(relationship_type)
    relationship_name_target = get_relationship_type_name(
        RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    )
    
    return Embed(
        'Relationship request accepted',
        (
            f'{source_user.name_at(guild_id)} is now your {concept}.\n'
            f'Now you are {relationship_name_target} and {relationship_name_source}.\n'
            f'You received half of their investment ({investment >> 1} {EMOJI__HEART_CURRENCY}).'
        ),
    )


def build_notification_embed_request_created(relationship_type, investment, source_user, guild_id):
    """
    Builds a notification embed sent to a user about a relationship request being created towards them.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'marry'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'have a blood-pact with'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'adopt'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'employ'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'You received a proposal',
        (
            f'{source_user.name_at(guild_id)} wants to {concept} you.\n'
            f'They are proposing with {investment} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_notification_embed_request_accepted(relationship_type, investment, target_user, guild_id):
    """
    Builds a notification embed sent to a user about a relationship request being accepted which is created by them.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'little sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'daughter'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'maid'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    relationship_name_source = get_relationship_type_name(relationship_type)
    relationship_name_target = get_relationship_type_name(
        RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    )
    
    return Embed(
        'Your proposal has been accepted',
        (
            f'{target_user.name_at(guild_id)} is now your {concept}.\n'
            f'Now you are {relationship_name_source} and {relationship_name_target}.\n'
            f'They received half of your investment ({investment >> 1} {EMOJI__HEART_CURRENCY}).'
        ),
    )


def build_notification_embed_request_rejected(relationship_type, investment, target_user, guild_id):
    """
    Builds a notification embed sent to a user about a relationship request being rejected which is created by them.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'little sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'daughter'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'maid'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'Your proposal has been rejected',
        (
            f'{target_user.name_at(guild_id)} rejected becoming your {concept}.\n'
            f'Your {investment} {EMOJI__HEART_CURRENCY} have been refunded.'
        ),
    )


def build_notification_embed_request_cancelled(relationship_type, investment, source_user, guild_id):
    """
    Builds a notification embed sent to a user about a relationship request being cancelled.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'A proposal towards you have been cancelled',
        (
            f'{source_user.name_at(guild_id)} cancelled their {concept} '
            f'with investment of {investment} {EMOJI__HEART_CURRENCY} towards you.'
        ),
    )


def build_relationship_request_listing_embed(outgoing, relationship_request_listing, users, guild_id):
    """
    Builds incoming relationship request embed.
    
    Parameters
    ----------
    outgoing : `bool`
        Whether to render the outgoing embed.
    
    relationship_request_listing : `None | list<RelationshipRequest>`
        Incoming relationship requests.
    
    users : `None | list<ClientUserBase>`
        The requested user for each relationship.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed('Outgoing requests' if outgoing else 'Incoming requests')
    
    if (relationship_request_listing is not None):
        grouped_relationship_request_listing = {}
        
        for relationship_request in relationship_request_listing:
            relationship_type = relationship_request.relationship_type
            
            try:
                group = grouped_relationship_request_listing[relationship_type]
            except KeyError:
                group = []
                grouped_relationship_request_listing[relationship_type] = group
            
            if outgoing:
                user_id = relationship_request.target_user_id
            else:
                user_id = relationship_request.source_user_id
            
            try:
                user = next(user for user in users if user.id == user_id)
            except StopIteration as exception:
                raise RuntimeError(outgoing, relationship_request_listing, users, guild_id, user_id) from exception
            
            group.append((user.name_at(guild_id), relationship_request.investment))
        
        
        for group in grouped_relationship_request_listing.values():
            group.sort()
        
        
        for relationship_type in (
            RELATIONSHIP_TYPE_WAIFU,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_MAMA,
            RELATIONSHIP_TYPE_MASTER,
            RELATIONSHIP_TYPE_UNSET,
        ):
            try:
                group = grouped_relationship_request_listing[relationship_type]
            except KeyError:
                continue
            
            if relationship_type == RELATIONSHIP_TYPE_WAIFU:
                title = 'Marriage proposals:'
            elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
                title = 'Blood-pact requests:'
            elif relationship_type == RELATIONSHIP_TYPE_MAMA:
                title = 'Adoption agreements:'
            elif relationship_type == RELATIONSHIP_TYPE_MASTER:
                title = 'Employment contract:'
            elif relationship_type == RELATIONSHIP_TYPE_UNSET:
                title = 'Unset:'
            else:
                title = ACTION_NAME_UNKNOWN
            
            description_parts = []
            
            index = 0
            length = len(group)
            
            while True:
                user_name, investment = group[index]
                
                description_parts.append(user_name)
                description_parts.append(' (')
                description_parts.append(str(investment))
                description_parts.append(' ')
                description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
                description_parts.append(')')
                
                index += 1
                if index == length:
                    break
                
                description_parts.append('\n')
            
            embed.add_field(title, ''.join(description_parts))
            description_parts = None
    
    if embed.fields is None:
        embed.description = '*none*'
    
    return embed


def build_relationship_listing_embed(
    source_user,
    target_user,
    target_user_balance,
    target_relationship_listing,
    target_relationship_listing_extend,
    target_relationship_request_listing,
    users,
    guild_id,
):
    """
    Builds a relationship listing.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is listing the relationships.
    
    target_user : ``ClientUserBase``
        The user who's relationships are being listed.
    
    target_user_balance : ``UserBalance``
        The targeted user's user balance.
    
    target_relationship_listing : `None | list<Relationship>`
        The targeted user's relationships.
    
    target_relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        Indirect relationships of the targeted user.
    
    target_relationship_request_listing : `None | list<RelationshipProposal>`
        The outgoing relationship proposals of the targeted user.
    
    users : `None | list<ClientUserBase>`
        The user entities the `target_user` has relationships with.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        f'{target_user.name_at(guild_id)}\'s relationship info',
    ).add_thumbnail(
        target_user.avatar_url_at(guild_id),
    )
    
    # Relationship value
    relationship_value = calculate_relationship_value(
        target_user.id, target_user_balance.relationship_value, target_relationship_listing
    )
    embed.add_field(
        f'Value',
        (
            f'```\n'
            f'{floor(relationship_value * 1.1)} - {floor(relationship_value * 2.1)}\n'
            f'```'
        ),
        inline = True,
    )
    
    # Divorces
    embed.add_field(
        'Divorces',
        (
            f'```\n'
            f'{target_user_balance.relationship_divorces!s}\n'
            f'```'
        ),
        inline = True,
    )
    
    # Relationship slots
    relationship_count = 0 if target_relationship_listing is None else len(target_relationship_listing)
    relationship_proposal_count = (
        0 if target_relationship_request_listing is None else len(target_relationship_request_listing)
    )
    relationship_slots = target_user_balance.relationship_slots
    
    description_parts = ['```\n']
    if relationship_proposal_count:
        description_parts.append(str(relationship_count + relationship_proposal_count))
        description_parts.append(' (')
        description_parts.append(str(relationship_count))
        description_parts.append(' + ')
        description_parts.append(str(relationship_proposal_count))
        description_parts.append(')')
    else:
        description_parts.append(str(relationship_count))
    
    description_parts.append(' / ')
    description_parts.append(str(relationship_slots))
    description_parts.append('\n```')
    
    description = ''.join(description_parts)
    description_parts = None
    
    embed.add_field(
        'Slots',
        description,
        inline = True,
    )
    
    # Relationships
    
    if (target_relationship_listing is None):
        embed.add_field('Relationships', '*none*')
    
    else:
        grouped_relationships = {}
        
        for relationship_source, relationships in chain(
            ((None, target_relationship_listing),),
            (() if target_relationship_listing_extend is None else target_relationship_listing_extend),
        ):
            if relationship_source is None:
                relationship_source = ''
            else:
                relationship_source = 'in law'
                
            for relationship in relationships:
                relationship_type = relationship.relationship_type
                
                user_id = relationship.target_user_id
                if user_id == target_user.id:
                    user_id = relationship.source_user_id
                else:
                    relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
                
                try:
                    group = grouped_relationships[relationship_type]
                except KeyError:
                    group = []
                    grouped_relationships[relationship_type] = group
                
                try:
                    user = next(user for user in users if user.id == user_id)
                except StopIteration as exception:
                    raise RuntimeError(
                        source_user,
                        target_user,
                        target_user_balance,
                        target_relationship_listing,
                        target_relationship_listing_extend,
                        target_relationship_request_listing,
                        users,
                        guild_id,
                        user_id,
                    ) from exception
                
                group.append((relationship_source, user.name_at(guild_id)))
        
        
        for group in grouped_relationships.values():
            group.sort()
        
        for relationship_type in (
            RELATIONSHIP_TYPE_WAIFU,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_SISTER_LIL,
            RELATIONSHIP_TYPE_MAMA,
            RELATIONSHIP_TYPE_DAUGHTER,
            RELATIONSHIP_TYPE_MASTER,
            RELATIONSHIP_TYPE_MAID,
            RELATIONSHIP_TYPE_UNSET,
        ):
            try:
                group = grouped_relationships[relationship_type]
            except KeyError:
                continue
            
            if relationship_type == RELATIONSHIP_TYPE_WAIFU:
                title = 'Waifu'
            elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
                title = 'Big sister(s)'
            elif relationship_type == RELATIONSHIP_TYPE_SISTER_LIL:
                title = 'Lil sister(s)'
            elif relationship_type == RELATIONSHIP_TYPE_MAMA:
                title = 'Mama'
            elif relationship_type == RELATIONSHIP_TYPE_DAUGHTER:
                title = 'Daughter(s)'
            elif relationship_type == RELATIONSHIP_TYPE_MASTER:
                title = 'Master'
            elif relationship_type == RELATIONSHIP_TYPE_MAID:
                title = 'Maid(s)'
            elif relationship_type == RELATIONSHIP_TYPE_UNSET:
                title = 'Unset'
            else:
                title = ACTION_NAME_UNKNOWN
            
            description_parts = []
            
            index = 0
            length = len(group)
            
            while True:
                relationship_source, user_name = group[index]
                
                description_parts.append(user_name)
                
                if relationship_source:
                    description_parts.append(' (')
                    description_parts.append(relationship_source)
                    description_parts.append(')')
                
                index += 1
                if index == length:
                    break
                
                description_parts.append('\n')
            
            description = ''.join(description_parts)
            description_parts = None
            
            embed.add_field(title, description)
    
    # Footer | could add more footers?
    if (source_user is target_user):
        footer = None
        footer_icon_url = None
    
    elif (
        (
            (target_relationship_listing is None) or
            not any(
                (
                    (relationship.source_user_id == source_user.id) and
                    (relationship.target_user_id == target_user.id)
                ) or (
                    (relationship.source_user_id == target_user.id) and
                    (relationship.target_user_id == source_user.id)
                )
                for relationship in target_relationship_listing
            )
        )
    ):
        footer = (
            f'To propose to {target_user.name_at(guild_id)} you need at least '
            f'{floor(get_affinity_multiplier(source_user.id, target_user.id) * relationship_value)} hearts.'
        )
        footer_icon_url = source_user.avatar_url_at(guild_id)
    
    else:
        footer = None
        footer_icon_url = None
    
    if (footer is not None):
        embed.add_footer(
            footer,
            icon_url = footer_icon_url,
        )
    
    return embed


def build_question_embed_divorce(target_user, guild_id):
    """
    Builds an embed that questions the user before divorcing.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Divorcing',
        f'Are you sure to divorce {target_user.name_at(guild_id)}?',
    )


def build_success_embed_divorce_cancelled(target_user, guild_id):
    """
    Builds an embed that is shown when divorcing is cancelled.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Divorcing cancelled',
        f'You cancelled divorcing {target_user.name_at(guild_id)}.',
    )


def build_failure_embed_you_cannot_cancel_this_divorce():
    """
    Builds an embed that is shown when the user cannot cancel this divorce.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Divorcing cannot be cancelled',
        'You are not part of this engagement, so you cannot cancel it.',
    )


def build_success_embed_divorce_confirmed(target_user, source_received, target_received, guild_id):
    """
    Builds an embed that is shown when divorcing is confirmed.
    
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
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    description_parts.append('You have divorced ')
    description_parts.append(target_user.name_at(guild_id))
    description_parts.append('.')
    
    if source_received or target_received:
        description_parts.append('\n')
        
        if source_received:
            description_parts.append('\nYou received ')
            description_parts.append(str(source_received))
            description_parts.append(' ')
            description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            description_parts.append(' after investing much into the relationship.')
        
        if target_received:
            description_parts.append('\nThey received ')
            description_parts.append(str(target_received))
            description_parts.append(' ')
            description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            description_parts.append(' after investing much into the relationship.')
    
    return Embed(
        'Divorcing confirmed',
        ''.join(description_parts),
    )


def build_failure_embed_you_cannot_confirm_this_divorce():
    """
    Builds an embed that is shown when the user cannot confirm this divorce.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Divorcing cannot be confirmed',
        'You are not part of this engagement, so you cannot confirm it.',
    )


def build_failure_embed_cannot_divorce_not_related_anymore(target_user, guild_id):
    """
    Builds a failure embed that is shown when the users are not related anymore, so cannot divorce each other.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Divorcing cannot be confirmed',
        f'You are not related to {target_user.name_at(guild_id)} anymore.'
    )


def build_notification_embed_divorced(source_user, target_received, guild_id):
    """
    Builds a notification embed sent to a user about a relationship request being created towards them.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who divorced.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    description_parts.append(source_user.name_at(guild_id))
    description_parts.append(' divorced you.')
    
    if target_received:
        description_parts.append('\n\nYou received ')
        description_parts.append(str(target_received))
        description_parts.append(' ')
        description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
        description_parts.append(' after investing much into the relationship.')
    
    return Embed(
        'You have been divorced',
        ''.join(description_parts),
    )


def build_success_embed_relationship_updated(relationship_type, target_user, guild_id):
    """
    Builds a success embed when a relationship's type is updated.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    target_user : ``ClientUserBase``
        The targeted user. May be actually the source user if the relationship is reversed.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'big sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'mama'
    elif relationship_type == RELATIONSHIP_TYPE_MASTER:
        concept = 'master'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return Embed(
        'Relationship updated',
        f'You have become the {concept} of {target_user.name_at(guild_id)}.',
    )


def build_failure_embed_target_relationship_creation_disallowed(target_user, guild_id):
    """
    Builds a failure embed if creating relationships towards the target user are disallowed.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Target relationship creation disallowed',
        (
            f'{target_user.name_at(guild_id)} is disallowed to create relationships.\n'
            f'Therefore creating a proposal towards them is not allowed.'
        ),
    )
