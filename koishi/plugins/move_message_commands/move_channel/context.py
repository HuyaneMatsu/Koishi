__all__ = ()

from hata import DiscordException, ERROR_CODES, Embed, KOKORO, now_as_id, seconds_to_elapsed_time
from scarletio import CancelledError, LOOP_TIME, Task, sleep

from ...move_message_core import create_webhook_message, get_files

from .constants import (
    CHANNEL_MOVER_ACTIVE_FROM, CHANNEL_MOVER_ACTIVE_TO, CHANNEL_MOVER_BY_STATUS_MESSAGE_ID, CHANNEL_MOVE_COMPONENTS,
    CHANNEL_MOVE_STATE_CANCELLED, CHANNEL_MOVE_STATE_CLIENT_SHUTDOWN, CHANNEL_MOVE_STATE_ERROR,
    CHANNEL_MOVE_STATE_FINISHED, CHANNEL_MOVE_STATE_NONE, CHANNEL_MOVE_STATE_WEBHOOK_DELETED, UPDATE_INTERVAL
)
from .helpers import add_embed_field, add_embed_thumbnail, build_components_continue


STATUS_FOOTERS = {
    CHANNEL_MOVE_STATE_NONE: f'In progress. This message is updated every {UPDATE_INTERVAL:.0f} seconds.',
    CHANNEL_MOVE_STATE_FINISHED: 'Finished',
    CHANNEL_MOVE_STATE_WEBHOOK_DELETED: 'Error: The webhook the client used for moving the messages has been deleted.',
    CHANNEL_MOVE_STATE_ERROR: 'Error: An unexpected error occurred.',
    CHANNEL_MOVE_STATE_CLIENT_SHUTDOWN: 'Shutdown: The client is shutting down, please try again later.',
    CHANNEL_MOVE_STATE_CANCELLED: 'Cancelled',
}


STATUS_COMPONENTS = {
    CHANNEL_MOVE_STATE_NONE: lambda context: CHANNEL_MOVE_COMPONENTS,
    CHANNEL_MOVE_STATE_FINISHED: None,
    CHANNEL_MOVE_STATE_WEBHOOK_DELETED: lambda context: build_components_continue(
        context.source_channel, context.target_channel, context.last_message_id
    ),
    CHANNEL_MOVE_STATE_ERROR : None,
    CHANNEL_MOVE_STATE_CLIENT_SHUTDOWN: lambda context: build_components_continue(
        context.source_channel, context.target_channel, context.last_message_id
    ),
    CHANNEL_MOVE_STATE_CANCELLED : lambda context: build_components_continue(
        context.source_channel, context.target_channel, context.last_message_id
    ),
}


class ChannelMoverContext:
    """
    Channel mover context containing information about channel moving.
    
    Attributes
    ----------
    message_cache : `None`, `list` of ``Message``
        Message cache of already requested messages.
    message_request_more : `bool`
        Whether more message should be requested.
    state : `int`
        An integer representing the state of the message mover.
    client : ``Client``
        The used client for moving.
    source_channel : ``Channel``
        The channel to move the messages from.
    target_channel : ``Channel``
        Target channel to move the messages to.
    total_moved_messages : `int`
        The total amount of messages moved.
    status_message_update_waiter : `None`, ``Future``
        Message status update waiter.
    webhook : ``Webhook``
        Webhook to use for moving the messages.
    started_at : `int`
        When message moving was started in unix time.
    last_message_id : `int`
        The last moved message's identifier.
    status_message : `None`, ``Message``
        The message notifying the user in dm about the move's state.
    move_channel_task : `None`, ``Task`` of ``.move_channel_loop``
        Move channel loop task.
    status_update_task : `None`, ``Task`` of ``.status_update_loop``
        Status update loop task.
    """
    __slots__ = (
        'message_cache', 'message_request_more', 'state', 'client', 'source_channel', 
        'target_channel', 'webhook', 'total_moved_messages', 'status_message_update_waiter', 'started_at',
        'last_message_id', 'status_message', 'move_channel_task', 'status_update_task'
    )
    
    async def __new__(cls, client, event, source_channel, target_channel, last_message_id, webhook):
        """
        Creates a nw channel mover context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The used client for moving.
        event : ``InteractionEvent``
            The received interaction event.
        source_channel : ``Channel``
            The channel to move the messages from.
        target_channel : ``Channel``
            Target channel to move the messages to.
        last_message_id : `int`
            The message identifier to continue from.
        webhook : ``Webhook``
            Webhook to use for moving the messages.
        """
        self = object.__new__(cls)
        self.last_message_id = last_message_id
        self.message_cache = None
        self.message_request_more = True
        self.state = CHANNEL_MOVE_STATE_NONE
        self.client = client
        self.source_channel = source_channel
        self.target_channel = target_channel
        self.webhook = webhook
        self.total_moved_messages = 0
        self.status_message_update_waiter = None
        self.started_at = LOOP_TIME()
        self.status_message = None
        self.move_channel_task = None
        self.status_update_task = None
        
        try:
            success = await self.create_status_message(event)
        except:
            self.discard()
            raise
        
        if not success:
            self.discard()
            await client.interaction_followup_message_create(
                event,
                'Creating DM status message failed.',
                show_for_invoking_user_only = True,
            )
            return
        
        self.move_channel_task = Task(KOKORO, self.move_channel_loop())
        self.status_update_task = Task(KOKORO, self.status_update_loop())
        
        CHANNEL_MOVER_BY_STATUS_MESSAGE_ID[self.status_message.id] = self
        
        return self
    
    
    async def poll_message(self):
        """
        Polls the next message to move.
        
        This method is a coroutine.
        
        Returns
        -------
        message : `None`, ``Message``
        """
        message_cache = self.message_cache
        if (message_cache is not None) and message_cache:
            return message_cache.pop()
        
        if not self.message_request_more:
            return
        
        message_cache = await self.client.message_get_chunk(self.source_channel, after = self.last_message_id)
        self.message_cache = message_cache
        
        if len(message_cache) < 100:
            self.message_request_more = False
        
        if message_cache:
            return message_cache.pop()
    
    
    def is_polling_done(self):
        """
        Returns whether polling is done.
        
        Returns
        -------
        is_polling_done : `bool`
        """
        if self.message_request_more:
            return False
        
        if self.message_cache:
            return False
        
        return True
    
    
    async def move_message(self, message):
        """
        Copies the given messages into the target channel.
        
        This function is a coroutine.
        
        Parameters
        ----------
        message : ``Message``
            The message to move.
        """
        target_channel = self.target_channel
        if target_channel.is_in_group_thread():
            thread_id = target_channel.id
        else:
            thread_id = 0
        
        files = await get_files(self.client, message)
        try:
            await create_webhook_message(self.client, self.webhook, message, thread_id, files)
        except:
            # Unallocate files if exception occurs
            files = None
            raise
    
    
    def get_estimated_percentage(self):
        """
        Gets estimated percentage how done the moving is.
        
        Returns
        -------
        estimated_percentage : `int`
        """
        now_id = now_as_id()
        message_id = self.last_message_id
        if message_id >= now_id:
            return 100.0
        
        channel_id = self.source_channel.id
        if channel_id >= message_id:
            return 0.0
        
        if self.is_polling_done():
            return 100.0
        
        return (1.0 - (now_id - message_id) / (now_id - channel_id)) * 100.0
    
    
    def get_status_embed_and_components(self):
        """
        Creates status embed and components.
        
        Returns
        -------
        embed : ``Embed``
        components : `None`, ``Component``
        """
        embed = Embed('Moving channel messages')
        add_embed_thumbnail(embed, self.source_channel.guild)
        add_embed_field(embed, 'From', self.source_channel.name, True)
        add_embed_field(embed, 'To', self.target_channel.name, True)
        add_embed_field(embed, 'Elapsed time', seconds_to_elapsed_time(LOOP_TIME() - self.started_at))
        add_embed_field(embed, 'Messages moved', str(self.total_moved_messages), True)
        add_embed_field(embed, 'Estimated percentage', format(self.get_estimated_percentage(), '.02f'), True)
        add_embed_field(embed, 'Last message id', str(self.last_message_id), True)
        
        state = self.state
        footer = STATUS_FOOTERS.get(state, None)
        if (footer is not None):
            embed.add_footer(footer)
        
        components_factory = STATUS_COMPONENTS.get(state, None)
        if components_factory is None:
            components = None
        else:
            components = components_factory(self)
        
        return embed, components
    
    
    async def create_status_message(self, event):
        """
        Creates the initial status message to notify the user.
        
        This function is a coroutine.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The source interaction event.
        
        Returns
        -------
        success : `bool`
        """
        try:
            channel = await self.client.channel_private_create(event.user)
        except ConnectionError:
            return False
        
        embed, components = self.get_status_embed_and_components()
        
        try:
            message = await self.client.message_create(channel, embed = embed, components = components)
        except ConnectionError:
            return False
        
        except DiscordException as err:
            if err.code == ERROR_CODES.cannot_message_user:
                return False
            
            raise
        
        # We sent an empty message -> should not happen.
        if message is None:
            return False
        
        self.status_message = message
        return True
    
    
    async def update_status_message(self):
        """
        Updates the status message.
        
        This method is a coroutine.
        """
        embed, components = self.get_status_embed_and_components()
        await self.client.message_edit(self.status_message, embed = embed, components = components)
    
    
    async def send_done_notification(self):
        """
        Sends done notification.
        
        This method is a coroutine.
        """
        state = self.state
        if state in (CHANNEL_MOVE_STATE_NONE, CHANNEL_MOVE_STATE_CANCELLED):
            return
        
        embed = Embed('Moving channel messages ended')
        add_embed_thumbnail(embed, self.source_channel.guild)
        
        status_message = STATUS_FOOTERS.get(state, None)
        if (status_message is not None):
            add_embed_field(embed, 'Status', status_message)
        
        await self.client.message_create(self.status_message, embed = embed)
    
    
    async def status_update_loop(self):
        """
        Updates the status message in regular intervals.
        
        This method is a coroutine.
        """
        self.status_message_update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
        
        while self.state == CHANNEL_MOVE_STATE_NONE:
            set_value = await self.status_message_update_waiter
            # sleep sets by `None`
            if set_value is not None:
                break
            
            self.status_message_update_waiter = sleep(UPDATE_INTERVAL, KOKORO)
            await self.update_status_message()
            continue
        
        await self.update_status_message()
        await self.send_done_notification()
        return
    
    
    async def move_channel_loop(self):
        """
        Moves the messages of the channel in a loop.
        
        This method is a coroutine.
        """
        try:
            while self.state == CHANNEL_MOVE_STATE_NONE:
                message = await self.poll_message()
                if message is None:
                    break
                
                try:
                    await self.move_message(message)
                except DiscordException as err:
                    if err.code == ERROR_CODES.unknown_webhook:
                        self.set_status_update_waiter_webhook_deleted()
                        return
                    
                    raise
                
                self.last_message_id = message.id
                self.total_moved_messages += 1
        
        except GeneratorExit:
            raise
        
        except CancelledError:
            raise
        
        except BaseException as err:
            self.set_status_update_waiter_error()
            await self.client.events.error(self.client, repr(self), err)
            return
        
        finally:
            self.discard()
        
        self.set_status_update_waiter_finished()
    
    
    def set_state(self, state):
        """
        Sets the state of channel mover if applicable.
        
        Parameters
        ----------
        state : `int`
            The state to set.
        """
        if self.state == CHANNEL_MOVE_STATE_NONE:
            self.state = state
    
    
    def set_status_update_waiter(self):
        """
        Sets the status update waiter.
        """
        status_message_update_waiter = self.status_message_update_waiter
        if (status_message_update_waiter is not None):
            self.status_message_update_waiter = None
            status_message_update_waiter.set_result(...)
    
    
    def set_status_update_waiter_finished(self):
        """
        Sets the status update waiter as we are finished.
        """
        self.set_state(CHANNEL_MOVE_STATE_FINISHED)
        self.set_status_update_waiter()
    
    
    def set_status_update_waiter_error(self):
        """
        Sets the status update waiter as we got an unexpected exception.
        """
        self.set_state(CHANNEL_MOVE_STATE_ERROR)
        self.set_status_update_waiter()
    
    
    def set_status_update_waiter_webhook_deleted(self):
        """
        Sets the status update waiter as we got a webhook deleted exception.
        """
        self.set_state(CHANNEL_MOVE_STATE_WEBHOOK_DELETED)
        self.set_status_update_waiter()
    
    
    def set_status_update_waiter_shutdown(self):
        """
        Sets status update waiter that we are shutting down.
        """
        self.set_state(CHANNEL_MOVE_STATE_CLIENT_SHUTDOWN)
        self.set_status_update_waiter()
    
    
    def shutdown(self):
        """
        Shuts down the channel mover.
        
        Returns
        -------
        task : `None`, ``Task``
        """
        status_update_task = self.status_update_task
        if (status_update_task is None):
            return
        
        self.set_status_update_waiter_shutdown()
        
        move_channel_task = self.move_channel_task
        if (move_channel_task is not None):
            self.move_channel_task = None
            move_channel_task.cancel()
            move_channel_task = None
        
        return status_update_task
    
    
    def set_status_update_waiter_cancelled(self):
        """
        Cancels down the channel mover.
        
        Returns
        -------
        task : `None`, ``Task``
        """
        self.set_state(CHANNEL_MOVE_STATE_CANCELLED)
        self.set_status_update_waiter()
        
    
    def discard(self):
        """
        Discards self from channel moves.
        """
        CHANNEL_MOVER_ACTIVE_FROM.discard(self.source_channel.id)
        CHANNEL_MOVER_ACTIVE_TO.discard(self.target_channel.id)
        
        status_message = self.status_message
        if (status_message is not None):
            try:
                del CHANNEL_MOVER_BY_STATUS_MESSAGE_ID[status_message.id]
            except KeyError:
                pass
