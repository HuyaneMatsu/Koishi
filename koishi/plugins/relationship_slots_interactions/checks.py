__all__ = ()

from hata.ext.slash import abort

from ...bot_utils.constants import MAX_WAIFU_SLOTS, WAIFU_SLOT_COST_DEFAULT

from .embed_builders import (
    build_failure_embed_insufficient_balance_self, build_failure_embed_max_relationship_slots_other,
    build_failure_embed_insufficient_balance_other, build_failure_embed_max_relationship_slots_self
)


def check_max_relationship_slots_self(relationship_slots):
    """
    Checks whether the maximal amount of relationship slots are reached.
    
    Parameters
    ----------
    relationship_slots : `int`
        The amount of relationship slots.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_slots < MAX_WAIFU_SLOTS:
        return
    
    abort(
        embed = build_failure_embed_max_relationship_slots_self(),
        components = None,
    )


def check_max_relationship_slots_other(relationship_slots, user, guild_id):
    """
    Checks whether the maximal amount of relationship slots are reached.
    
    Parameters
    ----------
    relationship_slots : `int`
        The amount of relationship slots.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if relationship_slots < MAX_WAIFU_SLOTS:
        return
    
    abort(
        embed = build_failure_embed_max_relationship_slots_other(user, guild_id),
        components = None,
    )


def check_sufficient_balance_self(required_balance, available_balance, new_relationship_slot_count):
    """
    Checks whether the user has sufficient balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    available_balance : `int`
        The available balance of the user.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (required_balance != WAIFU_SLOT_COST_DEFAULT) and (available_balance >= required_balance):
        return
    
    abort(
        embed = build_failure_embed_insufficient_balance_self(required_balance, new_relationship_slot_count),
        components = None,
    )


def check_sufficient_balance_other(required_balance, available_balance, new_relationship_slot_count, user, guild_id):
    """
    Checks whether the user has sufficient balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    available_balance : `int`
        The available balance of the user.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    if (required_balance != WAIFU_SLOT_COST_DEFAULT) and (available_balance >= required_balance):
        return
    
    abort(
        embed = build_failure_embed_insufficient_balance_other(
            required_balance, new_relationship_slot_count, user, guild_id
        ),
        components = None,
    )
