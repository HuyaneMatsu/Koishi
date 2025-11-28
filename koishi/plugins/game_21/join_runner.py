__all__ = ()

from scarletio import Lock, RichAttributeErrorBaseType, Task, get_event_loop

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..user_balance import ALLOCATION_FEATURE_ID_GAME_21, get_user_balance, save_user_balance

from .constants import (
    GAME_21_CUSTOM_ID_CANCEL, GAME_21_CUSTOM_ID_ENTER, GAME_21_CUSTOM_ID_START, GAME_21_JOINER_TIMEOUT,
    GAME_21_JOIN_ROW_DISABLED, GAME_21_JOIN_ROW_ENABLED, PLAYERS_MAX, UI_STATE_CANCELLED, UI_STATE_CANCELLING,
    UI_STATE_EDITING, UI_STATE_READY, UI_STATE_SWITCHING_CONTEXT
)
from .helpers import (
    add_user_id_to_session, remove_user_id_from_session, should_render_exception, try_acknowledge, try_edit_response
)
from .player import Player
from .queries import modify_user_hearts
from .rendering import (
    build_join_embed, build_join_embed_cancelled, build_join_embed_game_started, build_join_embed_timed_out,
)


EVENT_LOOP = get_event_loop()


class Game21JoinRunner(RichAttributeErrorBaseType):
    """
    Game 21 join runner.
    
    Attributes
    ----------
    _ui_state : `int`
        The state of the graphical user interface. Tracked, so we do not overlap operations that should not be.
    _previous_player : ``list<Player>``
        The previously rendered players.
        Stored so we do not render the same message after each other in case we have a backlog.
    _timeout_handle : ``None | TimerHandle``
        handle to timeout the runner.
    _update_lock : ``Lock``
        Lock used to synchronise message updates.
    client : ``Client``
        the respective client.
    message : ``None | Message``
        Message to operate on.
    players : ``list<Player>``
        The joined players. The 0th element is always the creator who cannot leave.
    session : ``Game21Session``
        Game session.
    single_player : `bool`
        Whether its a player runner for single player mode.
    waiter : ``Future<bool>``
        A future that has its result set when the runner is finished.
    """
    __slots__ = (
        '_ui_state', '_previous_player', '_timeout_handle', '_update_lock', 'client', 'message', 'players', 'session',
        'waiter'
    )
    
    async def __new__(cls, client, session, players, waiter):
        """
        Creates a new game 21 join runner.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            the respective client.
        session : ``Game21Session``
            Game session.
        players : `list<Player>`
            The joined players.
        waiter : `Future<bool>`
            A future that has its result set when the runner is finished.
        """
        try:
            await client.interaction_response_message_edit(session.latest_interaction_event, '-# _ _')
            await client.interaction_response_message_delete(session.latest_interaction_event)
            message = await client.interaction_followup_message_create(
                session.latest_interaction_event,
                embed = build_join_embed([player.user for player in players], session.guild, session.amount),
                components = GAME_21_JOIN_ROW_ENABLED,
            )
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            if should_render_exception(exception):
                await client.events.error(client, f'{cls.__name__}.__new__', exception)
            
            message = None
        
        else:
            session.message = message
        
        self = object.__new__(cls)
        self._ui_state = UI_STATE_SWITCHING_CONTEXT if message is None else UI_STATE_READY
        self._previous_player = players.copy()
        self._timeout_handle = None
        self._update_lock = Lock(EVENT_LOOP)
        self.client = client
        self.message = message
        self.players = players
        self.session = session
        self.waiter = waiter
        
        if message is None:
            timeout_handle = None
        else:
            timeout_handle = EVENT_LOOP.call_after(GAME_21_JOINER_TIMEOUT, self._invoke_timeout)
        self._timeout_handle = timeout_handle
        
        if message is None:
            waiter.set_result_if_pending(False)
        else:
            client.slasher.add_component_interaction_waiter(message, self)
        
        return self


    async def __call__(self, interaction_event):
        """
        Handles a component interaction on the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        custom_id = interaction_event.custom_id
        
        if custom_id == GAME_21_CUSTOM_ID_ENTER:
            await self._enter_user(interaction_event)
        
        elif custom_id == GAME_21_CUSTOM_ID_START:
            await self._start(interaction_event)
        
        elif custom_id == GAME_21_CUSTOM_ID_CANCEL:
            await self._cancel(interaction_event)
        
        else:
            # No other cases
            pass
    
    
    async def _enter_user(self, interaction_event):
        """
        Enters a users to the game.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        client = self.client
        players = self.players
        session = self.session
        
        # If the player is the creator one, do nothing.
        if interaction_event.user is players[0].user:
            await try_acknowledge(client, interaction_event, players[0], session, True)
            return
        
        player = next((player for player in players if player.user is interaction_event.user), None)
        
        # Is the user leaving?
        if (player is not None):
            players.remove(player)
            remove_user_id_from_session(session, interaction_event.user_id)
            await try_acknowledge(client, interaction_event, player, session, True)
            await modify_user_hearts(player.user.id, session.amount, 0.0, session.id)
            
            try:
                await client.interaction_followup_message_create(
                    interaction_event,
                    content = '21 multi-player game left.',
                    show_for_invoking_user_only = True,
                )
            except GeneratorExit:
                raise
            
            except BaseException as exception:
                if should_render_exception(exception):
                    await client.events.error(client, f'{type(self).__name__}._enter_user', exception)
            
            await self._update_message(interaction_event, player, False)
            return
                    
        # The user must be joining
        
        while True:
            if len(players) >= PLAYERS_MAX:
                error_message = f'Max {PLAYERS_MAX!s} players are allowed.'
                break
            
            user_balance = await get_user_balance(interaction_event.user_id)
            
            amount = session.amount
            available = user_balance.balance - user_balance.get_cumulative_allocated_balance()
            if amount > available:
                error_message = (
                    f'I must have at least {amount!s} available {EMOJI__HEART_CURRENCY} to join.\n'
                    f'I have {available!s} {EMOJI__HEART_CURRENCY} available.'
                )
                break
            
            user_balance.add_allocation(ALLOCATION_FEATURE_ID_GAME_21, session.id, amount)
            await save_user_balance(user_balance)
            
            player = Player(interaction_event.user, interaction_event)
            players.append(player)
            add_user_id_to_session(session, interaction_event.user_id)
            await self._update_message(interaction_event, player, False)
            return
        
        
        await try_acknowledge(client, interaction_event, player, session, True)
        try:
            await client.interaction_followup_message_create(
                interaction_event,
                content = error_message,
            )
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            if should_render_exception(exception):
                await client.events.error(client, f'{type(self).__name__}._enter_user', exception)
    
    
    async def _start(self, interaction_event):
        """
        Starts the game.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        client = self.client
        players = self.players
        session = self.session
        
        if interaction_event.user is not players[0].user:
            await try_acknowledge(self.client, interaction_event, None, session, True)
            return
        
        while True:
            # Can start only if user count >= 2
            if len(self.players) < 2:
                error_message = 'There must be at least 1 other user in game to start it.'
                break
            
            # start
            self._ui_state = UI_STATE_SWITCHING_CONTEXT
            
            try:
                await self._update_message(interaction_event, players[0], True)
            finally:
                self.waiter.set_result_if_pending(True)
                self._invoke_cancellation(False)
            return
        
            
        await try_acknowledge(client, interaction_event, players[0], session, True)
        try:
            await client.interaction_followup_message_create(
                interaction_event,
                content = error_message,
                show_for_invoking_user_only = True,
            )
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            if should_render_exception(exception):
                await client.events.error(client, f'{type(self).__name__}._start', exception)
        
        return
    
    async def _cancel(self, interaction_event):
        """
        Cancels the game.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        if interaction_event.user is not self.players[0].user:
            await try_acknowledge(self.client, interaction_event, None, self.session, True)
            return
        
        self._ui_state = UI_STATE_CANCELLING
        
        try:
            await self._update_message(interaction_event, self.players[0], True)
        finally:
            self._invoke_cancellation(False)
    
    
    async def _update_message(self, interaction_event, player, force):
        """
        Updates the join runner's message.
        
        This function is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received interaction event.
        player : ``Player``
            The player who causes the message to be updated.
        force : `bool`
            Whether the message should be updated even if the interface's current state is not ready.
        """
        client = self.client
        players = self.players
        session = self.session
        lock = self._update_lock
        
        if lock.is_locked():
            if not interaction_event.is_acknowledged():
                await try_acknowledge(client, interaction_event, player, session, True)
        
        async with lock:
            ui_state = self._ui_state
            if (ui_state != UI_STATE_READY) and (not force):
                return
            
            if ui_state == UI_STATE_READY:
                # We want to render the general embed.
                if self._previous_player == players:
                    # If nothing changed nothing to do.
                    return
                
                self._previous_player = players.copy()
                embed = build_join_embed(
                    [player.user for player in players], session.guild, session.amount,
                )
                components = GAME_21_JOIN_ROW_ENABLED
            
            elif ui_state == UI_STATE_SWITCHING_CONTEXT:
                # We want to render the started embed.
                embed = build_join_embed_game_started(
                    [player.user for player in players], session.guild, session.amount,
                )
                components = GAME_21_JOIN_ROW_DISABLED
            
            
            elif ui_state == UI_STATE_CANCELLING or ui_state == UI_STATE_CANCELLED:
                # We want to render the cancelling embed.
                embed = build_join_embed_cancelled(
                    [player.user for player in players], session.guild, session.amount,
                )
                components = GAME_21_JOIN_ROW_DISABLED
            
            else:
                # Should not happen
                return
            
            if ui_state == ui_state:
                self._ui_state = UI_STATE_EDITING
            
            try:
                success = await try_edit_response(
                    client,
                    interaction_event,
                    self.session.latest_interaction_event,
                    self.message,
                    player,
                    session,
                    True,
                    components,
                    embed,
                )
            except GeneratorExit:
                self._invoke_cancellation(False)
                raise
            
            except BaseException as exception:
                self._invoke_cancellation(False)
                if should_render_exception(exception):
                    await client.events.error(client, f'{type(self).__name__}._update_message', exception)
                
            else:
                if success:
                    if self._ui_state == UI_STATE_EDITING:
                        self._ui_state = UI_STATE_READY
                else:
                    self._invoke_cancellation(False)
    
    
    def _invoke_cancellation(self, timeout):
        """
        Invokes cancellation.
        
        Parameters
        ----------
        timeout : `bool`
            Whether invoked from ``._invoke_timeout``.
        """
        if timeout:
            self._timeout_handle = None
        else:
            timeout_handle = self._timeout_handle
            if (timeout_handle is not None):
                timeout_handle.cancel()
                self._timeout_handle = None
        
        message = self.message
        if (message is not None):
            self.client.slasher.remove_component_interaction_waiter(message, self)
        
        if self._ui_state != UI_STATE_SWITCHING_CONTEXT:
            self._ui_state = UI_STATE_CANCELLED
        
        self.waiter.set_result_if_pending(False)
    
    
    def _invoke_timeout(self):
        """
        Invokes timeout and edits the gui's message with a timeout embed.
        """
        self._invoke_cancellation(True)
        Task(
            EVENT_LOOP,
            try_edit_response(
                self.client,
                None,
                self.players[0].latest_interaction_event,
                self.message,
                self.players[0],
                self.session,
                False,
                GAME_21_JOIN_ROW_DISABLED,
                build_join_embed_timed_out(
                    [player.user for player in self.players], self.session.guild, self.session.amount,
                ),
            ),
        )
