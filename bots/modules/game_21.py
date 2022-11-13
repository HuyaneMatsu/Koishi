__all__ = ()

from random import random
from itertools import chain

from scarletio import Task, Future, WaitTillAll, future_or_timeout
from hata import Client, Embed, BUILTIN_EMOJIS, DiscordException, KOKORO, ERROR_CODES, InteractionType
from hata.ext.slash import Button, Row
from hata.ext.slash.menus.menu import GUI_STATE_READY, GUI_STATE_EDITING, GUI_STATE_CANCELLING, \
    GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CONTEXT, Timeouter

from sqlalchemy.sql import select

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE
from bot_utils.constants import EMOJI__HEART_CURRENCY, IN_GAME_IDS, COLOR__GAMBLING

SLASH_CLIENT: Client


CARD_TYPES = (
    BUILTIN_EMOJIS['spades'].as_emoji,
    BUILTIN_EMOJIS['clubs'].as_emoji,
    BUILTIN_EMOJIS['hearts'].as_emoji,
    BUILTIN_EMOJIS['diamonds'].as_emoji,
)

CARD_NUMBERS = (
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['nine'].as_emoji,
    BUILTIN_EMOJIS['keycap_ten'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_j'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_q'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_k'].as_emoji,
    BUILTIN_EMOJIS['a'].as_emoji,
)

DECK_SIZE   = len(CARD_TYPES) * len(CARD_NUMBERS)
ACE_INDEX   = len(CARD_NUMBERS) - 1
BET_MIN     = 10

@SLASH_CLIENT.interactions(name = '21', is_global = True)
async def game_21(client, event,
    amount : ('int', 'The amount of hearts to bet'),
    mode : ([('single-player', 'sg'), ('multi-player', 'mp')], 'Game mode, yayyy') = 'sg',
):
    """Starts a card game where you can bet your hearts."""
    is_multi_player = (mode == 'mp')
    
    embed = game_21_precheck(client, event.user, event.channel, amount, is_multi_player)
    if (embed is None):
        await client.interaction_application_command_acknowledge(event)
    else:
        await client.interaction_response_message_create(event, embed = embed)
        return
    
    if is_multi_player:
        coroutine_function = game_21_multi_player
    else:
        coroutine_function = game_21_single_player
    
    await coroutine_function(client, event, amount)


def should_render_exception(exception):
    if isinstance(exception, ConnectionError):
        # no internet
        return False
    
    if isinstance(exception, DiscordException) and exception.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user dm-s disabled or bot blocked.
            ):
         return False
    
    return True



class Game21Base:
    __slots__ = ('guild', 'all_pulled')
    def __new__(cls, guild):
        self = object.__new__(cls)
        self.guild = guild
        self.all_pulled = []
        return self
    
    def create_user_player(self, user):
        return Game21Player(self, user)
    
    def create_bot_player(self, user):
        player = Game21Player(self, user)
        player.auto_finish()
        return player
    
    def pull_card(self):
        all_pulled = self.all_pulled
        card = int((DECK_SIZE - len(all_pulled)) * random())
        for pulled in all_pulled:
            if pulled > card:
                break
            
            card += 1
            continue
        
        all_pulled.append(card)
        all_pulled.sort()
        
        return card

class Game21Player:
    __slots__ = ('parent', 'user', 'hand', 'total', 'ace')
    def __new__(cls, parent, user):
        hand = []
        total = 0
        ace = 0
        
        while True:
            card = parent.pull_card()
            
            hand.append(card)
            
            number_index = card % len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index + 2
            
            total += card_weight
            
            if total > 10 and len(hand) >= 2:
                break
        
        # We might draw 2 ace, at that case we hit 22.
        if total > 21:
            ace -= 1
            total -= 10
        
        self = object.__new__(cls)
        self.parent = parent
        self.user = user
        self.hand = hand
        self.total = total
        self.ace = ace
        return self
    
    def auto_finish(self):
        hand = self.hand
        total = self.total
        ace = self.ace
        
        while True:
            if total > (17 if ace else 15):
                break
            
            card = self.parent.pull_card()
            
            hand.append(card)
            
            number_index = card % len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index + 2
            
            total += card_weight
            
            while total>21 and ace:
                total -= 10
                ace -= 1
            
            continue
        
        self.total = total
        self.ace = ace
    
    def pull_card(self):
        hand = self.hand
        total = self.total
        ace = self.ace
        
        card = self.parent.pull_card()
        
        hand.append(card)
        
        number_index = card % len(CARD_NUMBERS)
        if number_index == ACE_INDEX:
            ace += 1
            card_weight = 11
        elif number_index > 7:
            card_weight = 10
        else:
            card_weight = number_index + 2
        
        total += card_weight
        
        while total>21 and ace:
            total -= 10
            ace -= 1
            
        self.total = total
        self.ace = ace
        
        # Return whether the user is done.
        if total >= 21:
            return True
        
        return False
    
    def add_done_embed_field(self, embed):
        field_content = []
        
        for round_, card in enumerate(self.hand, 1):
            type_index, number_index = divmod(card, len(CARD_NUMBERS))
            field_content.append('Round ')
            field_content.append(str(round_))
            field_content.append(': ')
            field_content.append(CARD_TYPES[type_index])
            field_content.append(' ')
            field_content.append(CARD_NUMBERS[number_index])
            field_content.append('\n')
        
        embed.add_field(f'{self.user.name_at(self.parent.guild)}\'s cards\'\nWeight: {self.total}',
            ''.join(field_content), inline=True)
    
    def add_hand(self, embed):
        for round_, card in enumerate(self.hand, 1):
            type_index, number_index = divmod(card, len(CARD_NUMBERS))
            embed.add_field(f'Round {round_}',
                f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
        
    def create_gamble_embed(self, amount):
        embed = Embed(f'How to gamble {amount} {EMOJI__HEART_CURRENCY.as_emoji}',
            f'You have cards equal to {self.total} weight at your hand.',
            color = COLOR__GAMBLING)
        
        self.add_hand(embed)
        
        return embed
    
    def create_after_embed(self, amount):
        embed = Embed(f'Gambled {amount} {EMOJI__HEART_CURRENCY.as_emoji}',
            (
                f'You have cards equal to {self.total} weight at your hand.\n'
                'Go back to the other channel and wait till all the player finishes the game and the winner will be '
                'announced!'
            ),
            color = COLOR__GAMBLING,
        )
        
        self.add_hand(embed)
        
        return embed

GAME_21_EMOJI_NEW = BUILTIN_EMOJIS['new']
GAME_21_EMOJI_STOP = BUILTIN_EMOJIS['octagonal_sign']

GAME_21_CUSTOM_ID_NEW = '21.new'
GAME_21_CUSTOM_ID_STOP = '21.stop'

GAME_21_BUTTON_NEW_ENABLED = Button(
    emoji = GAME_21_EMOJI_NEW,
    custom_id = GAME_21_CUSTOM_ID_NEW,
)

GAME_21_BUTTON_NEW_DISABLED = GAME_21_BUTTON_NEW_ENABLED.copy_with(
    enabled = False,
)

GAME_21_BUTTON_STOP_ENABLED = Button(
    emoji = GAME_21_EMOJI_STOP,
    custom_id = GAME_21_CUSTOM_ID_STOP,
)

GAME_21_BUTTON_STOP_DISABLED = GAME_21_BUTTON_STOP_ENABLED.copy_with(
    enabled = False,
)

GAME_21_ROW_ENABLED = Row(
    GAME_21_BUTTON_NEW_ENABLED,
    GAME_21_BUTTON_STOP_ENABLED,
)

GAME_21_ROW_DISABLED = Row(
    GAME_21_BUTTON_NEW_DISABLED,
    GAME_21_BUTTON_STOP_DISABLED,
)


GAME_21_EMOJI_ENTER = BUILTIN_EMOJIS['hand_splayed']
GAME_21_EMOJI_START = BUILTIN_EMOJIS['ok_hand']
GAME_21_EMOJI_CANCEL = BUILTIN_EMOJIS['x']

GAME_21_CUSTOM_ID_ENTER = '21.enter'
GAME_21_CUSTOM_ID_START = '21.start'
GAME_21_CUSTOM_ID_CANCEL = '21.cancel'

GAME_21_BUTTON_ENTER_ENABLED = Button(
    emoji = GAME_21_EMOJI_ENTER,
    custom_id = GAME_21_CUSTOM_ID_ENTER,
)

GAME_21_BUTTON_ENTER_DISABLED = GAME_21_BUTTON_ENTER_ENABLED.copy_with(
    enabled = False,
)

GAME_21_BUTTON_START_ENABLED = Button(
    emoji = GAME_21_EMOJI_START,
    custom_id = GAME_21_CUSTOM_ID_START,
)

GAME_21_BUTTON_START_DISABLED = GAME_21_BUTTON_START_ENABLED.copy_with(
    enabled = False,
)

GAME_21_BUTTON_CANCEL_ENABLED = Button(
    emoji = GAME_21_EMOJI_CANCEL,
    custom_id = GAME_21_CUSTOM_ID_CANCEL,
)

GAME_21_BUTTON_CANCEL_DISABLED = GAME_21_BUTTON_CANCEL_ENABLED.copy_with(
    enabled = False,
)

GAME_21_JOIN_ROW_ENABLED = Row(
    GAME_21_BUTTON_ENTER_ENABLED,
    GAME_21_BUTTON_START_ENABLED,
    GAME_21_BUTTON_CANCEL_ENABLED,
)

GAME_21_JOIN_ROW_FULL = Row(
    GAME_21_BUTTON_ENTER_DISABLED,
    GAME_21_BUTTON_START_ENABLED,
    GAME_21_BUTTON_CANCEL_ENABLED,
)

GAME_21_JOIN_ROW_DISABLED = Row(
    GAME_21_BUTTON_ENTER_DISABLED,
    GAME_21_BUTTON_START_DISABLED,
    GAME_21_BUTTON_CANCEL_DISABLED,
)

GAME_21_RESULT_FINISH = 0
GAME_21_RESULT_INITIALIZATION_ERROR = 1
GAME_21_RESULT_IN_GAME_ERROR = 2
GAME_21_RESULT_CANCELLED_TIMEOUT = 3
GAME_21_RESULT_CANCELLED_UNKNOWN = 4
GAME_21_RESULT_CANCELLED_BY_USER = 5

GAME_21_TIMEOUT = 300.0
GAME_21_CANCELLATION_TIMEOUT = 5.0

class Game21PlayerRunner:
    __slots__ = ('player', 'message', 'waiter', 'channel', 'client', 'amount', '_timeouter', 'canceller', '_gui_state',
        'render_after', 'event',)
    
    async def __new__(cls, client, base, user, channel, amount, render_after, event = None):
        player = base.create_user_player(user)
        
        waiter = Future(KOKORO)
        if player.total >= 21:
            if render_after:
                embed = player.create_after_embed(amount)
                try:
                    if event is None:
                        message = await client.message_create(
                            channel,
                            embed = embed,
                            components = GAME_21_ROW_DISABLED,
                        )
                    else:
                        if not event.is_acknowledged():
                            await client.interaction_application_command_acknowledge(event)
                        
                        message = await client.interaction_followup_message_create(
                            event,
                            embed = embed,
                            components = GAME_21_ROW_DISABLED,
                        )
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{cls.__name__}.__new__', err)
                    
                    message = None
            else:
                message = None
            
            waiter.set_result(GAME_21_RESULT_FINISH)
        else:
            embed = player.create_gamble_embed(amount)
            
            try:
                if event is None:
                    message = await client.message_create(
                        channel,
                        embed = embed,
                        components = GAME_21_ROW_ENABLED,
                    )
                else:
                    if not event.is_acknowledged():
                        await client.interaction_application_command_acknowledge(event)
                    
                    message = await client.interaction_followup_message_create(
                        event,
                        embed = embed,
                        components = GAME_21_ROW_ENABLED,
                    )
            except GeneratorExit:
                raise
            
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, f'{cls.__name__}.__new__', err)
                
                waiter.set_result_if_pending(GAME_21_RESULT_INITIALIZATION_ERROR)
                message = None
        
        self = object.__new__(cls)
        self.player = player
        self.waiter = waiter
        self.message = message
        self.channel = channel
        self.amount = amount
        self.client = client
        self.render_after = render_after
        self.event = event
        
        if message is None:
            self._timeouter = None
            self.canceller = None
            self._gui_state = GUI_STATE_SWITCHING_CONTEXT
        else:
            self._timeouter = Timeouter(self, timeout = GAME_21_TIMEOUT)
            self.canceller = cls._canceller
            self._gui_state = GUI_STATE_READY
            
            client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, interaction_event):
        client = self.client
        if (interaction_event.user is not self.player.user):
            await client.interaction_component_acknowledge(interaction_event)
            return
        
        self.event = interaction_event
        
        if self._gui_state != GUI_STATE_READY:
            await client.interaction_component_acknowledge(interaction_event)
            return
        
        custom_id = interaction_event.interaction.custom_id
        
        if (custom_id == GAME_21_CUSTOM_ID_NEW):
            game_ended = self.player.pull_card()
            
        elif (custom_id == GAME_21_CUSTOM_ID_STOP):
            game_ended = True
        
        else:
            # should not happen
            return
        
        if game_ended:
            self._gui_state = GUI_STATE_SWITCHING_CONTEXT
            self.waiter.set_result_if_pending(GAME_21_RESULT_FINISH)
            
            self.cancel()
            if self.render_after:
                await self._canceller_render_after()
            return
        
        self._gui_state = GUI_STATE_EDITING
        
        embed = self.player.create_gamble_embed(self.amount)
        
        try:
            await client.interaction_component_message_edit(
                interaction_event,
                embed = embed,
            )
        except GeneratorExit as err:
            self._gui_state = GUI_STATE_CANCELLING
            self.cancel(err)
            self.waiter.set_result_if_pending(GAME_21_RESULT_IN_GAME_ERROR)
            raise
        
        except BaseException as err:
            self._gui_state = GUI_STATE_CANCELLED
            self.cancel()
            
            if should_render_exception(err):
                await client.events.error(client, f'{self.__class__.__name__}.__new__', err)
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_IN_GAME_ERROR)
        else:
            self._gui_state = GUI_STATE_READY
    
    
    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.slasher.remove_component_interaction_waiter(message, self)
        
        if self._gui_state == GUI_STATE_SWITCHING_CONTEXT:
            # the message is not our, we should not do anything with it.
            return
        
        self._gui_state = GUI_STATE_CANCELLED
        
        if exception is None:
            if self.render_after:
                await self._canceller_render_after()
            return
        
        if isinstance(exception, TimeoutError):
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_TIMEOUT)
            if self.render_after:
                await self._canceller_render_after()
            else:
                interaction_event = self.event
                if interaction_event is None:
                    coroutine = client.message_edit(
                        self.message,
                        components = GAME_21_ROW_DISABLED,
                    )
                
                else:
                    if interaction_event.type is InteractionType.application_command:
                        coroutine = client.interaction_response_message_edit(
                            interaction_event,
                            components = GAME_21_ROW_DISABLED,
                        )
                    elif interaction_event.type is InteractionType.message_component:
                        if interaction_event.is_unanswered():
                            coroutine = client.interaction_component_message_edit(
                                interaction_event,
                                components = GAME_21_ROW_DISABLED,
                            )
                        else:
                            coroutine = client.interaction_response_message_edit(
                                interaction_event,
                                components = GAME_21_ROW_DISABLED,
                            )
                    
                    else:
                        return
                
                try:
                    await coroutine
                except GeneratorExit:
                    raise
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{self.__class__.__name__}._canceller', err)
            return
        
        self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_UNKNOWN)
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        # We do nothing.
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            self._timeouter = None
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)
    
    
    async def _canceller_render_after(self):
        # Do not edit twice
        self.render_after = False
        
        client = self.client
        embed = self.player.create_after_embed(self.amount)
        
        interaction_event = self.event
        
        if interaction_event is None:
            coroutine = client.message_edit(
                self.message,
                embed = embed,
                components = GAME_21_ROW_DISABLED,
            )
        
        else:
            if interaction_event.type is InteractionType.application_command:
                coroutine = client.interaction_response_message_edit(
                    interaction_event,
                    embed = embed,
                    components = GAME_21_ROW_DISABLED,
                )
            elif interaction_event.type is InteractionType.message_component:
                if interaction_event.is_unanswered():
                    coroutine = client.interaction_component_message_edit(
                        interaction_event,
                        embed = embed,
                        components = GAME_21_ROW_DISABLED,
                    )
                else:
                    coroutine = client.interaction_response_message_edit(
                        interaction_event,
                        embed = embed,
                        components = GAME_21_ROW_DISABLED,
                    )
            
            else:
                return
        
        try:
            await coroutine
        except GeneratorExit:
            raise
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, f'{self.__class__.__name__}._canceller_render_after', err)


def game_21_precheck(client, user, channel, amount, require_guild):
    if user.id in IN_GAME_IDS:
        error_message = 'You are already at a game.'
    elif amount < BET_MIN:
        error_message = f'You must bet at least {BET_MIN} {EMOJI__HEART_CURRENCY.as_emoji}'
    elif require_guild and (not channel.guild_id):
        error_message = 'Guild only command.'
    else:
        return
    
    return Embed('Ohoho', error_message, color = COLOR__GAMBLING)


async def game_21_postcheck(client, user, channel, amount):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == user.id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, total_allocated = results[0]
        else:
            total_love = 0
            total_allocated = 0
            entry_id = -1
        
        if total_love - total_allocated < amount:
            error_message = f'You have just {total_love} {EMOJI__HEART_CURRENCY.as_emoji}'
        else:
            return entry_id, None
    
    return entry_id, Embed('Ohoho', error_message, color = COLOR__GAMBLING)


async def game_21_single_player(client, event, amount):
    user = event.user
    channel = event.channel
    
    IN_GAME_IDS.add(event.user.id)
    try:
        entry_id, embed = await game_21_postcheck(client, event.user, event.channel, amount)
        if (embed is not None):
            try:
                await client.interaction_followup_message_create(event, embed = embed)
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
            return
        
        base = Game21Base(channel.guild)
        
        player_client = base.create_bot_player(client)
        
        player_runner = await Game21PlayerRunner(client, base, user, channel, amount, False, event = event)
        player_user_waiter = player_runner.waiter
        if player_user_waiter.is_done() or (entry_id == -1):
            unallocate = False
        else:
            unallocate = True
            async with DB_ENGINE.connect() as connector:
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = user_common_model.total_allocated + amount,
                    )
                )
        
        game_state = await player_user_waiter
        
        if game_state == GAME_21_RESULT_FINISH:
            client_total = player_client.total
            user_total = player_runner.player.total
            if client_total > 21:
                if user_total > 21:
                    winner = None
                else:
                    winner = user
            else:
                if user_total > 21:
                    winner = client
                else:
                    if client_total > user_total:
                        winner = client
                    elif client_total < user_total:
                        winner = user
                    else:
                        winner = None
            
            if winner is client:
                bonus = -amount
            elif winner is None:
                bonus = 0
            else:
                bonus = amount
            
            async with DB_ENGINE.connect() as connector:
                expression = USER_COMMON_TABLE.update(user_common_model.user_id == user.id)
                
                if amount:
                    expression = expression.values(total_love = user_common_model.total_love + bonus)
                
                if unallocate:
                    expression = expression.values(total_allocated = user_common_model.total_allocated - amount)
                
                await connector.execute(expression)
            
            if winner is None:
                title = f'How to draw.'
            elif winner is client:
                title = f'How to lose {amount} {EMOJI__HEART_CURRENCY.as_emoji}'
            else:
                title = f'How to win {amount} {EMOJI__HEART_CURRENCY.as_emoji}'
            
            embed = Embed(title, color = COLOR__GAMBLING)
            player_runner.player.add_done_embed_field(embed)
            player_client.add_done_embed_field(embed)
            
            interaction_event = player_runner.event
            if (interaction_event is None):
                if player_runner.message is None:
                    coroutine = client.message_create(
                        channel,
                        embed = embed,
                    )
                else:
                    coroutine = client.message_edit(
                        channel,
                        embed = embed,
                        components = GAME_21_ROW_DISABLED,
                    )
            else:
                if interaction_event.type is InteractionType.application_command:
                    coroutine = client.interaction_response_message_edit(
                        interaction_event,
                        embed = embed,
                        components = GAME_21_ROW_DISABLED,
                    )
                elif interaction_event.type is InteractionType.message_component:
                    if interaction_event.is_unanswered():
                        coroutine = client.interaction_component_message_edit(
                            interaction_event,
                            embed = embed,
                            components = GAME_21_ROW_DISABLED,
                        )
                    else:
                        coroutine = client.interaction_response_message_edit(
                            interaction_event,
                            embed = embed,
                            components = GAME_21_ROW_DISABLED,
                        )
                else:
                    return
            
            try:
                await coroutine
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
            
            return
        
        if game_state == GAME_21_RESULT_CANCELLED_TIMEOUT:
            if entry_id != -1:
                async with DB_ENGINE.connect() as connector:
                    expression = USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id
                    ).values(
                        total_love = user_common_model.total_love - amount
                    )
                    
                    if unallocate:
                        expression = expression.values(
                            total_allocated = user_common_model.total_allocated - amount
                        )
                    
                    await connector.execute(expression)
            
            embed = Embed(f'Timeout occurred, you lost your {amount} {EMOJI__HEART_CURRENCY.as_emoji} forever.')
            
            if player_runner.message is None:
                coroutine = client.interaction_followup_message_create(event, embed = embed)
            else:
                coroutine = client.message_edit(player_runner.message, embed = embed)
            
            try:
                await coroutine
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
                return
            
            return
        
        # Error occurred
        if unallocate:
            async with DB_ENGINE.connect() as connector:
                expression = USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id
                ).values(
                    total_allocated = user_common_model.total_allocated - amount,
                )
                
                await connector.execute(expression)
    
    finally:
        IN_GAME_IDS.discard(user.id)


def create_join_embed(users, amount):
    description_parts = [
        'Bet amount: ', str(amount), ' ', EMOJI__HEART_CURRENCY.as_emoji, '\n'
        'Creator: ', users[0].full_name, '\n',
    ]
    
    if len(users) > 1:
        description_parts.append('\nJoined users:\n')
        for user in users[1:]:
            description_parts.append(user.full_name)
            description_parts.append('\n')
    
    description_parts.append('\nClick on ')
    description_parts.append(GAME_21_EMOJI_ENTER.as_emoji)
    description_parts.append(' to join.')
    
    description = ''.join(description_parts)
    
    return Embed('Game 21 multi-player', description, color = COLOR__GAMBLING)


async def game_21_mp_user_joiner(
    client, user, guild, source_channel, amount, joined_user_ids, private_channel, entry_id
):
    try:
        private_channel = await client.channel_private_create(user)
    except GeneratorExit:
        raise
    except BaseException as err:
        if not isinstance(err, ConnectionError):
            await client.events.error(client, 'game_21_mp_user_joiner', err)
        
        return
    
    if user.id in IN_GAME_IDS:
        embed = Embed('Ohoho', 'You are already at a game.', color = COLOR__GAMBLING)
        try:
            await client.message_create(private_channel, embed = embed)
        except GeneratorExit:
            raise
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, 'game_21_mp_user_joiner', err)
        
        return
    
    result = False
    IN_GAME_IDS.add(user.id)
    joined_user_ids.add(user.id)
    
    entry_id = -1
    
    try:
        entry_id, embed = await game_21_postcheck(client, user, private_channel, amount)
        if (embed is None):
            embed = Embed(
                '21 multi-player game joined.',
                (
                    f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
                    f'Guild: {guild.name}\n'
                    f'Channel: {source_channel.mention}'
                ),
                color = COLOR__GAMBLING,
            )
            
            try:
                await client.message_create(private_channel, embed)
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_mp_user_joiner', err)
                
            else:
                result = True
    finally:
        if result:
            if (entry_id != -1):
                async with DB_ENGINE.connect() as connector:
                    await connector.execute(
                        USER_COMMON_TABLE.update(
                            user_common_model.id == entry_id,
                        ).values(
                            total_allocated = user_common_model.total_allocated + amount,
                        )
                    )
            
            joined_tuple = (user, private_channel, entry_id)
        
        else:
            IN_GAME_IDS.discard(user.id)
            joined_user_ids.discard(user.id)
            joined_tuple = None
    
    return joined_tuple



async def game_21_refund(entry_id, amount):
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_allocated = user_common_model.total_allocated - amount,
            )
        )

async def game_21_mp_user_leaver(client, user, guild, source_channel, amount, joined_user_ids, private_channel,
        entry_id):
    IN_GAME_IDS.discard(user.id)
    joined_user_ids.discard(user.id)
    
    await game_21_refund(entry_id, amount)
    
    embed = Embed('21 multi-player game left.',
        f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
        f'Guild: {guild.name}\n'
        f'Channel: {source_channel.mention}',
            color = COLOR__GAMBLING)
    
    try:
        await client.message_create(private_channel, embed = embed)
    except GeneratorExit:
        raise
    except BaseException as err:
        if should_render_exception(err):
            await client.events.error(client, 'game_21_mp_user_leaver', err)


async def game_21_mp_cancelled(client, user, guild, source_channel, amount, private_channel, joined_user_ids, entry_id):
    IN_GAME_IDS.discard(user.id)
    joined_user_ids.discard(user.id)
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_allocated = user_common_model.total_allocated - amount,
            )
        )
    
    embed = Embed('21 multi-player game was cancelled.',
        (
            f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
            f'Guild: {guild.name}\n'
            f'Channel: {source_channel.mention}'
        ),
        color = COLOR__GAMBLING,
    )
    
    try:
        await client.message_create(private_channel, embed)
    except GeneratorExit:
        raise
    except BaseException as err:
        if should_render_exception(err):
            await client.events.error(client, 'game_21_mp_cancelled', err)


def game_21_mp_notify_cancellation(client, joined_tuples, amount, channel, guild, joined_user_ids):
    Task(game_21_refund(joined_tuples[0][2], amount), KOKORO)
    for notify_user, private_channel, entry_id in joined_tuples[1:]:
        Task(game_21_mp_cancelled(client, notify_user, guild, channel, amount, private_channel,
            joined_user_ids, entry_id), KOKORO)

GAME_21_MP_MAX_USERS = 10
GAME_21_MP_FOOTER = f'Max {GAME_21_MP_MAX_USERS} users allowed.'

class Game21JoinGUI:
    __slots__ = ('client', 'channel', 'message', 'waiter', 'amount', 'joined_tuples', '_timeouter', '_gui_state',
        'canceller', 'user_locks', 'joined_user_ids', 'workers', 'guild', 'message_sync_last_state',
        'message_sync_in_progress', 'message_sync_handle', 'event')
    
    async def __new__(cls, client, channel, joined_user_tuple, amount, joined_user_ids, guild, event):
        waiter = Future(KOKORO)
        
        embed = create_join_embed([joined_user_tuple[0]], amount)
        embed.add_footer(GAME_21_MP_FOOTER)
        
        try:
            if not event.is_acknowledged():
                await client.interaction_application_command_acknowledge(event)
            
            message = await client.interaction_followup_message_create(
                event,
                embed = embed,
                components = GAME_21_JOIN_ROW_ENABLED,
            )
        
        except GeneratorExit:
            waiter.set_result_if_pending(GAME_21_RESULT_INITIALIZATION_ERROR)
            raise
        
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, f'{cls.__name__}.__new__', err)
            
            waiter.set_result_if_pending(GAME_21_RESULT_INITIALIZATION_ERROR)
            message = None
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.message = message
        self.waiter = waiter
        self.amount = amount
        self.joined_tuples = [joined_user_tuple]
        self.user_locks = set()
        self.joined_user_ids = joined_user_ids
        self.workers = set()
        self.guild = guild
        self.message_sync_last_state = self.joined_tuples.copy()
        self.message_sync_in_progress = False
        self.message_sync_handle = None
        self.event = event
        
        if message is None:
            self._timeouter = None
            self.canceller = None
            self._gui_state = GUI_STATE_SWITCHING_CONTEXT
        else:
            self._timeouter = Timeouter(self, timeout = GAME_21_TIMEOUT)
            self.canceller = cls._canceller
            self._gui_state = GUI_STATE_READY
            
            client.slasher.add_component_interaction_waiter(message, self)
        
        return self
    
    
    async def __call__(self, interaction_event):
        custom_id = interaction_event.interaction.custom_id
        
        client = self.client
        self.event = interaction_event
        
        if custom_id == GAME_21_CUSTOM_ID_ENTER:
            user = interaction_event.user
            
            if user.id in self.user_locks:
                # already doing something.
                await client.interaction_component_acknowledge(interaction_event)
                return
            
            joined_tuples = self.joined_tuples
            if user is joined_tuples[0][0]:
                # Source user cannot join / leave
                await client.interaction_component_acknowledge(interaction_event)
                return
            
            for maybe_user, private_channel, entry_id in joined_tuples[1:]:
                if maybe_user is user:
                    join = False
                    break
            else:
                private_channel = None
                join = True
                entry_id = -1
            
            if join and (len(joined_tuples) == GAME_21_MP_MAX_USERS):
                await client.interaction_component_acknowledge(interaction_event)
                return
            
            self.user_locks.add(user.id)
            try:
                if join:
                    coroutine_function = game_21_mp_user_joiner
                else:
                    coroutine_function = game_21_mp_user_leaver
                
                task = Task(coroutine_function(client, user, self.guild, self.channel, self.amount,
                    self.joined_user_ids, private_channel, entry_id), KOKORO)
                
                Task(self.do_acknowledge(interaction_event), KOKORO)
                
                self.workers.add(task)
                try:
                    result = await task
                    if join:
                        if (result is not None):
                            self.joined_tuples.append(result)
                    else:
                        for index in range(1, len(joined_tuples)):
                            maybe_user = joined_tuples[index][0]
                            if maybe_user is user:
                                del joined_tuples[index]
                                break
                finally:
                    self.workers.discard(task)
            
            finally:
                self.user_locks.discard(user.id)
            
            self.maybe_message_sync(interaction_event)
            return
        
        if custom_id == GAME_21_CUSTOM_ID_START:
            if (interaction_event.user is not self.joined_tuples[0][0]):
                await client.interaction_component_acknowledge(interaction_event)
                return
            
            self._gui_state = GUI_STATE_SWITCHING_CONTEXT
            
            # Wait for all worker to finish
            await self._wait_for_cancellation()
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_FINISH)
            self.cancel()
            return
        
        if custom_id == GAME_21_CUSTOM_ID_CANCEL:
            if (interaction_event.user is not self.joined_tuples[0][0]):
                await client.interaction_component_acknowledge(interaction_event)
                return
            
            self._gui_state = GUI_STATE_CANCELLING
            
            # Wait for all workers to finish
            await self._wait_for_cancellation()
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_BY_USER)
            self.cancel()
            return
    
    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.slasher.remove_component_interaction_waiter(message, self)
        
        message_sync_handle = self.message_sync_handle
        if (message_sync_handle is not None):
            self.message_sync_handle = None
            message_sync_handle.cancel()
        
        if self._gui_state == GUI_STATE_SWITCHING_CONTEXT:
            # the message is not our, we should not do anything with it.
            return
        
        self._gui_state = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        await self._wait_for_cancellation()
        game_21_mp_notify_cancellation(client, self.joined_tuples, self.amount, self.channel, self.guild,
            self.joined_user_ids)
        
        if isinstance(exception, TimeoutError):
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_TIMEOUT)
            
            interaction_event = self.event
            if interaction_event is None:
                coroutine = client.message_edit(
                    self.message,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
            
            else:
                if interaction_event.type is InteractionType.application_command:
                    coroutine = client.interaction_response_message_edit(
                        interaction_event,
                        components = GAME_21_JOIN_ROW_DISABLED,
                    )
                elif interaction_event.type is InteractionType.message_component:
                    if interaction_event.is_unanswered():
                        coroutine = client.interaction_component_message_edit(
                            interaction_event,
                            components = GAME_21_JOIN_ROW_DISABLED,
                        )
                    else:
                        coroutine = client.interaction_response_message_edit(
                            interaction_event,
                            components = GAME_21_JOIN_ROW_DISABLED,
                        )
                
                else:
                    return
            
            try:
                await coroutine
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, f'{self.__class__.__name__}._canceller', err)
        
        
        self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_UNKNOWN)
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
    
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)
    
    
    async def _wait_for_cancellation(self):
        workers = self.workers
        if workers:
            future = WaitTillAll(workers, KOKORO)
            future_or_timeout(future, GAME_21_CANCELLATION_TIMEOUT)
            done, pending = await future
            for future in chain(done, pending):
                future.cancel()
    
    def maybe_message_sync(self, interaction_event):
        if self.message_sync_in_progress:
            if interaction_event.is_unanswered():
                Task(self.do_acknowledge(interaction_event), KOKORO)
        
        else:
            self.message_sync_in_progress = True
            Task(self.do_message_sync(), KOKORO)
    
    async def do_acknowledge(self, interaction_event):
        client = self.client
        try:
            await client.interaction_component_acknowledge(interaction_event)
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, f'{self.__class__.__name__}.do_acknowledge', err)
    
    async def do_message_sync(self):
        while True:
            if (self._gui_state != GUI_STATE_READY) or (self.joined_tuples == self.message_sync_last_state):
                self.message_sync_in_progress = False
                return
            
            self.message_sync_last_state = self.joined_tuples.copy()
            
            embed = create_join_embed([item[0] for item in self.joined_tuples], self.amount)
            embed.add_footer(GAME_21_MP_FOOTER)
            
            if len(self.joined_tuples) >= GAME_21_MP_MAX_USERS:
                components = GAME_21_JOIN_ROW_FULL
            else:
                components = GAME_21_JOIN_ROW_ENABLED
                
            client = self.client
            interaction_event = self.event
            if interaction_event is None:
                coroutine = client.message_edit(
                    self.message,
                    embed = embed,
                    components = components,
                )
            else:
                if interaction_event.type is InteractionType.application_command:
                    coroutine = client.interaction_response_message_edit(
                        interaction_event,
                        embed = embed,
                        components = components,
                    )
                elif interaction_event.type is InteractionType.message_component:
                    if interaction_event.is_unanswered():
                        coroutine = client.interaction_component_message_edit(
                            interaction_event,
                            embed = embed,
                            components = components,
                        )
                    else:
                        coroutine = client.interaction_response_message_edit(
                            interaction_event,
                            embed = embed,
                            components = components,
                        )
                else:
                    return
            
            task = Task(coroutine, KOKORO)
            self.workers.add(task)
            try:
                try:
                    await task
                except GeneratorExit:
                    raise
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{self.__class__.__name__}.do_message_sync', err)
            finally:
                self.workers.discard(task)


async def game_21_multi_player(client, event, amount):
    user = event.user
    channel = event.channel
    
    guild = channel.guild
    
    IN_GAME_IDS.add(user.id)
    joined_user_ids = set()
    joined_user_ids.add(user.id)
    try:
        entry_id, embed = await game_21_postcheck(client, user, channel, amount)
        if (embed is not None):
            return embed
        
        try:
            private_channel = await client.channel_private_create(user)
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if not isinstance(err, ConnectionError):
                await client.events.error(client, 'game_21_multi_player', err)
            
            return
        
        embed = Embed(
            '21 multi-player game created.',
            (
                f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
                f'Guild: {guild.name}\n'
                f'Channel: {channel.mention}'
            ),
            color = COLOR__GAMBLING
        )
        
        try:
            await client.message_create(private_channel, embed)
        except GeneratorExit:
            raise
        
        except ConnectionError:
            return
        
        except BaseException as err:
            if (not isinstance(err, DiscordException)) or (err.code != ERROR_CODES.cannot_message_user):
                await client.events.error(client, 'game_21_multi_player', err)
                return
            
            private_open = False
        else:
            private_open = True
        
        if (not private_open):
            embed = Embed('Error', 'I cannot send private message to you.', color = COLOR__GAMBLING)
            
            try:
                await client.interaction_response_message_edit(event, embed = embed)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        join_gui = await Game21JoinGUI(client, channel, (user, private_channel, entry_id), amount, joined_user_ids,
            guild, event)
        
        game_state = await join_gui.waiter
        message = join_gui.message
        event = join_gui.event
        
        if game_state == GAME_21_RESULT_CANCELLED_TIMEOUT:
            embed = Embed('Timeout', 'Timeout occurred, the hearts were refund', color = COLOR__GAMBLING)
            
            try:
                await client.interaction_response_message_edit(event, embed = embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        if not (game_state == GAME_21_RESULT_FINISH or game_state == GAME_21_RESULT_CANCELLED_BY_USER):
            return
        
        
        if game_state == GAME_21_RESULT_CANCELLED_BY_USER:
            game_21_mp_notify_cancellation(client, join_gui.joined_tuples, amount, channel, guild, joined_user_ids)
            
            embed = Embed(
                'Cancelled',
                'The game has been cancelled, the hearts are refund.',
                color = COLOR__GAMBLING,
            )
            
            if event.type is InteractionType.application_command:
                coroutine = client.interaction_response_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
            elif event.type is InteractionType.message_component:
                if event.is_unanswered():
                    coroutine = client.interaction_component_message_edit(
                        event,
                        embed = embed,
                        components = GAME_21_JOIN_ROW_DISABLED,
                    )
                else:
                    coroutine = client.interaction_response_message_edit(
                        event,
                        embed = embed,
                        components = GAME_21_JOIN_ROW_DISABLED,
                    )
            
            else:
                return
            
            try:
                await coroutine
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        joined_tuples = join_gui.joined_tuples
        if len(joined_tuples) == 1:
            await game_21_refund(joined_tuples[0][2], amount)
            
            embed = Embed(
                'RIP',
                'Starting the game alone, is just sad.',
                color = COLOR__GAMBLING,
            )
            
            if event.type is InteractionType.application_command:
                coroutine = client.interaction_response_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
            elif event.type is InteractionType.message_component:
                if event.is_unanswered():
                    coroutine = client.interaction_component_message_edit(
                        event,
                        embed = embed,
                        components = GAME_21_JOIN_ROW_DISABLED,
                    )
                else:
                    coroutine = client.interaction_response_message_edit(
                        event,
                        embed = embed,
                        components = GAME_21_JOIN_ROW_DISABLED,
                    )
            else:
                return
            
            try:
                await coroutine
            except GeneratorExit:
                raise
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        total_bet_amount = len(joined_tuples) * amount
        # Update message
        description_parts = [
            'Total bet amount: ',
            str(total_bet_amount),
            EMOJI__HEART_CURRENCY.as_emoji,
            '\n\nPlayers:\n',
        ]
        
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            description_parts.append(tuple_user.full_name)
            description_parts.append('\n')
        
        del description_parts[-1]
        
        description = ''.join(description_parts)
        embed = Embed(
            'Game 21 in progress',
            description,
            color = COLOR__GAMBLING
        )
        
        if event.type is InteractionType.application_command:
            coroutine = client.interaction_response_message_edit(
                event,
                embed = embed,
                components = GAME_21_JOIN_ROW_DISABLED,
            )
        elif event.type is InteractionType.message_component:
            if event.is_unanswered():
                coroutine = client.interaction_component_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
            else:
                coroutine = client.interaction_response_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
        else:
            return
    
        try:
            await coroutine
        except GeneratorExit:
            raise
        except BaseException as err:
            game_21_mp_notify_cancellation(client, joined_tuples, amount, channel, guild, joined_user_ids)
            if should_render_exception(err):
                await client.events.error(client, 'game_21_multi_player', err)
            return
        
        # Start game
        base = Game21Base(guild)
        tasks = []
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            task = Task(Game21PlayerRunner(client, base, tuple_user, tuple_channel, amount, True), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillAll(tasks, KOKORO)
        
        waiters_to_runners = {}
        
        for task in done:
            runner = await task
            waiter = runner.waiter
            waiters_to_runners[waiter] = runner
        
        done, pending = await WaitTillAll(waiters_to_runners, KOKORO)
        
        max_point = 0
        losers = []
        winners = []
        for waiter in done:
            game_state = waiter.result()
            runner = waiters_to_runners[waiter]
            if game_state != GAME_21_RESULT_FINISH:
                losers.append(user)
                continue
            
            user_total = runner.player.total
            user = runner.player.user
            if user_total > 21:
                losers.append(user)
                continue
            
            if user_total > max_point:
                losers.extend(winners)
                winners.clear()
                winners.append(user)
                max_point = user_total
                continue
            
            if user_total == max_point:
                winners.append(user)
                continue
            
            losers.append(user)
            continue
        
        user_entry_map = {}
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            user_entry_map[tuple_user] = entry_id
        
        loser_entry_ids = None
        if losers:
            for user in losers:
                entry_id = user_entry_map[user]
                if entry_id == -1:
                    continue
                
                if loser_entry_ids is None:
                    loser_entry_ids = []
                loser_entry_ids.append(entry_id)
        
        winner_entry_ids = None
        if winners:
            for user in winners:
                entry_id = user_entry_map[user]
                if entry_id == -1:
                    continue
                
                if winner_entry_ids is None:
                    winner_entry_ids = []
                winner_entry_ids.append(entry_id)
        
        async with DB_ENGINE.connect() as connector:
            if (loser_entry_ids is not None):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id.in_(loser_entry_ids),
                    ).values(
                        total_allocated = user_common_model.total_allocated - amount,
                        total_love = user_common_model.total_love - amount,
                    )
                )
                
                if (winner_entry_ids is not None):
                    won_per_user = int(len(losers) * amount // len(winners))
                    
                    await connector.execute(
                        USER_COMMON_TABLE.update(
                            user_common_model.id.in_(winner_entry_ids),
                        ).values(
                            total_allocated = user_common_model.total_allocated - amount,
                            total_love = user_common_model.total_love + won_per_user,
                        )
                    )
                
            else:
                if (winner_entry_ids is not None):
                    await connector.execute(
                        USER_COMMON_TABLE.update(
                            user_common_model.id.in_(winner_entry_ids),
                        ).values(
                            total_allocated = user_common_model.total_allocated - amount,
                        )
                    )
        
        description_parts = [
            'Total bet amount: ',
            str(total_bet_amount),
            EMOJI__HEART_CURRENCY.as_emoji,
            '\n\n',
        ]
        
        if winners:
            description_parts.append('Winners:\n')
            for user in winners:
                description_parts.append(user.full_name)
                description_parts.append('\n')
            
            description_parts.append('\n')
        
        if losers:
            description_parts.append('Losers:\n')
            for user in losers:
                description_parts.append(user.full_name)
                description_parts.append('\n')
        
        if description_parts[-1] == '\n':
            del description_parts[-1]
        
        description = ''.join(description_parts)
        
        embed = Embed('Game ended', description, color = COLOR__GAMBLING)
        for runner in waiters_to_runners.values():
            runner.player.add_done_embed_field(embed)
        

        if event.type is InteractionType.application_command:
            coroutine = client.interaction_response_message_edit(
                event,
                embed = embed,
                components = GAME_21_JOIN_ROW_DISABLED,
            )
        elif event.type is InteractionType.message_component:
            if event.is_unanswered():
                coroutine = client.interaction_component_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
            else:
                coroutine = client.interaction_response_message_edit(
                    event,
                    embed = embed,
                    components = GAME_21_JOIN_ROW_DISABLED,
                )
        else:
            return
        
        try:
            await coroutine
        except GeneratorExit:
            raise
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, 'game_21_multi_player', err)
        
        return
    
    finally:
        for user_id in joined_user_ids:
            IN_GAME_IDS.discard(user_id)
