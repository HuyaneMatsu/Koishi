__all__ = ()

from hata import DiscordException, ERROR_CODES, InteractionType, KOKORO
from hata.ext.slash import Timeouter
from scarletio import CancelledError, Task

from .action_processors import ACTION_PROCESSORS
from .component_building import (
    build_components_end_screen, build_components_in_game, build_components_in_menu, build_components_shutdown
)
from .constants import (
    DUNGEON_SWEEPER_GAMES, RUNNER_STATE_CLOSED, RUNNER_STATE_END_SCREEN, RUNNER_STATE_IN_GAME, RUNNER_STATE_IN_MENU,
    RUNNER_STATE_VALUE_TO_NAME, UI_STATE_CANCELLED, UI_STATE_CANCELLING, UI_STATE_EDITING, UI_STATE_READY,
    UI_STATE_SWITCHING_CONTEXT, UI_STATE_VALUE_TO_NAME, UI_TIMEOUT
)
from .helpers import disable_interactive_components
from .queries import get_user_state, save_user_game_state, save_user_game_state_init_failure


def build_response_components(runner_state, user_state):
    """
    Builds the response components for the given runner state.
    
    Parameters
    ----------
    runner_state : `int`
        The state of the runner.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | RUNNER_STATE_IN_MENU          | 1     |
        +-------------------------------+-------+
        | RUNNER_STATE_IN_GAME          | 2     |
        +-------------------------------+-------+
        | RUNNER_STATE_END_SCREEN       | 3     |
        +-------------------------------+-------+
    
    user_state : ``UserState``
        The user's state.
    
    Returns
    -------
    components : ``None | tuple<Component>``
    """
    while True:
        if runner_state == RUNNER_STATE_IN_MENU:
            components = build_components_in_menu(user_state)
            break
        
        game_state = user_state.game_state
        if game_state is None:
            components = None
            break
        
        if runner_state == RUNNER_STATE_IN_GAME:
            components = build_components_in_game(game_state)
            break
        
        if runner_state == RUNNER_STATE_END_SCREEN:
            components = build_components_end_screen(game_state)
            break
        
        components = None
        break
    
    return components



async def try_create_initial_message(client, interaction_event, components):
    """
    Tries to create an initial message.
    
    Parameters
    ----------
    client : ``Client``
        Client to create message with.
    
    interaction_event : ``InteractionEvent``
        Interaction event to create message with.
    
    components : ``tuple<Component>``
        Components to create message with.
    
    Returns
    -------
    message_and_interaction_event : ``(None | Message, None | InteractionEvent)``
        Returning `None` as interaction event means that it could not been used.
        Returning `None` as message means that the message could not been created.
    """
    try:
        if interaction_event.is_acknowledging() or interaction_event.is_acknowledged():
            message = await client.interaction_followup_message_create(interaction_event, components = components)
        else:
            message = await client.interaction_response_message_create(interaction_event, components = components)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code != ERROR_CODES.unknown_interaction # interaction expired.
        ):
            raise
    
    else:
        return message, interaction_event
    
    # Try sending normal message if we did not crash really hard
    channel = interaction_event.channel
    permissions = channel.cached_permissions_for(client)
    if channel.is_in_group_thread():
        can_create_message = permissions.send_messages_in_threads
    else:
        can_create_message = permissions.send_messages
    
    if not can_create_message:
        return None, None
    
    try:
        message = await client.message_create(channel, components = components)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code not in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user has dm-s disallowed
            )
        ):
            raise
    
    else:
        return message, None
    
    return None, None


async def try_edit_message(client, message, new_interaction_event, old_interaction_event, components):
    """
    Tries to edit the given message.
    
    Parameters
    ----------
    client : ``Client``
        Client to create message with.
    
    message : ``Message``
        The message to edit.
    
    new_interaction_event : ``None | InteractionEvent``
        Newly received interaction event.
    
    old_interaction_event : ``None | InteractionEvent``
        Previously received interaction event.
    
    components : ``tuple<Component>``
        Components to create message with.
    
    Returns
    -------
    message_and_interaction_event : ``(None | Message, None | InteractionEvent)``
        Returning `None` as interaction event means that non could been used.
        Returning `None` as message means that the message could not been edited.
    """
    for interaction_event in (new_interaction_event, old_interaction_event):
        if interaction_event is None:
            continue
        
        try:
            if (
                interaction_event.type is InteractionType.application_command or
                interaction_event.is_acknowledging() or
                interaction_event.is_acknowledged()
            ):
                await client.interaction_response_message_edit(interaction_event, components = components)
            else:
                await client.interaction_component_message_edit(interaction_event, components = components)
        except GeneratorExit:
            raise
        
        except ConnectionError:
            pass
        
        except DiscordException as exception:
            if (
                exception.status < 500 and
                exception.code not in (
                    ERROR_CODES.unknown_interaction, # interaction expired.
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                )
            ):
                raise
        
        else:
            return message, interaction_event
    
    # Try edit the message normally if we did not crash too hard.
    channel = interaction_event.channel
    permissions = channel.cached_permissions_for(client)
    if channel.is_in_group_thread():
        can_create_message = permissions.send_messages_in_threads
    else:
        can_create_message = permissions.send_messages
    
    if not can_create_message:
        return None, None
    
    try:
        message = await client.message_edit(message, components = components)
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code not in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user has dm-s disallowed
            )
        ):
            raise
    
    else:
        return message, None
    
    return None, None


class DungeonSweeperRunner:
    """
    Dungeon sweeper game runner.
    
    Attributes
    ----------
    _canceller : None`, `CoroutineFunction`
        Canceller set as `._canceller_function``, meanwhile the gui is not cancelled.
    
    _ui_state : `int`
        The gui's state.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | UI_STATE_NONE                | 0     |
        +===============================+=======+
        | UI_STATE_READY               | 1     |
        +-------------------------------+-------+
        | UI_STATE_EDITING             | 2     |
        +-------------------------------+-------+
        | UI_STATE_CANCELLING          | 3     |
        +-------------------------------+-------+
        | UI_STATE_CANCELLED           | 4     |
        +-------------------------------+-------+
        | UI_STATE_SWITCHING_CONTEXT   | 5     |
        +-------------------------------+-------+
    
    _runner_state : `int`
        The state of the runner.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | RUNNER_STATE_IN_MENU          | 1     |
        +-------------------------------+-------+
        | RUNNER_STATE_IN_GAME          | 2     |
        +-------------------------------+-------+
        | RUNNER_STATE_END_SCREEN       | 3     |
        +-------------------------------+-------+
    
    _timeouter : `None`, ``Timeouter``
        Timeouts the gui if no action is performed within the expected time.
    
    client : ``Client``
        The client, who executes the requests.
    
    latest_interaction_event : ``InteractionEvent``
        The latest interaction event of runner.
    
    message : ``Message``
        The message edited by the runner.
    
    user_id : `int`
        The user's identifier, who requested the game.
    
    user_state : ``UserState``
        The user's user state.
    """
    __slots__ = (
        '_canceller', '_ui_state', '_runner_state', '_timeouter', 'client', 'latest_interaction_event', 'message',
        'user_id', 'user_state'
    )
    
    async def __new__(cls, client, interaction_event):
        """
        Creates a new dungeon sweeper runner.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The source client.
        
        interaction_event : ``InteractionEvent``
            The received client.
        """
        user_id = interaction_event.user_id
        try:
            existing_game = DUNGEON_SWEEPER_GAMES[user_id]
        except KeyError:
            pass
        else:
            if (existing_game is not None):
                await existing_game.renew(interaction_event)
            
            else:
                try:
                    await client.interaction_response_message_create(
                        interaction_event,
                        'A game is already starting somewhere else.',
                        show_for_invoking_user_only = True,
                    )
                except GeneratorExit:
                    raise
                
                except ConnectionError:
                    pass
                
                except DiscordException as exception:
                    if exception.code != ERROR_CODES.unknown_interaction:
                        raise
                    
            return
        
        DUNGEON_SWEEPER_GAMES[user_id] = None
        user_state = None
        message = None
        try:
            await client.interaction_application_command_acknowledge(interaction_event, False)
            user_state = await get_user_state(user_id)
            
            game_state = user_state.game_state
            if game_state is None:
                runner_state = RUNNER_STATE_IN_MENU
            else:
                if game_state.is_done():
                    runner_state = RUNNER_STATE_END_SCREEN
                else:
                    runner_state = RUNNER_STATE_IN_GAME
            
            components = build_response_components(runner_state, user_state)
            if components is None:
                # Hacker trying to hack Huyane
                return
            
            message, interaction_event = await try_create_initial_message(client, interaction_event, components)
        
        except GeneratorExit:
            del DUNGEON_SWEEPER_GAMES[user_id]
            raise
        
        else:
            if (message is None):
                return
        
        finally:
            if (message is None):
                if (user_state is not None):
                    await save_user_game_state_init_failure(user_state)
                
                del DUNGEON_SWEEPER_GAMES[user_id]
        
        
        self = object.__new__(cls)
        self._canceller = cls._canceller_function
        self.client = client
        self.latest_interaction_event = interaction_event
        self.user_id = user_id
        self.message = message
        self.user_state = user_state
        self._timeouter = Timeouter(self, UI_TIMEOUT)
        self._ui_state = UI_STATE_READY
        self._runner_state = runner_state
        
        DUNGEON_SWEEPER_GAMES[user_id] = self
        client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def renew(self, new_client, interaction_event):
        """
        Renews the interaction gui creating a new message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        new_client : ``Client``
            The new client to work with.
        
        interaction_event : ``InteractionEvent``
            The received interaction event.
        """
        if self._ui_state in (UI_STATE_CANCELLING, UI_STATE_CANCELLED, UI_STATE_SWITCHING_CONTEXT):
            return
        
        user_state = self.user_state
        runner_state = self._runner_state
        
        components = build_response_components(runner_state, user_state)
        if components is None:
            # Hacker trying to hack Huyane
            return
        
        self._ui_state = UI_STATE_SWITCHING_CONTEXT
        
        message = None
        try:
            message, interaction_event = await try_create_initial_message(new_client, interaction_event, components)
        except GeneratorExit:
            raise
        
        else:
            if message is None:
                return
        
        finally:
            if (message is None):
                if self._ui_state == UI_STATE_SWITCHING_CONTEXT:
                    self._ui_state = UI_STATE_READY
        
        old_client = self.client
        disable_interactive_components(components)
        
        try:
            await try_edit_message(
                old_client, self.message, self.latest_interaction_event, None, components
            )
        except GeneratorExit:
            raise
        
        except BaseException as exception:
            await old_client.events.error(old_client, f'{self!r}.renew', exception)
        
        
        old_client.slasher.remove_component_interaction_waiter(self.message, self)
        new_client.slasher.add_component_interaction_waiter(message, self)
        
        self.client = new_client
        self.message = message
        self.latest_interaction_event = interaction_event
        
        if self._ui_state == UI_STATE_SWITCHING_CONTEXT:
            self._ui_state = UI_STATE_READY
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.set_timeout(UI_TIMEOUT)
    
    
    async def __call__(self, interaction_event):
        """
        Calls the dungeon sweeper runner, processing a component event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            The received client.
        """
        while True:
            client = self.client
            if interaction_event.user_id != self.user_id:
                break
            
            ui_state = self._ui_state
            if ui_state != UI_STATE_READY:
                break
            
            try:
                action_processor = ACTION_PROCESSORS[interaction_event.custom_id]
            except KeyError:
                break
            
            user_state = self.user_state
            if not await action_processor(self):
                break
            
            runner_state = self._runner_state
            
            components = build_response_components(runner_state, user_state)
            if components is None:
                if runner_state == RUNNER_STATE_CLOSED:
                    self.cancel(CancelledError())
                    return
                
                break
            
            self._ui_state = UI_STATE_EDITING
    
            message = None
            try:
                message, interaction_event = await try_edit_message(
                    self.client, self.message, interaction_event, self.latest_interaction_event, components
                )
            except BaseException as err:
                self.cancel(err)
                raise
            
            else:
                if message is None:
                    self.cancel(None)
                    return
            
            self.message = message
            self.latest_interaction_event = interaction_event
            
            if self._ui_state == UI_STATE_EDITING:
                self._ui_state = UI_STATE_READY
            
            timeouter = self._timeouter
            if (timeouter is not None):
                timeouter.set_timeout(UI_TIMEOUT)
            return
        
        
        try:
            await client.interaction_component_acknowledge(interaction_event)
        except GeneratorExit:
            raise
        
        except ConnectionError:
            pass
        
        except DiscordException as exception:
            if (
                exception.status < 500 and
                exception.code not in (
                    ERROR_CODES.unknown_interaction, # interaction expired.
                )
            ):
                await client.events.error(client, f'{self!r}.__call__', exception)
    
    
    def cancel(self, exception = None):
        """
        Cancels the dungeon sweeper gui with the given exception if applicable.
        
        Parameters
        ----------
        exception : `None`, `BaseException`, Optional
            Exception to cancel the pagination with. Defaults to `None`
        
        Returns
        -------
        canceller_task : ``None | Task``
        """
        if self._ui_state in (UI_STATE_READY, UI_STATE_EDITING, UI_STATE_CANCELLING):
            self._ui_state = UI_STATE_CANCELLED
        
        canceller = self._canceller
        if canceller is None:
            return
        
        self._canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(KOKORO, canceller(self, exception))
    
    
    async def _canceller_function(self, exception):
        """
        Cancels the gui state, saving the current game if needed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, `BaseException`
        """
        await save_user_game_state(self.user_state)
        
        user_id = self.user_id
        if DUNGEON_SWEEPER_GAMES.get(user_id, None) is self:
            del DUNGEON_SWEEPER_GAMES[user_id]
        
        
        client = self.client
        message = self.message
        
        client.slasher.remove_component_interaction_waiter(message, self)
        
        
        if self._ui_state == UI_STATE_SWITCHING_CONTEXT:
            # the message is not our, we should not do anything with it.
            return
        
        self._ui_state = UI_STATE_CANCELLED
        
        if not await self._handle_close_exception(exception):
            await client.events.error(client, f'{self!r}._canceller_function', exception)

    
    async def _handle_close_exception(self, exception):
        """
        Handles close exception if any.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None | BaseException`
            The close exception to handle.
        
        Returns
        -------
        exception_handled : `bool`
            Whether the exception was handled.
        """
        if exception is None:
            return True
        
        client = self.client
        message = self.message
        
        if isinstance(exception, CancelledError):
            try:
                await client.message_delete(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return True
                
                if isinstance(err, DiscordException):
                    if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                    ):
                        return True
                
                await client.events.error(client, f'{self!r}._handle_close_exception', exception)
            
            return True
        
        if isinstance(exception, TimeoutError):
            components = build_response_components(self._runner_state, self.user_state)
            if components is None:
                return True
            
            disable_interactive_components(components)
            
            try:
                await try_edit_message(
                    self.client, self.message, self.latest_interaction_event, None, components
                )
            except GeneratorExit:
                raise
            
            except BaseException as exception:
                await client.events.error(client, f'{self!r}._handle_close_exception', exception)
            
            return True
        
        if isinstance(exception, SystemExit):
            components = build_components_shutdown()
            
            try:
                await try_edit_message(
                    self.client, self.message, self.latest_interaction_event, None, components
                )
            except GeneratorExit:
                raise
            
            except BaseException as exception:
                await client.events.error(client, f'{self!r}._handle_close_exception', exception)
            
            return True
        
        
        if isinstance(exception, PermissionError):
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the dungeon sweep runner's representation."""
        repr_parts = [
            '<', type(self).__name__,
            ' client = ', repr(self.client),
            ', channel = ', repr(self.message.channel),
            ', ui_state = '
        ]
        
        ui_state = self._ui_state
        
        repr_parts.append(repr(ui_state))
        repr_parts.append(' (')
        ui_state_name = UI_STATE_VALUE_TO_NAME[ui_state]
        repr_parts.append(ui_state_name)
        repr_parts.append('), ')
        
        runner_state = self._runner_state
        repr_parts.append(repr(runner_state))
        repr_parts.append(' (')
        runner_state_name = RUNNER_STATE_VALUE_TO_NAME[runner_state]
        repr_parts.append(runner_state_name)
        repr_parts.append('), ')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
