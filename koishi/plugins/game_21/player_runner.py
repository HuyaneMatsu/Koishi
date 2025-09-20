__all__ = ()

from scarletio import RichAttributeErrorBaseType, Task, get_event_loop

from .constants import (
    GAME_21_CUSTOM_ID_NEW, GAME_21_CUSTOM_ID_STOP, GAME_21_ROW_DISABLED, GAME_21_ROW_ENABLED, GAME_21_RUNNER_TIMEOUT,
    UI_STATE_CANCELLED, UI_STATE_EDITING, UI_STATE_READY, UI_STATE_SWITCHING_CONTEXT,
    PLAYER_STATE_CANCELLED_TIMEOUT, PLAYER_STATE_FINISH, PLAYER_STATE_INITIALIZATION_ERROR, PLAYER_STATE_IN_GAME_ERROR
)
from .helpers import should_render_exception, store_event, try_acknowledge, try_edit_response
from .rendering import build_gamble_after_embed, build_gamble_embed, build_gamble_timeout_embed


EVENT_LOOP = get_event_loop()


class Game21PlayerRunner(RichAttributeErrorBaseType):
    """
    Game 21 player runner.
    
    Attributes
    ----------
    _ui_state : `int`
        The state of the graphical user interface. Tracked, so we do not overlap operations that should not be.
    _timeout_handle : `None | TimerHandle`
        handle to timeout the runner.
    client : ``Client``
        the respective client.
    message : ``None | Message``
        Message to operate on.
    player : ``Player``
        User player.
    session : ``Session``
        Game session.
    single_player : `bool`
        Whether its a player runner for single player mode.
    waiter : `Future<bool>`
        A future that has its result set when the runner is finished.
    """
    __slots__ = ('_ui_state', '_timeout_handle', 'client', 'message', 'player', 'session', 'single_player', 'waiter')
    
    async def __new__(cls, client, session, player, single_player, waiter):
        """
        Creates a new game 21 player runner.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            the respective client.
        session : ``Session``
            Game session.
        player : ``Player``
            User player.
        single_player : `bool`
            Whether its a player runner for single player mode.
        waiter : `Future<bool>`
            A future that has its result set when the runner is finished.
        """
        game_ended = player.hand.is_finished()
        
        if game_ended:
            if single_player:
                message = None
            
            else:
                try:
                    message = await client.interaction_followup_message_create(
                        player.latest_interaction_event,
                        content = f'> {player.user.mention}',
                        embed = build_gamble_after_embed(player.hand, session.amount),
                        components = GAME_21_ROW_DISABLED,
                        show_for_invoking_user_only = True,
                    )
                except GeneratorExit:
                    raise
                
                except BaseException as exception:
                    if should_render_exception(exception):
                        await client.events.error(client, f'{cls.__name__}.__new__', exception)
                    
                    message = None
                    game_ended = True
            
            if waiter.set_result_if_pending(True):
                player.state = PLAYER_STATE_FINISH
        
        else:
            if single_player:
                await client.interaction_response_message_edit(player.latest_interaction_event, '-# _ _')
                await client.interaction_response_message_delete(player.latest_interaction_event)
                
            try:
                # even on single player it still will not create new message, because we just acknowledged it,
                # so no need to check for it.
                message = await client.interaction_followup_message_create(
                    player.latest_interaction_event,
                    content = (None if single_player else f'> {player.user.mention}'),
                    embed = build_gamble_embed(player.hand, session.amount),
                    components = GAME_21_ROW_ENABLED,
                    show_for_invoking_user_only = (not single_player),
                )
            except GeneratorExit:
                raise
            
            except BaseException as exception:
                if should_render_exception(exception):
                    await client.events.error(client, f'{cls.__name__}.__new__', exception)
                
                if waiter.set_result_if_pending(False):
                    player.state = PLAYER_STATE_INITIALIZATION_ERROR
                
                message = None
                game_ended = True
        
        
        self = object.__new__(cls)
        self._ui_state = UI_STATE_SWITCHING_CONTEXT if game_ended else UI_STATE_READY
        self._timeout_handle = None
        self.client = client
        self.message = message
        self.player = player
        self.session = session
        self.single_player = single_player
        self.waiter = waiter
        
        if game_ended:
            timeout_handle = None
        else:
            timeout_handle = EVENT_LOOP.call_after(GAME_21_RUNNER_TIMEOUT, self._invoke_timeout)
        self._timeout_handle = timeout_handle
        
        if not game_ended:
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
        client = self.client
        player = self.player
        session = self.session
        
        # Do nothing if other user clicked.
        if (interaction_event.user is not self.player.user):
            await client.interaction_component_acknowledge(interaction_event)
            return
        
        # Are we ready? If we arent acknowledge the event and we can store it as the latest event. Great success.
        if self._ui_state != UI_STATE_READY:
            await try_acknowledge(client, interaction_event, player, session, self.single_player)
            return
        
        custom_id = interaction_event.custom_id
        if (custom_id == GAME_21_CUSTOM_ID_NEW):
            player.hand.pull_card(session.deck)
            game_ended = player.hand.is_finished()
        
        elif (custom_id == GAME_21_CUSTOM_ID_STOP):
            game_ended = True
        
        else:
            # should not happen
            return
        
        if game_ended:
            self._ui_state = UI_STATE_SWITCHING_CONTEXT
            if self.waiter.set_result_if_pending(True):
                player.state = PLAYER_STATE_FINISH
            
            self._invoke_cancellation(False)
            if self.single_player:
                # If we are in single player, we will edit the message right after outside, so do not
                store_event(player, session, self.single_player, interaction_event)
                return
            
            await try_edit_response(
                client,
                interaction_event,
                player.latest_interaction_event,
                self.message,
                player,
                session,
                self.single_player,
                GAME_21_ROW_DISABLED,
                build_gamble_after_embed(player.hand, session.amount),
            )
            return
        
        self._ui_state = UI_STATE_EDITING
        try:
            success = await try_edit_response(
                client,
                interaction_event,
                player.latest_interaction_event,
                self.message,
                player,
                session,
                self.single_player,
                GAME_21_ROW_ENABLED,
                build_gamble_embed(player.hand, session.amount),
            )
        except GeneratorExit:
            self._invoke_cancellation(False)
            raise
        
        except BaseException as exception:
            self._invoke_cancellation(False)
            if should_render_exception(exception):
                await client.events.error(client, f'{type(self).__name__}.__main__', exception)
            
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
        
        if self.waiter.set_result_if_pending(timeout):
            self.player.state = PLAYER_STATE_CANCELLED_TIMEOUT if timeout else PLAYER_STATE_IN_GAME_ERROR
    
    
    def _invoke_timeout(self):
        """
        Invokes timeout and edits the gui's message with a timeout embed.
        """
        self._invoke_cancellation(True)
        if not self.single_player:
            Task(
                EVENT_LOOP,
                try_edit_response(
                    self.client,
                    None,
                    self.player.latest_interaction_event,
                    self.message,
                    self.player,
                    self.session,
                    self.single_player,
                    GAME_21_ROW_DISABLED,
                    build_gamble_timeout_embed(self.player.hand, self.session.amount),
                ),
            )
