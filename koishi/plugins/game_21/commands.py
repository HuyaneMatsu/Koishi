__all__ = ()

from scarletio import Future, Task, TaskGroup, get_event_loop
from hata.ext.slash import Button

from ...bot_utils.constants import IN_GAME_IDS
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance

from .checks import check_bet_too_low, check_has_enough_love, check_in_game
from .constants import GAME_21_JOIN_ROW_DISABLED, GAME_21_ROW_DISABLED, PLAYER_STATE_FINISH
from .helpers import (
    decide_winners, get_love_distribution, get_refund_distribution, is_draw, try_deliver_end_notification,
    try_edit_response
)
from .join_runner import Game21JoinRunner
from .player import Player
from .player_runner import Game21PlayerRunner
from .queries import batch_modify_user_hearts
from .rendering import build_end_embed_multi_player, build_end_embed_single_player
from .session import Session


EVENT_LOOP = get_event_loop()


@FEATURE_CLIENTS.interactions(
    name = '21',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def game_21(
    client,
    interaction_event,
    amount : ('int', 'The amount of hearts to bet'),
    mode : ([('single-player', 'single'), ('multi-player', 'multi')], 'Game mode, yayyy') = 'single',
):
    """
    Starts a card game where you can bet your hearts.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    amount : `str`
        Bet amount.
    
    mode : `str` = `single`, Optional
        Game mode.
    """
    check_in_game(interaction_event)
    check_bet_too_low(amount)
    
    user_balance = await get_user_balance(interaction_event.user_id)
    check_has_enough_love(amount, user_balance.balance - user_balance.allocated, False)
    user_balance.set('allocated', user_balance.allocated + amount)
    await user_balance.save()
    
    single_player_mode = (mode == 'single')
    if single_player_mode:
        user_balance = await get_user_balance(client.id)
        check_has_enough_love(amount, user_balance.balance - user_balance.allocated, True)
        user_balance.set('allocated', user_balance.allocated + amount)
        await user_balance.save()
    
    await client.interaction_application_command_acknowledge(interaction_event)
    
    if single_player_mode:
        coroutine_function = game_21_single_player
    else:
        coroutine_function = game_21_multi_player
    
    await coroutine_function(client, interaction_event, amount)


async def game_21_single_player(client, event, amount):
    """
    Runs a single player game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    amount : `int`
        Bet amount.
    """
    session = Session(event.guild, amount, event)
    
    player_user = Player(event.user, event)
    player_user.hand.auto_pull_starting_cards(session.deck)
    
    player_bot = Player(client, None)
    player_bot.hand.auto_finish(session.deck)
    player_bot.state = PLAYER_STATE_FINISH
    
    waiter = Future(EVENT_LOOP)
    
    IN_GAME_IDS.add(event.user_id)
    try:
        await Game21PlayerRunner(client, session, player_user, True, waiter)
        success = await waiter
    except GeneratorExit:
        raise
    
    except:
        await batch_modify_user_hearts(get_refund_distribution([player_user, player_bot], amount))
        raise
    
    finally:
        IN_GAME_IDS.discard(event.user_id)
    
    if not success:
        await batch_modify_user_hearts(get_refund_distribution([player_user, player_bot], amount))
        return
    
    
    winners, losers = decide_winners([player_user, player_bot])
    await batch_modify_user_hearts(get_love_distribution(winners, losers, amount))
    
    if is_draw(winners, losers):
        player_win = 0
    elif (losers is not None) and (player_user in losers):
        player_win = -1
    else:
        player_win = 1
    
    await try_edit_response(
        client,
        None,
        session.latest_interaction_event,
        None,
        player_user,
        session,
        True,
        GAME_21_ROW_DISABLED,
        build_end_embed_single_player(session, player_user, player_bot, player_win),
    )


async def game_21_multi_player(client, event, amount):
    """
    Runs a multi player game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    amount : `int`
        Bet amount.
    """
    session = Session(event.guild, amount, event)
    
    players = [Player(event.user, event)]
    
    waiter = Future(EVENT_LOOP)
    
    IN_GAME_IDS.add(event.user_id)
    
    try:
        try:
            await Game21JoinRunner(client, session, players, waiter)
            success = await waiter
        except GeneratorExit:
            raise
        
        except:
            await batch_modify_user_hearts(get_refund_distribution(players, amount))
            raise
        
        if not success:
            await batch_modify_user_hearts(get_refund_distribution(players, amount))
            return
        
        
        task_group = TaskGroup(EVENT_LOOP)
        
        for player in players:
            player.hand.auto_pull_starting_cards(session.deck)
            
            waiter = task_group.create_future()
            task_group.create_task(Game21PlayerRunner(client, session, player, False, waiter))
        
        try:
            await task_group.wait_all()
        except GeneratorExit:
            raise
    
    finally:
        IN_GAME_IDS.difference_update(player.user.id for player in players)
        
    
    # Do we wanna do this?
    '''
    # Connect players that could not have their
    failed_to_initialize_players = players.copy()
    for future in task_group.iter_done():
        if not isinstance(future, Task):
            continue
        
        if future.get_exception() is not None:
            # Exception already logged, do nothing.
            continue
        
        runner = future.get_result()
        if runner is None:
            continue
        
        try:
            failed_to_initialize_players.remove(runner.player)
        except ValueError:
            pass
    
    # Refund failed to initialize players
    if failed_to_initialize_players:
        await batch_modify_user_hearts(get_refund_distribution(players, amount))
        
        for player in failed_to_initialize_players:
            try:
                players.remove(player)
            except ValueError:
                pass
    '''
    
    winners, losers = decide_winners(players)
    await batch_modify_user_hearts(get_love_distribution(winners, losers, amount))
    
    await try_edit_response(
        client,
        None,
        session.latest_interaction_event,
        None,
        players[0],
        session,
        True,
        GAME_21_JOIN_ROW_DISABLED,
        build_end_embed_multi_player(session, players, winners, losers),
    )
    
    # Deliver notifications
    message = session.latest_interaction_event.message
    if (message is not None):
        for player in players:
            Task(
                EVENT_LOOP,
                try_deliver_end_notification(
                    client,
                    player.latest_interaction_event,
                    Button('Get me there!', url = message.url),
                    f'> {player.user.mention} !!! The winners have been announced !!!'
                ),
            )
