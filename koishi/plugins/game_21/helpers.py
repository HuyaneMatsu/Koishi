__all__ = ()

from itertools import islice
from random import random

from hata import DiscordException, ERROR_CODES

from .constants import COUNTER, COUNTER_MASK, PLAYER_STATE_FINISH, SESSIONS, STARTUP_IDENTIFIER
from .player import Player


def should_render_exception(exception):
    """
    Returns whether the given exception should be rendered.
    
    Parameters
    ----------
    exception : `BaseException`
        The exception to decide about.
    
    Returns
    -------
    should_render : `bool`
    """
    if isinstance(exception, ConnectionError):
        # no internet
        return False
    
    if isinstance(exception, DiscordException) and exception.code in (
        ERROR_CODES.unknown_message, # message deleted
        ERROR_CODES.unknown_channel, # message's channel deleted
        ERROR_CODES.missing_access, # client removed
        ERROR_CODES.missing_permissions, # permissions changed meanwhile
        ERROR_CODES.cannot_message_user, # user dm-s disabled or bot blocked.
        ERROR_CODES.unknown_interaction, # discord is lagging as usual.
    ):
         return False
    
    return True


def is_exception_expiration(exception):
    """
    Returns whether the exception is an expiration.
    
    Parameters
    ----------
    exception : `BaseException`
        The exception to decide about.
    
    Returns
    -------
    expiration : `bool`
    """
    return isinstance(exception, DiscordException) and exception.code == ERROR_CODES.unknown_interaction


def iter_interaction_events(interaction_event, previous_interaction_event):
    """
    Iterates over interaction events to try to send response with.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    interaction_event : `None | InteractionEvent`
        Interaction event.
    previous_interaction_event : `InteractionEvent`
        The previous interaction event.
    
    Yields
    ------
    interaction_event : ``InteractionEvent``
    """
    if (interaction_event is not None):
        yield interaction_event
    
    if (previous_interaction_event is not interaction_event):
        yield previous_interaction_event


def store_event(player, session, single_player, interaction_event):
    """
    Stores the given event as latest
    
    Parameters
    ----------
    player : `None | Player`
        The respective player.
    session : ``Game21Session``
        The respective session.
    single_player : `bool`
        Whether the game mode is single player.
    interaction_event : ``InteractionEvent``
        The interaction event to store.
    """
    if (player is not None) and player.latest_interaction_event.id < interaction_event.id:
        player.latest_interaction_event = interaction_event
    
    if single_player and session.latest_interaction_event.id < interaction_event.id:
        session.latest_interaction_event = interaction_event


def is_all_equal(values):
    """
    Returns every value is equal.
    
    Parameters
    ----------
    values : `iterable<object>`
        Values to check.
    
    Returns
    -------
    is_all_equal : `bool`
    """
    values = iter(values)
    
    try:
        first = next(values)
    except StopIteration:
        return True
    
    for value in values:
        if value != first:
            return False
    
    return True


def decide_winners(players):
    """
    Decides the winners and losers from the given players.
    
    Parameters
    ----------
    players : `list<Player>`
        Players to decide about.
    
    Returns
    -------
    winners : `None | list<Player>`
        The winning players.
    losers : `None | list<Player>`
        The losing players.
    """
    # Should not happen
    if not players:
        return None, None
    
    best_score_under_21 = -1
    
    for player in players:
        if player.state != PLAYER_STATE_FINISH:
            continue
        
        total = player.hand.total
        if total > 21:
            continue
        
        if total <= best_score_under_21:
            continue
        
        best_score_under_21 = total
    
    if best_score_under_21 == -1:
        winners = None
    else:
        winners = [
            player for player in players
            if player.state == PLAYER_STATE_FINISH and player.hand.total == best_score_under_21
        ]
    
    if (winners is None):
        losers = [*players]
    elif len(winners) == len(players):
        losers = None
    else:
        losers = [player for player in players if player not in winners]
    
    return winners, losers


def chain_nullables(*nullable_iterables):
    """
    Chains nullable iterables.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    *nullable_iterables : `iterable`
        Iterables to chain.
    
    Yields
    ------
    value : `object`
    """
    for nullable_iterable in nullable_iterables:
        if (nullable_iterable is not None):
            yield from nullable_iterable


def is_draw(winners, losers):
    """
    Returns whether a game ended with draw.
    
    Parameters
    ----------
    winners : `None | list<Player>`
        The winning players.
    losers : `None | list<Player>`
        The losing players.
    
    Returns
    -------
    draw : `bool`
    """
    return (winners is None) or (losers is None)


def get_refund_distribution(players, amount):
    """
    Creates refund distribution for the given players.
    
    Parameters
    -----------
    players : `iterable<Player>`
        Players to create distribution for.
    amount : `int`
        The bet amount.
    
    Returns
    -------
    distribution : `list<(int, int, int, bool)>`
    """
    return [(player.user.id, amount, 0.0) for player in players]


def get_balance_distribution(winners, losers, amount):
    """
    Gets love distribution for the given players.
    
    Parameters
    ----------
    winners : `None | list<Player>`
        The winning players.
    losers : `None | list<Player>`
        The losing players.
    amount : `int`
        The bet amount.
    
    Returns
    -------
    distribution : `list<(int, int, int, bool)>`
    """
    if is_draw(winners, losers):
        return get_refund_distribution(chain_nullables(winners, losers), amount)
    
    distribution = []
    multiplier = (len(winners) + len(losers)) / len(winners) - 1.0
    
    for player in winners:
        distribution.append((player.user.id, amount, multiplier))
    
    for player in losers:
        distribution.append((player.user.id, amount, -1.0))
    
    return distribution


async def try_acknowledge(client, interaction_event, player, session, single_player):
    """
    Tries to acknowledge the given event.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The respective client.
    interaction_event : ``InteractionEvent``
        The received interaction event.
    player : `None | Player`
        The respective player.
    session : ``Game21Session``
        The respective session.
    single_player : `bool`
        Whether the game mode is single player.
    """
    try:
        await client.interaction_component_acknowledge(interaction_event)
    except GeneratorExit:
        raise
    
    except BaseException as exception:
        if should_render_exception(exception):
            await client.events.error(client, f'try_acknowledge', exception)
        return
    
    store_event(player, session, single_player, interaction_event)


async def try_edit_response(
    client,
    interaction_event,
    latest_interaction_event,
    message,
    player,
    session,
    single_player,
    components,
    embed,
):
    """
    Tries to edit the response message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The respective client.
    
    interaction_event : `None | InteractionEvent`
        The received interaction event.
    
    latest_interaction_event : `int`
        Previous interaction event.
    
    message : ``Message``
        The message to edit if required.
    
    player : ``Player``
        The respective player.
    
    session : ``Game21Session``
        The respective session.
    
    single_player : `bool`
        Whether the game mode is single player.
    
    components : ``None | Component | list<Component>``
        The components to send.
    
    embed : ``Embed``
        The embed to send.
    
    Returns
    -------
    success : `bool`
    """
    for interaction_event in iter_interaction_events(interaction_event, latest_interaction_event):
        try:
            if interaction_event.is_acknowledged():
                if message is None:
                    if interaction_event.is_response_invoking_user_only():
                        await client.interaction_response_message_edit(interaction_event, '-# _ _')
                        await client.interaction_response_message_delete(interaction_event)
                        await client.interaction_followup_message_create(
                            interaction_event,
                            components = components,
                            embed = embed,
                        )
                    else:
                        await client.interaction_response_message_edit(
                            interaction_event,
                            components = components,
                            embed = embed,
                        )
                else:
                    await client.interaction_followup_message_edit(
                        interaction_event,
                        message,
                        components = components,
                        embed = embed,
                    )
            
            else:
                await client.interaction_component_message_edit(
                    interaction_event,
                    components = components,
                    embed = embed,
                )
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            if is_exception_expiration(exception):
                continue
            
            if should_render_exception(exception):
                await client.events.error(client, '_try_send_gamble_after', exception)
            
            return False
        
        if (interaction_event is not None):
            store_event(player, session, single_player, interaction_event)
        return True
    
    return False


async def try_deliver_end_notification(
    client,
    interaction_event,
    components,
    content,
):
    """
    Tries to deliver end notification.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The respective client.
    interaction_event : `None | InteractionEvent`
        The received interaction event.
    components : `None | Component | list<Component>`
        The components to send.
    content : `str`
        The content to send.
    
    Returns
    -------
    success : `bool`
    """
    try:
        await client.interaction_followup_message_create(
            interaction_event,
            components = components,
            content = content,
            show_for_invoking_user_only = True,
        )
    except GeneratorExit:
        raise
    
    except BaseException as exception:
        if should_render_exception(exception):
            await client.events.error(client, '_try_send_gamble_after', exception)
        
        return False
    
    return True


def create_player_bot(client, deck, difficulty):
    """
    Creates a bot player with the given difficulty.
    
    Difficulty represents the chance [0.0 : 1.0] how likely should it be for the bot to cheat.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client to we create player for.
    
    deck : ``Deck``
        Deck to pull from.
    
    difficulty : `float`
        The likeliness to cheat.
    
    Returns
    -------
    player_bot : ``Player``
    """
    player_bot_0 = Player(client, None)
    player_bot_0.hand.auto_finish(deck)
    player_bot_0.state = PLAYER_STATE_FINISH
    
    if (difficulty <= 0.0) or (player_bot_0.hand.total == 21) or (random() > difficulty):
        return player_bot_0
    
    player_bot_1 = Player(client, None)
    player_bot_1.hand.auto_finish(deck)
    player_bot_1.state = PLAYER_STATE_FINISH
    
    player_bot_0_total = player_bot_0.hand.total
    player_bot_1_total = player_bot_1.hand.total
    
    if (
        (player_bot_1_total == 21) or
        (player_bot_1_total < 21) and (player_bot_0_total < 21) and (player_bot_0_total < player_bot_1_total)
    ):
        player_bot_0.hand.restore(deck)
        return player_bot_1
    
    player_bot_1.hand.restore(deck)
    return player_bot_0


def create_session_identifier():
    """
    Creates a session identifier.
    
    Returns
    -------
    session_id : `int`
    """
    return STARTUP_IDENTIFIER | (next(COUNTER) & COUNTER_MASK)


def add_user_id_to_session(session, user_id):
    """
    Adds the user identifier to the session.
    
    Parameters
    ----------
    session : ``Game21Session``
        Session to add to.
    
    user_id : `int`
        User identifier to add.
    """
    user_ids = session.user_ids
    if user_ids is None:
        SESSIONS[session.id] = session
        user_ids = (user_id,)
    elif user_id not in user_ids:
        user_ids = (*user_ids, user_id)
    else:
        return
    
    session.user_ids = user_ids
    return


def remove_user_id_from_session(session, user_id):
    """
    Removes the user identifier to the session.
    
    Parameters
    ----------
    session : ``Game21Session``
        Session to add to.
    
    user_id : `int`
        User identifier to add.
    """
    user_ids = session.user_ids
    if (user_ids is None):
        return
    
    if (len(user_ids) == 1):
        if (user_ids[0] != user_id):
            return
        
        session.user_ids = None
        try:
            del SESSIONS[session.id]
        except KeyError:
            pass
        return
    
    try:
        index = user_ids.index(user_id)
    except ValueError:
        return
    
    session.user_ids = (*islice(user_ids, 0, index), *islice(user_ids, index + 1, None),)
    return


def remove_user_ids_from_session(session):
    """
    Removes all the user identifiers from the session.
    
    session : ``Game21Session``
        Session to add to.
    """
    user_ids = session.user_ids
    if (user_ids is None):
        return
    
    session.user_ids = None
    
    try:
        del SESSIONS[session.id]
    except KeyError:
        pass
