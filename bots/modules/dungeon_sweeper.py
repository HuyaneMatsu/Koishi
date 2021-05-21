# -*- coding: utf-8 -*-
import re, os

from hata import Emoji, Embed, Color, DiscordException, BUILTIN_EMOJIS, Task, WaitTillAll, ERROR_CODES, Client, \
    KOKORO, LOOP_TIME

from hata.ext.command_utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, \
    GUI_STATE_SWITCHING_CTX, GUI_STATE_CANCELLED
from hata.ext.commands_v2 import checks

from hata.discord.core import GC_CYCLER
from hata.ext.slash import SlashResponse, abort

from bot_utils.models import DB_ENGINE, DS_TABLE, ds_model
from bot_utils.shared import PATH__KOISHI

DS_COLOR = Color(0xa000c4)

DS_GAMES = {}
STAGES = []
CHARS = []
COLORS = (0xa000c4, 0x00cc03, 0xffe502, 0xe50016)

#:-> @ <-:#}{#:-> @ <-:#{ GC }#:-> @ <-:#}{#:-> @ <-:#

async def _keep_await(function,games):
    for game in games:
        await function(game)

def GC_games(cycler):
    limit = LOOP_TIME()-3600. #we delete after 1 hour
    to_delete = []
    to_save = []
    for game in DS_GAMES.values():
        if game.last < limit:
            to_delete.append(game)
        else:
            to_save.append(game)
    
    if to_delete:
        KOKORO.call_soon_thread_safe(Task, _keep_await(ds_game.cancel, to_delete), KOKORO)
    
    if to_save:
        KOKORO.call_soon_thread_safe(Task, _keep_await(ds_game.save_position, to_save), KOKORO)


GC_CYCLER.append(GC_games)

del GC_CYCLER
del GC_games

#:-> @ <-:#}{#:-> @ <-:#{ command }#:-> @ <-:#}{#:-> @ <-:#

SLASH_CLIENT : Client

DUNGEON_SWEEPER = SLASH_CLIENT.interactions(None,
    name='ds',
    description='Touhou themed puzzle game.',
    is_global=True,
)

@DUNGEON_SWEEPER.interactions
async def rules(client, event):
    """Shows the rules of DS!"""
    if not event.channel.cached_permissions_for(client).can_use_external_emojis:
        abort('I have no permissions at this channel to render this message.')
    
    return RULES_HELP

@DUNGEON_SWEEPER.interactions(is_default=True)
async def play(client, event):
    """Starts the game"""
    permissions = event.channel.cached_permissions_for(client)
    if not (permissions.can_send_messages and permissions.can_add_reactions and permissions.can_use_external_emojis \
            and permissions.can_manage_messages):
        abort('I have not all permissions to start a game at this channel.')
        return
    
    game = DS_GAMES.get(event.user.id, None)
    if game is None:
        yield ds_game(client, event)
    else:
        yield game.renew(event)

#:-> @ <-:#}{#:-> @ <-:#{ backend }#:-> @ <-:#}{#:-> @ <-:#

class ds_game:

    WEST   = BUILTIN_EMOJIS['arrow_left']
    NORTH  = BUILTIN_EMOJIS['arrow_up']
    SOUTH  = BUILTIN_EMOJIS['arrow_down']
    EAST   = BUILTIN_EMOJIS['arrow_right']
    
    emojis_game_p1 = (WEST, NORTH, SOUTH, EAST)
    
    BACK   = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
    RESET  = BUILTIN_EMOJIS['arrows_counterclockwise']
    CANCEL = BUILTIN_EMOJIS['x']
    
    emojis_game_p2 = (BACK, RESET, CANCEL)

    UP     = BUILTIN_EMOJIS['arrow_up_small']
    DOWN   = BUILTIN_EMOJIS['arrow_down_small']
    UP2    = BUILTIN_EMOJIS['arrow_double_up']
    DOWN2  = BUILTIN_EMOJIS['arrow_double_down']
    LEFT   = BUILTIN_EMOJIS['arrow_backward']
    RIGHT  = BUILTIN_EMOJIS['arrow_forward']
    SELECT = BUILTIN_EMOJIS['ok']
    
    emojis_menu = (UP, DOWN, UP2, DOWN2, LEFT, RIGHT, SELECT)
    
    __slots__ = ('cache', 'call', 'channel', 'client', 'data', 'last', 'message', 'position', 'position_ori', 'stage',
        '_task_flag', 'user', )
    
    async def __new__(cls, client, event):
        self = object.__new__(cls)
        self.client = client
        self.user = event.user
        self.channel = event.channel
        self.message = None
        self.stage = None
        self._task_flag = GUI_STATE_READY
        self.call = type(self).call_menu
        self.cache = [None for _ in range(len(CHARS))]
        self.last = LOOP_TIME()
        
        DS_GAMES[self.user.id]= self
        
        async with DB_ENGINE.connect() as connector:
            result = await connector.execute(DS_TABLE.select(ds_model.user_id == self.user.id))
            stats = await result.fetchall()
        if stats:
            stats = stats[0]
            self.position = self.position_ori = stats.position
            self.data = bytearray(stats.data)
        else:
            self.position = 0
            self.position_ori =- 1
            self.data = bytearray(800)
        
        try:
            message = yield SlashResponse(embed=self.render_menu(), force_new_message=True)
        except BaseException as err:
            self._task_flag = GUI_STATE_CANCELLED
            del DS_GAMES[self.user.id]
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__new__', err)
            return
        
        self.message = message
        
        tasks = []
        
        for emoji in self.emojis_menu:
            task = Task(client.reaction_add(message, emoji), KOKORO)
            tasks.append(task)
        
        try:
            await WaitTillAll(tasks, KOKORO)
        except BaseException as err:
            for task in tasks:
                task.cancel()
            
            self._task_flag = GUI_STATE_CANCELLED
            del DS_GAMES[self.user.id]
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.unknown_emoji, # no permission to use external emoji
                        ERROR_CODES.max_reactions, # maximal amount of reactions reached
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__new__', err)
            return
        
        client.events.reaction_add.append(message, self)
        return
    
    def __repr___(self):
        result = [
            '<',
            self.__class__.__name__,
            'client=',
            repr(self.client),
            ', user=',
            repr(self.user),
            ', channel=',
            repr(self.channel),
            ', task_flag=',
        ]
        
        task_flag = self._task_flag
        
        result.append(repr(task_flag))
        result.append(' (')
        
        task_flag_name = (
            'GUI_STATE_READY',
            'GUI_STATE_SWITCHING_PAGE',
            'GUI_STATE_CANCELLING',
            'GUI_STATE_CANCELLED',
            'GUI_STATE_SWITCHING_CTX',
        )[task_flag]
        
        result.append(task_flag_name)
        result.append(')')
        
        result.append(', call =')
        result.append(repr(self.call.__name__))
        result.append('>')
        
        return ''.join(result)
        
    async def start_menu(self):
        self.stage = None
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        client = self.client
        message = self.message
        
        tasks = []
        task = Task(client.reaction_clear(message), KOKORO)
        tasks.append(task)
        for emoji in self.emojis_menu:
            task = Task(client.reaction_add(message, emoji), KOKORO)
            tasks.append(task)
        
        task=Task(client.message_edit(message, embed=self.render_menu()), KOKORO)
        tasks.append(task)
        
        try:
            await WaitTillAll(tasks, KOKORO)
        except BaseException as err:
            for task in tasks:
                task.cancel()
            
            self._task_flag = GUI_STATE_CANCELLING
            Task(self.cancel(), KOKORO)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.unknown_emoji, # no permission to use external emoji
                        ERROR_CODES.max_reactions, # maximal amount of reactions reached
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.start_menu', err)
            return
        
        self.last = LOOP_TIME()
        self.call = type(self).call_menu
        self._task_flag = GUI_STATE_READY

    async def start_game(self):
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        i1, rest = divmod(self.position, 33)
        if rest < 3:
            i2 = 0
            i3 = rest
        else:
            i2, i3 = divmod(rest+7, 10)

        self.stage = stage_backend(STAGES[i1][i2][i3], self.value_from_position(self.position))

        client = self.client
        message = self.message
        
        tasks = []
        task = Task(client.reaction_clear(message), KOKORO)
        tasks.append(task)
        
        for emoji in self.emojis_game_p1:
            task=Task(client.reaction_add(message, emoji), KOKORO)
            tasks.append(task)
        
        task = Task(client.reaction_add(message, self.stage.source.emoji), KOKORO)
        tasks.append(task)
        
        for emoji in self.emojis_game_p2:
            task = Task(client.reaction_add(message, emoji), KOKORO)
            tasks.append(task)
        
        task = Task(client.message_edit(message, embed=self.render_game()), KOKORO)
        tasks.append(task)
        
        try:
            await WaitTillAll(tasks, KOKORO)
        except BaseException as err:
            for task in tasks:
                task.cancel()
            
            self._task_flag = GUI_STATE_CANCELLING
            Task(self.cancel(), KOKORO)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.unknown_emoji, # no permission to use external emoji
                        ERROR_CODES.max_reactions, # maximal amount of reactions reached
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.start_game', err)
            return
        
        self.last = LOOP_TIME()
        self.call = type(self).call_game
        
        if self._task_flag != GUI_STATE_SWITCHING_CTX:
            self._task_flag = GUI_STATE_READY

    async def start_done(self):
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        client=self.client
        
        save_task = Task(self.save_done(), KOKORO)
        message = self.message
        
        tasks = []
        task = Task(client.reaction_clear(message), KOKORO)
        tasks.append(task)
        task = Task(client.reaction_add(message, self.RESET), KOKORO)
        tasks.append(task)
        task = Task(client.reaction_add(message, self.CANCEL), KOKORO)
        tasks.append(task)
        task = Task(client.message_edit(message, embed=self.render_done()), KOKORO)
        tasks.append(task)
        
        try:
            await WaitTillAll(tasks, KOKORO)
        except BaseException as err:
            for task in tasks:
                task.cancel()
            
            self._task_flag = GUI_STATE_CANCELLING
            Task(self.cancel(), KOKORO)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.unknown_emoji, # no permission to use external emoji
                        ERROR_CODES.max_reactions, # maximal amount of reactions reached
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.start_done', err)
            return
        
        finally:
            await save_task
            
        self.last = LOOP_TIME()
        self.call = type(self).call_done
        
        if self._task_flag != GUI_STATE_SWITCHING_CTX:
            self._task_flag = GUI_STATE_READY
    
    @staticmethod
    async def default_coro():
        pass
    
    async def __call__(self, client, event):
        if event.user is not self.user:
            return
    
        await self.call(self, event.emoji)

    async def call_menu(self, emoji):
        if (emoji not in self.emojis_menu):
            return
        
        if self._task_flag!=GUI_STATE_READY:
            Task(self.reaction_delete(emoji), KOKORO)
            return
        
        while True:
            if emoji is self.UP:
                position_change = 1
                break
            
            if emoji is self.DOWN:
                position_change = -1
                break
            
            if emoji is self.UP2:
                position_change = 5
                break

            if emoji is self.DOWN2:
                position_change = -5
                break

            position_change=0
            if emoji is self.RIGHT:
                chapter_change = 1
                break

            if emoji is self.LEFT:
                chapter_change = -1
                break

            if emoji is self.SELECT:
                if self.message.embeds[0].fields:
                    await self.start_game()
                else:
                    Task(self.reaction_delete(emoji), KOKORO)
                return
            
            return       
        
        Task(self.reaction_delete(emoji), KOKORO)
        
        position = self.position
        i1, rest = divmod(position, 33)
        if rest < 3:
            i2 = 0
            i3 = rest
        else:
            i2, i3 = divmod(rest+7, 10)
        
        if position_change:
            cache = self.get_cache(i1)
            for actual_position, element in enumerate(cache):
                stage = element[0]
                if stage.difficulty == i2 and stage.level == i3:
                    break
            
            relative_position = actual_position+position_change
            if position_change < 0:
                if relative_position < 0:
                    relative_position = 0
            else:
                if relative_position >= len(cache):
                    relative_position = len(cache)-1
            
            if actual_position == relative_position:
                return
            
            new_position=cache[relative_position][0].position
            
            if new_position == position:
                return
            
        else:
            relative_chapter = i1+chapter_change
            if relative_chapter < 0 or relative_chapter >= len(STAGES):
                return
            
            cache = self.get_cache(relative_chapter)
            for target_position, element in enumerate(cache):
                stage = element[0]
                
                if stage.difficulty == i2:
                    relative_position = target_position
                    if stage.level == i3:
                        break
                elif stage.difficulty>i2:
                    break
            else:
                relative_position = target_position
            
            new_position = cache[relative_position][0].position
        
        self.position = new_position
        
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        client = self.client
        try:
            await client.message_edit(self.message, embed=self.render_menu())
        except BaseException as err:
            
            self._task_flag = GUI_STATE_CANCELLING
            Task(self.cancel(), KOKORO)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message already deleted
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.call_menu', err)
            return
        
        if self._task_flag != GUI_STATE_SWITCHING_CTX:
            self._task_flag = GUI_STATE_READY
    
    async def call_game(self, emoji):
        stage = self.stage
        if stage is None:
            return
        
        if (emoji not in self.emojis_game_p1) and (emoji is not stage.source.emoji) and (emoji not in self.emojis_game_p2):
            return
        
        if self._task_flag!=GUI_STATE_READY:
            Task(self.reaction_delete(emoji), KOKORO)
            return
        
        while True:
            if emoji is self.WEST:
                result = stage.move_west()
                break
            
            if emoji is self.NORTH:
                result = stage.move_north()
                break

            if emoji is self.SOUTH:
                result = stage.move_south()
                break

            if emoji is self.EAST:
                result = stage.move_east()
                break
            
            if emoji is self.stage.source.emoji:
                result = stage.activate_skill()
                break

            if emoji is self.BACK:
                result = stage.back()
                break

            if emoji is self.RESET:
                result = stage.reset()
                break

            if emoji is self.CANCEL:
                await self.start_menu()
                return

            return
        
        client = self.client
        if not result:
            Task(self.reaction_delete(emoji), KOKORO)
            return
        
        if stage.done():
            await self.start_done()
            return
        
        Task(self.reaction_delete(emoji), KOKORO)
        
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        try:
            await self.client.message_edit(self.message, embed=self.render_game())
        except BaseException as err:
            
            self._task_flag = GUI_STATE_CANCELLING
            Task(self.cancel(), KOKORO)
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message already deleted
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.call_game', err)
            return
        
        self.last = LOOP_TIME()
        
        if self._task_flag != GUI_STATE_SWITCHING_CTX:
            self._task_flag = GUI_STATE_READY

    async def call_done(self, emoji):
        if (emoji is not self.RESET) and (emoji is not self.CANCEL):
            return
        
        Task(self.reaction_delete(emoji), KOKORO)
        
        if self._task_flag != GUI_STATE_READY:
            return 
        
        if emoji is self.RESET:
            self.position = self.stage.source.position
            await self.start_game()
        else:
            await self.start_menu()
        
    async def cancel(self):
        if self._task_flag == GUI_STATE_CANCELLING:
            await self.save_position()
            return
        
        self._task_flag = GUI_STATE_CANCELLED
        
        try:
            del DS_GAMES[self.user.id]
        except KeyError:
            return #already cancelled
        
        self.client.events.reaction_add.remove(self.message, self)
        
        await self.save_position()
    
    async def save_position(self):
        position = self.position
        if position == self.position_ori:
            return
        
        async with DB_ENGINE.connect() as connector:
            if self.position_ori<0:
                coro=DS_TABLE.insert(). \
                    values(user_id=self.user.id, position=position, data=self.data)
            else:
                coro=DS_TABLE.update(). \
                    values(position=position, data=self.data). \
                    where(ds_model.user_id==self.user.id)
            
            await connector.execute(coro)
        
        self.position_ori = position
        
    async def save_done(self):
        best_steps = self.stage.best
        position = self.position
        old_steps = self.value_from_position(position)
        
        if position%33 != 32:
            relative_position = position+1
            i1, rest = divmod(relative_position, 33)
            if rest < 3:
                i2 = 0
                i3 = rest
            else:
                i2, i3 = divmod(rest+7, 10)
            
            difficulties = STAGES[i1]
            if difficulties:
                levels = difficulties[i2]
                if i3 < len(levels):
                    self.position=relative_position
        
        if old_steps != best_steps:
            self.write_value(position, best_steps)
            self.cache[self.stage.source.chapter] = None
            return_ = False
        else:
            return_ = True
        
        if return_ and self.position == self.position_ori:
            return
        
        async with DB_ENGINE.connect() as connector:
            if self.position_ori < 0:
                coro=DS_TABLE.insert(). \
                    values(user_id=self.user.id, position=self.position, data=self.data)
            else:
                coro=DS_TABLE.update(). \
                    values(position=self.position, data=self.data). \
                    where(ds_model.user_id==self.user.id)
            
            await connector.execute(coro)
    
        self.position_ori = self.position
      
    async def renew(self, channel):
        if self._task_flag in (GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CTX):
            return
        
        self._task_flag = GUI_STATE_SWITCHING_CTX
        
        client = self.client
        
        if self.call is type(self).call_game:
            embed = self.render_game()
        elif self.call is type(self).call_menu:
            embed = self.render_menu()
        else:
            embed = self.render_done()
        
        try:
            message = yield SlashResponse(embed=embed, force_new_message=True)
        except BaseException as err:
            
            if self._task_flag == GUI_STATE_SWITCHING_CTX:
                self._task_flag = GUI_STATE_READY
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.renew', err)
            return
        
        tasks = []
        if self.call is type(self).call_game:
            for emoji in self.emojis_game_p1:
                task = Task(client.reaction_add(message, emoji), KOKORO)
                tasks.append(task)
            
            task = Task(client.reaction_add(message, self.stage.source.emoji), KOKORO)
            tasks.append(task)
            
            for emoji in self.emojis_game_p2:
                task = Task(client.reaction_add(message, emoji), KOKORO)
                tasks.append(task)
        
        elif self.call is type(self).call_menu:
            for emoji in self.emojis_menu:
                task = Task(client.reaction_add(message, emoji), KOKORO)
                tasks.append(task)
        
        else:
            task = Task(client.reaction_add(message, self.RESET), KOKORO)
            tasks.append(task)
            task = Task(client.reaction_add(message, self.CANCEL), KOKORO)
            tasks.append(task)
        
        try:
            await WaitTillAll(tasks, KOKORO)
        except BaseException as err:
            for task in tasks:
                task.cancel()
            
            if self._task_flag == GUI_STATE_SWITCHING_CTX:
                self._task_flag = GUI_STATE_READY
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.unknown_emoji, # no permission to use external emoji
                        ERROR_CODES.max_reactions, # maximal amount of reactions reached
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.renew', err)
            return
        
        try:
            await client.reaction_clear(self.message)
        except BaseException as err:
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.renew', err)
            return
        
        client.events.reaction_add.remove(self.message, self)
        
        self.message = message
        self.channel = channel
        
        client.events.reaction_add.append(message, self)
        
        self.last = LOOP_TIME()
        
        if self._task_flag == GUI_STATE_SWITCHING_CTX:
            self._task_flag = GUI_STATE_READY
        
    def render_done(self):
        stage = self.stage
        steps = len(stage.history)
        
        rating = stage.source.rate(steps)
        
        embed = Embed(f'{stage.source.name} finished with {steps} steps with {rating} rating!',
            stage.render(), COLORS[stage.source.difficulty])
        embed.add_footer(f'steps : {steps}, best : {stage.best}')
        embed.add_author(self.user.avatar_url_as('png', 32), self.user.full_name)
        return embed
    
    def render_game(self):
        stage = self.stage
        
        title_parts = [stage.source.name]
        if stage.has_skill:
            title_parts.append(stage.source.emoji.as_emoji)
            if stage.next_skill:
                title_parts.append('READY')
            
        embed = Embed(' '.join(title_parts), stage.render(), COLORS[stage.source.difficulty])
        footer = f'steps : {len(stage.history)}'
        if stage.best:
            footer = f'{footer}, best : {stage.best}'
        embed.add_footer(footer)
        embed.add_author(self.user.avatar_url_as('png', 32), self.user.full_name)
        return embed

    def get_cache(self, chapter, force=False):
        cache = self.cache[chapter]
        if cache is None:
            cache = self.cache[chapter]=[]
            force = True
        
        if not force:
            return cache
        
        cache.clear()
        
        difficulties = STAGES[chapter]
        
        additional = chapter*33
        
        levels=difficulties[0]
        for index in range(len(levels)):
            value = self.value_from_position(additional+index)
            cache.append((levels[index], value),)
            if value:
                continue
            break
        
        
        if len(cache) == len(levels) and cache[-1][1]:
            additional -= 7
            for diff_index in range(1,4):
                additional += 10
                levels = difficulties[diff_index]
                for index in range(len(levels)):
                    value = self.value_from_position(additional+index)
                    cache.append((levels[index], value),)
                    if value:
                        continue
                    break
        
        return cache
    
    def render_menu(self):
        position = self.position
        i1, rest = divmod(position, 33)
        if rest < 3:
            i2 = 0
            i3 = rest
        else:
            i2, i3 = divmod(rest+7, 10)
        
        cache = self.get_cache(i1)
        
        embed = Embed(f'Chapter {chr(i1+49)}')
        embed.add_thumbnail(CHARS[i1][3].url)
        
        if len(cache) > 1 or (i1 == 0) or self.value_from_position(i1*33-21):
            
            for target_index, element in enumerate(cache):
                stage = element[0]
                
                if stage.difficulty == i2 and stage.level == i3:
                    embed.color = COLORS[stage.difficulty]
                    break
            
            if target_index < 3:
                to_render = cache[4::-1]
            elif target_index > len(cache)-3:
                to_render = cache[:-6:-1]
            else:
                to_render = cache[target_index+2:target_index-3:-1]
                
            for stage, steps in to_render:
                field_name = f'{("Tutorial","Easy","Normal","Hard")[stage.difficulty]} level {stage.level+1}'
                if steps == 0:
                    field_value='No results recorded yet!'
                else:
                    field_value=f'rating {stage.rate(steps)}; steps : {steps}'
                
                
                if stage.difficulty == i2 and stage.level == i3:
                    field_name = f'**{field_name}**'
                    field_value = f'**{field_value}**'
                
                embed.add_field(field_name, field_value)
        
        else:
            embed.color = COLORS[0]
            embed.description=f'**You must finish chapter {chr(i1+48)} Easy 10 first.**'
        
        embed.add_author(self.user.avatar_url_as('png', 32), self.user.full_name)
        return embed                     
    
    def value_from_position(self, position):
        position = position<<1
        return int.from_bytes(self.data[position:position+2], byteorder='big')
    
    def write_value(self, position, value):
        position = position<<1
        self.data[position:position+2] = value.to_bytes(2, byteorder='big')
    
    async def reaction_delete(self, emoji):
        client = self.client
        
        try:
            await client.reaction_delete(self.message, emoji, self.user)
        except BaseException as err:
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.reaction_delete', err)
            return

#:-> @ <-:#}{#:-> @ <-:#{ game }#:-> @ <-:#}{#:-> @ <-:#

PASSABLE    = 0b0000000000000111

FLOOR       = 0b0000000000000001
TARGET      = 0b0000000000000010
HOLE_P      = 0b0000000000000011
OBJECT_P    = 0b0000000000000100


PUSHABLE    = 0b0000000000111000

BOX         = 0b0000000000001000
BOX_TARGET  = 0b0000000000010000
BOX_HOLE    = 0b0000000000011000
BOX_OBJECT  = 0b0000000000100000


SPECIAL     = 0b0000000011000000

HOLE_U      = 0b0000000001000000
OBJECT_U    = 0b0000000010000000


CHAR        = 0b0000011100000000
CHAR_N      = 0b0000010000000000
CHAR_E      = 0b0000010100000000
CHAR_S      = 0b0000011000000000
CHAR_W      = 0b0000011100000000

##CN_FLOOR    = 0b0000010000000001
##CE_FLOOR    = 0b0000010100000001
##CS_FLOOR    = 0b0000011000000001
##CW_FLOOR    = 0b0000011100000001
##
##CN_TARGET   = 0b0000010000000010
##CE_TARGET   = 0b0000010100000010
##CS_TARGET   = 0b0000011000000010
##CW_TARGET   = 0b0000011100000010
##
##CN_OBJECT_P = 0b0000010000000011
##CE_OBJECT_P = 0b0000010100000011
##CS_OBJECT_P = 0b0000011000000011
##CW_OBJECT_P = 0b0000011100000011
##
##CN_HOLE_P   = 0b0000010000000100
##CE_HOLE_P   = 0b0000010100000100
##CS_HOLE_P   = 0b0000011000000100
##CW_HOLE_P   = 0b0000011100000100

WALL        = 0b1111100000000000

NOTHING     = 0b0000100000000000
WALL_N      = 0b0001000000000000
WALL_E      = 0b0010000000000000
WALL_S      = 0b0100000000000000
WALL_W      = 0b1000000000000000
##WALL_A      = 0b1111000000000000
##WALL_SE     = 0b0110000000000000
##WALL_SW     = 0b1100000000000000

UNPUSHABLE  = WALL|SPECIAL
BLOCKS_LOS  = WALL|PUSHABLE|OBJECT_U



class history_element:
    __slots__ = ('changes', 'position', 'was_skill')
    
    def __init__(self, position, was_skill, changes):
        self.position=position
        self.was_skill=was_skill
        self.changes=changes

DIFFICULTY_NAMES = ('Tutorial', 'Easy', 'Normal', 'Hard')
class stage_source:
    __slots__ = ('best', 'chapter', 'char', 'difficulty', 'level', 'map', 'size', 'start', 'targets')
    
    def __init__(self, header, map_):
        self.chapter = int(header[0])
        self.difficulty = int(header[1])
        self.targets = int(header[2])
        self.size = int(header[3])
        self.start = int(header[4])
        self.best = int(header[5])
        
        self.char = CHARS[self.chapter]
        
        self.map = map_.copy()
        
        level_cont = STAGES[self.chapter][self.difficulty]
        self.level = len(level_cont)
        level_cont.append(self)
    
    @property
    def style(self):
        return self.char[0]

    @property
    def activate_skill(self):
        return self.char[1]

    @property
    def use_skill(self):
        return self.char[2]

    @property
    def emoji(self):
        return self.char[3]
    
    def rate(self, steps):
        best = self.best
        for rating in ('S', 'A', 'B', 'C', 'D', 'E'):
            if steps <= best:
                break
            best +=5
        return rating

    @property
    def position(self):
        position = self.chapter*33+self.level
        if self.difficulty:
            return position-7+self.difficulty*10
        return position
    
    @property
    def name(self):
        return f'Chapter {chr(49+self.chapter)} {DIFFICULTY_NAMES[self.difficulty]} level {self.level+1}'

class stage_backend:
    __slots__ = ('best', 'has_skill', 'history', 'map', 'next_skill', 'position', 'source')
    
    def __init__(self, source, best):
        self.source = source
        self.map = source.map.copy()
        self.position=source.start
        self.history = []
        self.has_skill = True
        self.next_skill = False
        self.best = best
        
    def done(self):
        targets = self.source.targets
        for tile in self.map:
            if tile == BOX_TARGET:
                targets -= 1
                if targets == 0:
                    if self.best == 0 or self.best > len(self.history):
                        self.best = len(self.history)
                    return True
        
        return False

    def move_north(self):
        return self.move(-self.source.size, CHAR_N)

    def move_east(self):
        return self.move(1, CHAR_E)

    def move_south(self):
        return self.move(self.source.size, CHAR_S)

    def move_west(self):
        return self.move(-1, CHAR_W)
            
    def move(self, step, align):
        if self.next_skill:
            result = self.source.use_skill(self, step, align)
            if result:
                self.next_skill=False
            return result
        
        map_ = self.map
        position = self.position

        actual_tile = map_[position]
        target_tile = map_[position+step]
        
        if target_tile&UNPUSHABLE:
            return False
        
        if target_tile&PASSABLE:
            self.history.append(history_element(position, False, (
                (position, actual_tile), (position+step, target_tile))))
            
            map_[position] = actual_tile&PASSABLE
            self.position = position = position+step
            map_[position] = target_tile|align
            
            return True

        after_tile = map_[position+(step<<1)]

        if target_tile&PUSHABLE and after_tile&(PASSABLE|HOLE_U):
            self.history.append(history_element(self.position, False, (
                (position, actual_tile), (position+step, target_tile), (position+(step<<1), after_tile))))
            
            map_[position] = actual_tile&PASSABLE
            self.position = position = position+step
            map_[position] = (target_tile>>3)|align
            if after_tile&PASSABLE:
                map_[position+step] = after_tile<<3
            else:
                map_[position+step] = HOLE_P
            return True
        
        return False

    def activate_skill(self):
        if not self.has_skill:
            return False
        if self.source.activate_skill(self):
            self.next_skill = True
            return True
        return False
    
    
    def render(self):
        style = self.source.style
        result = []
        map_ = self.map
        limit = len(map_)
        step = self.source.size
        
        if limit <= 75:
            start =0
            shift = 0
        else:
            step_count = limit//step
            if step_count < step:
                if (step_count * (step-2)) <= 75:
                    start = 1
                    step -= 2
                    shift = 2
                else:
                    start = step+1
                    limit -= step
                    step -= 2
                    shift = 2
            else:
                if ((step_count-2) * step) <= 75:
                    start = step
                    limit -= step
                    shift = 0
                else:
                    start = step+1
                    limit -= step
                    step -= 2
                    shift = 2
        
        while start < limit:
            end = start+step
            result.append(''.join([style[element] for element in map_[start:end]]))
            start = end+shift
        
        return '\n'.join(result)

    def back(self):
        if self.next_skill:
            self.next_skill = False
            return True
        
        history = self.history
        if not history:
            return False
        
        element = history.pop(-1)
        map_ = self.map
        self.position = element.position
        
        for position, value in element.changes:
            map_[position] = value
        
        if element.was_skill:
            self.has_skill = True
        return True

    def reset(self):
        history = self.history
        if not history:
            return False

        history.clear()

        self.position = self.source.start
        self.map = self.source.map.copy()
        self.has_skill = True

        return True

NOTHING_EMOJI = Emoji.precreate(568838460434284574, name='0Q')

DEFAULT_STYLE_PARTS = {
    NOTHING                     : NOTHING_EMOJI.as_emoji,
    WALL_E                      : Emoji.precreate(568838488464687169, name='0P').as_emoji,
    WALL_S                      : Emoji.precreate(568838546853462035, name='0N').as_emoji,
    WALL_W                      : Emoji.precreate(568838580278132746, name='0K').as_emoji,
    WALL_N|WALL_E|WALL_S|WALL_W : Emoji.precreate(578678249518006272, name='0X').as_emoji,
    WALL_E|WALL_S               : Emoji.precreate(568838557318250499, name='0M').as_emoji,
    WALL_S|WALL_W               : Emoji.precreate(568838569087598627, name='0L').as_emoji,
    WALL_N|WALL_E               : Emoji.precreate(574312331849498624, name='01').as_emoji,
    WALL_N|WALL_W               : Emoji.precreate(574312332453216256, name='00').as_emoji,
    WALL_N|WALL_E|WALL_S        : Emoji.precreate(578648597621506048, name='0R').as_emoji,
    WALL_N|WALL_S|WALL_W        : Emoji.precreate(578648597546139652, name='0S').as_emoji,
    WALL_N|WALL_S               : Emoji.precreate(578654051848421406, name='0T').as_emoji,
    WALL_E|WALL_W               : Emoji.precreate(578674409968238613, name='0U').as_emoji,
    WALL_N|WALL_E|WALL_W        : Emoji.precreate(578676096829227027, name='0V').as_emoji,
    WALL_E|WALL_S|WALL_W        : Emoji.precreate(578676650389274646, name='0W').as_emoji,
        }

REIMU_STYLE = {
    WALL_N                      : Emoji.precreate(580141387631165450, name='0O').as_emoji,
    FLOOR                       : Emoji.precreate(574211101638656010, name='0H').as_emoji,
    TARGET                      : Emoji.precreate(574234087645249546, name='0A').as_emoji,
    OBJECT_P                    : NOTHING_EMOJI.as_emoji,
    HOLE_P                      : Emoji.precreate(574202754134835200, name='0I').as_emoji,
    BOX                         : Emoji.precreate(574212211434717214, name='0G').as_emoji,
    BOX_TARGET                  : Emoji.precreate(574213002190913536, name='0F').as_emoji,
    BOX_HOLE                    : Emoji.precreate(574212211434717214, name='0G').as_emoji,
    BOX_OBJECT                  : NOTHING_EMOJI.as_emoji,
    HOLE_U                      : Emoji.precreate(574187906642477066, name='0J').as_emoji,
    OBJECT_U                    : NOTHING_EMOJI.as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(574214258871500800, name='0D').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(574213472347226114, name='0E').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(574220751662612502, name='0B').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(574218036156825629, name='0C').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(574249292496371732, name='04').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(574249292026478595, name='07').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(574249292261490690, name='06').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(574249292487720970, name='05').as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(574249293662388264, name='02').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(574249291074240523, name='09').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(574249291145543681, name='08').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(574249292957614090, name='03').as_emoji,
    CHAR_N|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_E|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_S|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_W|OBJECT_P             : NOTHING_EMOJI.as_emoji,
        }
REIMU_STYLE.update(DEFAULT_STYLE_PARTS)

def REIMU_SKILL_ACTIVATE(self):
    size = self.source.size
    position = self.position
    map_ = self.map
    
    for step in (-size, 1, size, -1):
        target_tile=map_[position+step]
        
        if not target_tile&(PUSHABLE|SPECIAL):
            continue
        
        after_tile = map_[position+(step<<1)]

        if not after_tile&PASSABLE:
            continue
        
        return True
    
    return False
    
def REIMU_SKILL_USE(self, step, align):
    map_ = self.map
    position = self.position
    
    target_tile = map_[position+step]
    
    if not target_tile&(PUSHABLE|SPECIAL):
        return False
    
    after_tile = map_[position+(step<<1)]

    if not after_tile&PASSABLE:
        return False

    actual_tile = map_[position]
    self.history.append(history_element(position,True, ((position, actual_tile), (position+(step<<1), after_tile))))
    
    map_[position] = actual_tile&PASSABLE
    self.position = position = position+(step<<1)

    map_[position] = after_tile|align
    self.has_skill = False
    
    return True

REIMU_EMOJI = Emoji.precreate(574307645347856384, name='REIMU')

CHARS.append((REIMU_STYLE, REIMU_SKILL_ACTIVATE, REIMU_SKILL_USE, REIMU_EMOJI),)

FURANDOORU_STYLE = {
    WALL_N                      : Emoji.precreate(580143707534262282, name='0X').as_emoji,
    FLOOR                       : Emoji.precreate(580150656501940245, name='0Y').as_emoji,
    TARGET                      : Emoji.precreate(580153111545511967, name='0b').as_emoji,
    OBJECT_P                    : Emoji.precreate(580163014045728818, name='0e').as_emoji,
    HOLE_P                      : Emoji.precreate(580159124466303001, name='0d').as_emoji,
    BOX                         : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    BOX_TARGET                  : Emoji.precreate(580188214086598667, name='0f').as_emoji,
    BOX_HOLE                    : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    BOX_OBJECT                  : Emoji.precreate(580151963937931277, name='0a').as_emoji,
    HOLE_U                      : Emoji.precreate(580156463888990218, name='0c').as_emoji,
    OBJECT_U                    : Emoji.precreate(580151385258065925, name='0Z').as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(580357693022142485, name='0g').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(580357693093576714, name='0h').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(580357693160685578, name='0i').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(580357693152165900, name='0j').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(580357693018210305, name='0k').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(580357693085188109, name='0l').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(580357693181657089, name='0m').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(580357693361881089, name='0n').as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(580357693324132352, name='0o').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(580357693072736257, name='0p').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(580357693131456513, name='0q').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(580357693366337536, name='0r').as_emoji,
    CHAR_N|OBJECT_P             : Emoji.precreate(580357693143777300, name='0s').as_emoji,
    CHAR_E|OBJECT_P             : Emoji.precreate(580357692711763973, name='0t').as_emoji,
    CHAR_S|OBJECT_P             : Emoji.precreate(580357693269606410, name='0u').as_emoji,
    CHAR_W|OBJECT_P             : Emoji.precreate(580357693387177984, name='0v').as_emoji,
        }
FURANDOORU_STYLE.update(DEFAULT_STYLE_PARTS)

def FURANDOORU_SKILL_ACTIVATE(self):
    size = self.source.size
    position = self.position
    map_ = self.map
    
    for step in (-size, 1, size, -1):
        target_tile=map_[position+step]
        
        if target_tile == OBJECT_U:
            return True
    
    return False

def FURANDOORU_SKILL_USE(self, step, align):
    map_ = self.map
    position = self.position
    
    target_tile = map_[position+step]
    
    if target_tile != OBJECT_U:
        return False
    
    actual_tile = map_[position]
    self.history.append(history_element(position,True, ((position, actual_tile), (position+step, target_tile))))
    
    map_[position] = actual_tile&PASSABLE|align
    map_[position+step] = OBJECT_P
    self.has_skill = False
    
    return True

FURANDOORU_EMOJI = Emoji.precreate(575387120147890210, name='FURANDOORU')

CHARS.append((FURANDOORU_STYLE, FURANDOORU_SKILL_ACTIVATE, FURANDOORU_SKILL_USE, FURANDOORU_EMOJI),)

YUKARI_STYLE = {
    WALL_N                      : Emoji.precreate(593179300270702593, name='0w').as_emoji,
    FLOOR                       : Emoji.precreate(593179300426022914, name='0x').as_emoji,
    TARGET                      : Emoji.precreate(593179300019306556, name='0y').as_emoji,
    OBJECT_P                    : NOTHING_EMOJI.as_emoji,
    HOLE_P                      : Emoji.precreate(593179300287479833, name='0z').as_emoji,
    BOX                         : Emoji.precreate(593179300296130561, name='10').as_emoji,
    BOX_TARGET                  : Emoji.precreate(593179300136615936, name='11').as_emoji,
    BOX_HOLE                    : Emoji.precreate(593179300149067790, name='12').as_emoji,
    BOX_OBJECT                  : NOTHING_EMOJI.as_emoji,
    HOLE_U                      : Emoji.precreate(593179300153262196, name='13').as_emoji,
    OBJECT_U                    : NOTHING_EMOJI.as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(593179300161650871, name='14').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(593179300153262257, name='15').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(593179300300324887, name='16').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(593179300237410314, name='17').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(593179300207919125, name='18').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(593179300145135646, name='19').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(593179300170301451, name='1A').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(593179300153262189, name='1B').as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(593179300199399531, name='1C').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(593179300300193800, name='1D').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(593179300216176760, name='1E').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(593179300153524224, name='1F').as_emoji,
    CHAR_N|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_E|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_S|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_W|OBJECT_P             : NOTHING_EMOJI.as_emoji,
}
YUKARI_STYLE.update(DEFAULT_STYLE_PARTS)

def YUKARI_SKILL_ACTIVATE(self):
    map_=self.map
    
    x_size=self.source.size
    y_size=len(map_)//x_size

    position=self.position
    y_position, x_position=divmod(position, x_size)

##    x_min=x_size*y_position
##    x_max=x_size*(y_position+1)-1
##    y_min=x_position
##    y_max=x_position+(x_size*(y_size-1))
    
    for step, limit in (
            (-1, x_size*y_position),
            (1, x_size*(y_position+1)-1),
            (-x_size, -x_size),
            (x_size, x_position+(x_size*(y_size-1))),
                 ):
        target_position = position+step
        if target_position == limit:
            continue
        if not map_[target_position]&BLOCKS_LOS:
            continue
        while True:
            target_position = target_position+step
            if target_position == limit:
                break
            target_tile = map_[target_position]
            if target_tile&BLOCKS_LOS:
                continue
            if target_tile&PASSABLE:
                return True
            break
    return False

def YUKARI_SKILL_USE(self, step, align):
    map_ = self.map

    x_size = self.source.size
    y_size = len(map_)//x_size
    
    position=self.position
    y_position, x_position = divmod(position, x_size)

    if step > 0:
        if step == 1:
            limit = x_size*(y_position+1)-1
        else:
            limit = x_position+(x_size*(y_size-1))
    else:
        if step == -1:
            limit = x_size*y_position
        else:
            limit = -x_size

    target_position = position+step
    if target_position == limit:
        return False
    if not map_[target_position]&BLOCKS_LOS:
        return False
    while True:
        target_position = target_position+step
        if target_position==limit:
            return False
        target_tile = map_[target_position]
        if target_tile&BLOCKS_LOS:
            continue
        if target_tile&PASSABLE:
            break
        return False

    actual_tile = map_[position]
    self.history.append(history_element(position,True, ((position, actual_tile), (target_position, target_tile))))
    
    map_[position] = actual_tile&PASSABLE
    self.position = target_position
    
    map_[target_position] = target_tile|align
    self.has_skill = False
    
    return True

YUKARI_EMOJI = Emoji.precreate(575389643424661505, name='YUKARI')

CHARS.append((YUKARI_STYLE, YUKARI_SKILL_ACTIVATE, YUKARI_SKILL_USE, YUKARI_EMOJI),)

RULES_HELP = Embed('Rules of Dungeon sweeper',
    'Your quest is to help our cute Touhou characters to put their stuffs on places, where they supposed be. These '
    f'places are marked with an {BUILTIN_EMOJIS["x"]:e} on the floor. Because our characters are lazy, the less steps '
    'required to sort their stuffs, makes them give you a better rating.\n'
    '\n'
    'You can move with the reactions under the embed, to activate your characters\' skill, or go back, reset the map '
    'or cancel the game:\n'
    f'{ds_game.WEST:e}{ds_game.NORTH:e}{ds_game.SOUTH:e}{ds_game.EAST:e}{REIMU_EMOJI:e}{ds_game.BACK:e}'
    f'{ds_game.RESET:e}{ds_game.CANCEL:e}\n'
    'You can show push boxes by moving towards them, but you cannot push more at the same time time or push into the '
    'wall:\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[FLOOR]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}'
    '\n'
    'You can push the boxes into the holes to pass them, but be careful, you might lose too much boxes to finish the '
    'stages!\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[HOLE_U]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[HOLE_P]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[FLOOR]}{REIMU_STYLE[CHAR_E|HOLE_P]}\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[HOLE_P]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX_HOLE]}\n'
    'If you get a box on the it\'s desired place it\'s color will change:\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[TARGET]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX_TARGET]}\n'
    'The game has 3 chapters. *(there will be more maybe.)* Each chapter introduces a different character to '
    'play with.',
    color=COLORS[0],
).add_field(f'Chapter 1 {REIMU_EMOJI:e}',
    'Your character is Hakurei Reimu (博麗　霊夢), who needs some help at her basement to sort her *boxes* out.\n'
    'Reimu can jump over a box or hole.\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[FLOOR]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[BOX]}{REIMU_STYLE[CHAR_E|FLOOR]}\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]:}{REIMU_STYLE[HOLE_U]}{REIMU_STYLE[FLOOR]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}{REIMU_STYLE[HOLE_U]}{REIMU_STYLE[CHAR_E|FLOOR]}'
).add_field(f'Chapter 2 {FURANDOORU_EMOJI:e}',
    'Your character is Scarlet Flandre (スカーレット・フランドール Sukaaretto Furandooru), who want to put her *bookshelves*'
    f'on their desired place.\n'
    'Flandre can destroy absolutely anything and everything, and she will get rid of the pillars for you.\n'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}{FURANDOORU_STYLE[OBJECT_U]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}{FURANDOORU_STYLE[OBJECT_P]}{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{FURANDOORU_STYLE[FLOOR]}{FURANDOORU_STYLE[CHAR_E|OBJECT_P]}\n'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}{FURANDOORU_STYLE[BOX]}{FURANDOORU_STYLE[OBJECT_P]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}{FURANDOORU_STYLE[FLOOR]}{FURANDOORU_STYLE[CHAR_E|FLOOR]}'
    f'{FURANDOORU_STYLE[BOX_OBJECT]}'
).add_field(f'Chapter 3 {YUKARI_EMOJI:e}',
    'Your character is Yakumo Yukari (八雲　紫). Her beddings needs some replacing at her home.\n'
    'Yukari can create gaps and travel trough them. She will open gap to the closest place straightforward, which is '
    f'separated by a bedding or with wall from her.\n'
    f'{YUKARI_STYLE[CHAR_E|FLOOR]}{YUKARI_STYLE[WALL_N]}{YUKARI_STYLE[WALL_N]}{YUKARI_STYLE[FLOOR]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}{YUKARI_STYLE[FLOOR]}{YUKARI_STYLE[WALL_N]}{YUKARI_STYLE[WALL_N]}'
    f'{YUKARI_STYLE[CHAR_E|FLOOR]}\n'
    f'{YUKARI_STYLE[CHAR_E|FLOOR]}{YUKARI_STYLE[BOX]}{YUKARI_STYLE[BOX]}{YUKARI_STYLE[FLOOR]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}{YUKARI_STYLE[FLOOR]}{YUKARI_STYLE[BOX]}{YUKARI_STYLE[BOX]}'
    f'{YUKARI_STYLE[CHAR_E|FLOOR]}'
)

def loader(filename):

    for _ in range(len(CHARS)):
        STAGES.append(([], [], [], []),)
            
    PATTERN_HEADER = re.compile('[a-zA-Z0-9_]+')
    PATTERN_MAP = re.compile('[A-Z_]+')

    PATTERNS = {
        'FLOOR'     : FLOOR,
        'TARGET'    : TARGET,
        'BOX'       : BOX,
        'BOX_TARGET': BOX_TARGET,
        'HOLE_U'    : HOLE_U,
        'HOLE_P'    : HOLE_P,
        'OBJECT_U'  : OBJECT_U,
        'CN_FLOOR'  : CHAR_N|FLOOR,
        'CE_FLOOR'  : CHAR_E|FLOOR,
        'CS_FLOOR'  : CHAR_S|FLOOR,
        'CW_FLOOR'  : CHAR_W|FLOOR,
        'NOTHING'   : NOTHING,
        'WALL_N'    : WALL_N,
        'WALL_E'    : WALL_E,
        'WALL_S'    : WALL_S,
        'WALL_W'    : WALL_W,
        'WALL_HV'   : WALL_N|WALL_E|WALL_S|WALL_W,
        'WALL_SE'   : WALL_E|WALL_S,
        'WALL_SW'   : WALL_S|WALL_W,
        'WALL_NE'   : WALL_N|WALL_E,
        'WALL_NW'   : WALL_N|WALL_W,
        'WALL_HE'   : WALL_N|WALL_E|WALL_S,
        'WALL_HW'   : WALL_N|WALL_S|WALL_W,
        'WALL_H'    : WALL_N|WALL_S,
        'CN_TARGET' : CHAR_N|TARGET,
        'CE_TARGET' : CHAR_E|TARGET,
        'CS_TARGET' : CHAR_S|TARGET,
        'CW_TARGET' : CHAR_W|TARGET,
        'WALL_V'    : WALL_E|WALL_W,
        'WALL_NV'   : WALL_E|WALL_S|WALL_W,
        'WALL_SV'   : WALL_N|WALL_E|WALL_W,
    }

    STATE = 0
    map_ = []
    
    with open(filename, 'r') as file:
        for debug_index, line in enumerate(file, 1):
            try:
                if STATE == 0:
                    if len(line) > 2:
                        header = PATTERN_HEADER.findall(line)
                        STATE = 1
                    
                    continue
                
                if STATE == 1:
                    if len(line) > 2:
                        STATE = 2
                    else:
                        continue
                    
                if STATE == 2:
                    if len(line) > 2:
                        map_.extend(PATTERNS[element] for element in PATTERN_MAP.findall(line))
                    else:
                        stage_source(header, map_)
                        map_.clear()
                        STATE = 0
                    continue
                
            except KeyError as err:
                print(f'Exception at line {debug_index}:\n{err!r}')
                if STATE == 2:
                    print(', '.join(re.findall(PATTERN_MAP, line)))
                map_.clear()
                break
                
        if map_:
            stage_source(header, map_)

loader(os.path.join(PATH__KOISHI, 'library', 'ds.txt'))

del DEFAULT_STYLE_PARTS

del REIMU_STYLE
del REIMU_SKILL_ACTIVATE
del REIMU_SKILL_USE
del REIMU_EMOJI

del FURANDOORU_STYLE
del FURANDOORU_SKILL_ACTIVATE
del FURANDOORU_SKILL_USE
del FURANDOORU_EMOJI

del YUKARI_STYLE
del YUKARI_SKILL_ACTIVATE
del YUKARI_SKILL_USE
del YUKARI_EMOJI


async def ds_modify_best(client, message, content):
    if not client.is_owner(message.author):
        return
    try:
        position = int(content)
    except ValueError:
        return

    i1, rest = divmod(position, 33)
    if rest < 3:
        i2 = 0
        i3 = rest
    else:
        i2, i3 = divmod(rest+7, 10)
        
    best=STAGES[i1][i2][i3].best
        
    position=position<<1

    count=0
    
    async with DB_ENGINE.connect() as connector:
        result = await connector.execute(DS_TABLE.select())
        stats = await result.fetchall()
        for obj in stats:
            data = obj.data
            amount = int.from_bytes(data[position:position+2], byteorder='big')
            
            if amount == 0:
                continue
            if amount >= best:
                continue
            
            data = bytearray(data)
            data[position:position+2] = best.to_bytes(2, byteorder='big')
            
            await connector.execute(DS_TABLE.update(). \
                values(data=data). \
                where(ds_model.user_id==obj.user_id))

            count += 1

    await client.message_create(message.channel, f'modified : {count}')
    
async def ds_modify_best_description(command_context):
    return Embed('ds_modify_best', (
        f'A helper command for `{command_context.prefix}ds`, to modify the best results of a stage.\n'
        'Before calling this command, make sure you edited the source code and restarted me.\n'
        f'Usage : `{command_context.prefix}ds_modify_best *position*`\n'
        'The `position` is the position of the stage.'
            ), color=DS_COLOR).add_footer(
            'Owner only!')

COMMAND_CLIENT : Client
COMMAND_CLIENT.commands(ds_modify_best,
    checks = checks.owner_only(),
    category = 'GAMES',
    description = ds_modify_best_description,
)
