# -*- coding: utf-8 -*-
import re

from hata import CHANNELS, KOKORO, DiscordException, ERROR_CODES, sleep, ScarletExecutor, ClientWrapper, MESSAGES, \
    Color, Embed, Emoji, CLIENTS, Role, ROLES, EMOJIS, WeakKeyDictionary, Client, parse_message_reference, \
    ChannelBase, INTERACTION_EVENT_RESPONSE_STATE_NONE, INTERACTION_EVENT_RESPONSE_STATE_DEFERRED, \
    INTERACTION_EVENT_RESPONSE_STATE_RESPONDED

from hata.ext.commands import ContentParser, Converter, ChooseMenu, Pagination, ConverterFlag, Closer
from hata.ext.slash import abort

from bot_utils.models import DB_ENGINE, auto_react_role_model, AUTO_REACT_ROLE_TABLE

ROLE_CONVERTER = Converter('role', flags=ConverterFlag.role_default.update_by_keys(everywhere=True))
MESSAGE_CONVERTER = Converter('message', flags=ConverterFlag.message_default.update_by_keys(everywhere=True))

SLASH_CLIENT: Client

async def teardown(lib):
    async with ScarletExecutor(limit=20) as executor:
        for gui in AUTO_REACT_ROLE_GUIS.values():
            await executor.add(gui.cancel())
    
    AUTO_REACT_ROLE_GUIS.clear()

AUTO_REACT_ROLE_COLOR = Color.from_rgb(219, 31, 87)

BEHAVIOUR_FLAG_KEYS = {
    'remove_emoji_if_role': 0,
    'remove_role_if_emoji': 1,
}

class BehaviourFlag(int):
    @property
    def remove_emoji_if_role(self):
        return self&1
    
    @property
    def remove_role_if_emoji(self):
        return (self>>1)&1
    
    def update_by_keys(self,**kwargs):
        
        new = self
        for name, value in kwargs.items():
            shift = BEHAVIOUR_FLAG_KEYS[name]
            if value:
                new = new | (1<<shift)
            else:
                if (new>>shift)&1:
                    new = new^(1<<shift)
        
        return type(self)(new)
    
    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

AUTO_REACT_ROLE = SLASH_CLIENT.interactions(None,
    name = 'auto-react-role',
    description = 'Fire in my soul!',
    is_global=True,
        )

AUTO_REACT_ROLE.interactions(name='create', show_for_invking_user_only=True)
async def create_auto_react_role(client, event,
        message: ('str', 'Please reference a message!'),
            ):
    """Adds roles if the users reacts on a message. (Admin only)"""
    guild = event.guild
    if guild is None:
        abort('Guild only command!')
    
    if guild not in client.guild_profiles:
        abort('I must be in the guild to execute this command.')
    
    message_reference = parse_message_reference(message)
    if message_reference is None:
        abort('Could not identify the message.')
    
    guild_id, channel_id, message_id = message_reference
    try:
        target_message = MESSAGES[message_id]
    except KeyError:
        if channel_id:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                abort('I have no access to the channel.')
                return # Or hinter goes brr
        else:
            channel = event.channel
        
        if not channel.cached_permissions_for(client).can_read_message_history:
            abort('Ohoho', 'I have no permission to get that message.')
            return
        
        # We only really need `channel_id` and `guild_id`, so we can ignore `guild_id`.
        yield
        
        try:
            target_message = await client.message_get(channel, message_id)
        except ConnectionError:
            # No internet
            return
        except DiscordException as err:
            if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                        ):
                # The message is already deleted.
                abort('The referenced message is already yeeted.')
            
            if err.code == ERROR_CODES.missing_access: # client removed
                # This is not nice.
                return
            
            if err.code == ERROR_CODES.missing_permissions: # permissions changed meanwhile
                abort('I have no permission to get that message.')
            
            raise
    
    target_guild = target_message.guild
    if target_guild is None:
        abort('The referenced message is inside of a private channel.')
    
    if not target_guild.permissions_for(event.user).can_administrator:
        if guild is target_guild:
            error_message = 'You must have `administrator` permission to invoke this command.'
        else:
            error_message = 'You must have `administrator` permission in the respective guild to invoke this command.'
        abort(error_message)
    
    permissions = target_guild.cached_permissions_for(client)
    if (not permissions.can_manage_messages) or (not permissions.can_manage_roles):
        if guild is target_guild:
            error_message = 'I need to have `manage messages` and `manage roles` permissions to invoke this command.'
        else:
            error_message = 'I need to have `manage messages` and `manage roles` permissions in the respective guild ' \
                            'to invoke this command.'
        abort(error_message)
    
    await AutoReactRoleGUI(client, target_message, event, guild)


def iterate_embed_parts(embed):
    part = embed.title
    if (part is not None):
        yield part
    
    part = embed.description
    if (part is not None):
        yield part
    
    for field in embed.fields:
        yield field.name
        yield field.value

def render_message_content(message):
    content = message.content
    if content:
        if len(content) > 200:
            space_position = content.rfind(' ', 180, 200)
            if space_position == -1:
                space_position = 197
            
            content = content[:space_position]+'...'
    else:
        embeds = message.embeds
        if (embeds is None) or (not embeds):
            content = None
        else:
            embed = embeds[0]
            leftover_length = 200
            collected_parts = []
            for part in iterate_embed_parts(embed):
                if len(part) <= leftover_length:
                    collected_parts.append(part)
                    collected_parts.append(' ')
                    leftover_length = leftover_length-len(part)-1
                    
                    if leftover_length < 20:
                        break
                
                else:
                    space_position = content.rfind(' ', leftover_length-20, leftover_length)
                    if space_position == -1:
                        space_position = leftover_length-4
                    
                    part = part[:space_position]
                    collected_parts.append(part)
                    collected_parts.append('...')
                    break
            
            if collected_parts:
                if collected_parts[-1] == ' ':
                    del collected_parts[-1]
                    
                content = ''.join(collected_parts)
            else:
                content = None
    
    return content

AUTO_REACT_ROLE_GUI_EMBED_FIELD_NAME = 'HOW TO'
AUTO_REACT_ROLE_GUI_EMBED_FIELD_VALUE = (
    'Type `add <emoji> <role>` to add a new emoji-role pair to add a new connection\n'
    'Type `del <emoji>` or `del <role>` to remove a connection.\n'
    'Type `behaviour enable/disable delete role/emoji` to enable or disable deleting the emoji if the role is removed, '
    'or deleting the role if the emoji is removed.\n'
    'Type `apply` to save or `cancel` to not.\n'
    'Type `destroy` to destroy the auto react role instance, if exists.'
        )

SUB_COMMAND_RP = re.compile('(add|del|behaviour|apply|cancel|destroy)(?:[ \t]+(.+))?', re.I)
SUB_BEHAVIOUR_RP = re.compile('(?:(enable|disable)[ \t]+)?delete[ \t]+(role|emoji)', re.I)

CHANGE_STATE_NONE    = 0
CHANGE_STATE_ADDED   = 1
CHANGE_STATE_ACTUAL  = 2
CHANGE_STATE_REMOVED = 3

class AutoReactRoleChange:
    __slots__ = ('added', 'removed', 'actual', 'old_behaviour', 'new_behaviour', 'guild',)
    
    def __init__(self, manager, guild):
        self.guild = guild
        
        if manager is None:
            actual = None
        else:
            relations = manager.relations
            if relations:
                actual = []
                for item in relations.items():
                    if type(item[0]) is Emoji:
                        actual.append(item)
            else:
                actual = None
        
        self.actual = actual
        
        if manager is None:
            behaviour = BehaviourFlag()
        else:
            behaviour = manager.behaviour
        
        self.old_behaviour = behaviour
        self.new_behaviour = behaviour
        
        self.added = []
        self.removed = []
    
    def changed(self):
        if self.added:
            return True
        
        if self.removed:
            return True
        
        if self.old_behaviour != self.new_behaviour:
            return True
        
        return False
    
    def update_behaviour(self,updates):
        actual = self.new_behaviour
        new = actual.update_by_keys(**updates)
        self.new_behaviour = new
        return (actual != new)
    
    def get_state_and_item(self, object_):
        index = (type(object_) is Role)
        
        added = self.added
        if added:
            for item in added:
                if item[index] is object_:
                    return CHANGE_STATE_ADDED, item
        
        actual = self.actual
        if (actual is not None) and actual:
            for item in actual:
                if item[index] is object_:
                    return CHANGE_STATE_ACTUAL, item
        
        removed = self.removed
        if removed:
            for item in removed:
                if item[index] is object_:
                    return CHANGE_STATE_REMOVED, item
        
        return CHANGE_STATE_NONE, None
    
    def add(self, emoji, role):
        emoji_state, emoji_item = self.get_state_and_item(emoji)
        role_state,  role_item  = self.get_state_and_item(role)
        
        # if both item is same, emoji_state and role_state is None
        if emoji_item is role_item is not None:
            if emoji_state == CHANGE_STATE_ADDED:
                return
            
            if emoji_state == CHANGE_STATE_ACTUAL:
                return
            
            if emoji_state == CHANGE_STATE_REMOVED:
                self.removed.remove(emoji_item)
                self.actual.append(emoji_item)
                return
            
            return
        
        actual_length = len(self.added)
        if (self.actual is not None):
            actual_length += len(self.actual)
        if emoji_state in (CHANGE_STATE_ADDED, CHANGE_STATE_ACTUAL):
            actual_length -=1
        if role_state in (CHANGE_STATE_ADDED, CHANGE_STATE_ACTUAL):
            actual_length -=1
        
        if actual_length>=20:
            return False
        
        self.added.append((emoji,role))
        
        if emoji_state == CHANGE_STATE_ADDED:
            self.added.remove(emoji_item)
        elif emoji_state == CHANGE_STATE_ACTUAL:
            self.actual.remove(emoji_item)
            self.removed.append(emoji_item)
        
        if role_state == CHANGE_STATE_ADDED:
            self.added.remove(role_item)
        elif role_state == CHANGE_STATE_ACTUAL:
            self.actual.remove(emoji_item)
            self.removed.append(emoji_item)
        
        return True
    
    def remove(self, object_):
        index = (type(object_) is Role)
        
        while True:
            added = self.added
            if not added:
                break
            
            for item in added:
                if item[index] is object_:
                    break
            else:
                break
            
            added.remove(item)
            return True
        
        while True:
            actual = self.actual
            if (actual is None):
                break
            
            if (not actual):
                break
                
            for item in actual:
                if item[index] is object_:
                    break
            else:
                break
            
            actual.remove(item)
            self.removed.append(item)
            return True
        
        # if in removed do nothing.
        return False
    
    def render(self):
        result = []
        added = self.added
        if added:
            result.append('Added relations:\n')
            for emoji, role in added:
                result.append(emoji.as_emoji)
                result.append(' -> ')
                if role.guild is self.guild:
                    result.append(role.mention)
                else:
                    result.append('@')
                    result.append(role.name)
                result.append('\n')
            add_line = True
        else:
            add_line = False
        
        actual = self.actual
        if (actual is not None) and actual:
            if add_line:
                result.append('\n')
            else:
                add_line = True
            result.append('Actual relations:\n')
            for emoji, role in actual:
                result.append(emoji.as_emoji)
                result.append(' -> ')
                if role.guild is self.guild:
                    result.append(role.mention)
                else:
                    result.append('@')
                    result.append(role.name)
                
                result.append('\n')
        
        removed = self.removed
        if actual:
            if add_line:
                result.append('\n')
            else:
                add_line = True
            result.append('Removed relations:\n')
            for emoji, role in removed:
                result.append(emoji.as_emoji)
                result.append(' -> ')
                if role.guild is self.guild:
                    result.append(role.mention)
                else:
                    result.append('@')
                    result.append(role.name)
                result.append('\n')
        
        old_behaviour = self.old_behaviour
        new_behaviour = self.new_behaviour
        
        added = BehaviourFlag(new_behaviour&(~old_behaviour))
        if added:
            result.append('Added behaviours:\n')
            if added.remove_emoji_if_role:
                result.append('- remove the emoji if the role is removed')
            
            if added.remove_role_if_emoji:
                result.append('- remove the role if the emoji is removed')
            
            result.append('\n')
            
        actual = BehaviourFlag(new_behaviour&old_behaviour)
        if actual:
            result.append('Actual behaviours:\n')
            if actual.remove_emoji_if_role:
                result.append('- remove the emoji if the role is removed')
            
            if actual.remove_role_if_emoji:
                result.append('- remove the role if the emoji is removed')
            
            result.append('\n')
        
        removed = BehaviourFlag(old_behaviour&(~new_behaviour))
        if removed:
            result.append('Removed behaviours:\n')
            if removed.remove_emoji_if_role:
                result.append('- remove the emoji if the role is removed')
            
            if removed.remove_role_if_emoji:
                result.append('- remove the role if the emoji is removed')
            
            result.append('\n')
        
        if result:
            del result[-1]
            return ''.join(result)
        
        return None
    
    def __repr__(self):
        result =[
            '<',
            self.__class__.__name__,
            ' added='
                ]
        
        added = self.added
        if added:
            result.append('{')
            for emoji, role in added:
                result.append(repr(emoji))
                result.append(': ')
                result.append(repr(role))
                result.append(', ')
            result[-1] = '}'
        else:
            result.append('{}')
        
        result.append(', actual=')
        actual = self.actual
        if (actual is not None) and actual:
            result.append('{')
            for emoji, role in actual:
                result.append(repr(emoji))
                result.append(': ')
                result.append(repr(role))
                result.append(', ')
            result[-1] = '}'
        else:
            result.append('{}')
        
        result.append(', removed=')
        removed = self.removed
        if removed:
            result.append('{')
            for emoji, role in removed:
                result.append(repr(emoji))
                result.append(': ')
                result.append(repr(role))
                result.append(', ')
            result[-1] = '}'
        else:
            result.append('{}')
        
        old_behaviour = self.old_behaviour
        new_behaviour = self.new_behaviour
        
        if old_behaviour == new_behaviour:
            result.append(', behaviour=')
            result.append(repr(old_behaviour))
        else:
            result.append(', old_behaviour=')
            result.append(repr(old_behaviour))
            result.append(', new_behaviour=')
            result.append(repr(new_behaviour))
        
        result.append('>')
        
        return ''.join(result)

AUTO_REACT_ROLE_GUIS = WeakKeyDictionary()

class AutoReactRoleGUI:
    __slots__ = ('target_message', 'changes', 'manager', 'message', 'client', 'guild', )
    def render(self):
        message = self.target_message
        embed = Embed(render_message_content(message), self.changes.render(), color=AUTO_REACT_ROLE_COLOR)
        embed.add_author(message.author.avatar_url,message.author.full_name,message.url)
        embed.add_field(AUTO_REACT_ROLE_GUI_EMBED_FIELD_NAME, AUTO_REACT_ROLE_GUI_EMBED_FIELD_VALUE)
        return embed
    
    async def __new__(cls, client, target_message, channel_or_event, guild, message = None):
        try:
            old_gui = AUTO_REACT_ROLE_GUIS.pop(target_message)
        except KeyError:
            manager = client.events.reaction_add.get_waiter(target_message, AutoReactRoleManager, by_type = True, is_method=True)
            changes = AutoReactRoleChange(manager, channel_or_event.guild)
        else:
            await old_gui.cancel()
            manager = old_gui.manager
            changes = old_gui.changes
            changes.guild = channel_or_event.guild
        
        self = object.__new__(cls)
        self.target_message = target_message
        self.guild = guild
        self.manager = manager
        self.changes = changes
        self.message = None
        self.client = client
        
        try:
            embed = self.render()
            if message is None:
                if isinstance(channel_or_event, ChannelBase):
                    message = await client.message_create(channel_or_event, embed=embed)
                else:
                    if channel_or_event._response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
                        await client.interaction_response_message_create(channel_or_event)
                    
                    message = await client.interaction_followup_message_create(channel_or_event, embed=embed)
            else:
                await client.message_edit(message, embed=embed)
        except BaseException as err:
            if isinstance(err,ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.__new__', err)
            return
        
        self.message = message
        
        client.command_processer.append(message.channel, self)
        AUTO_REACT_ROLE_GUIS[target_message] = self
        return self
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
            ' client=',
            repr(self.client),
            ', changes=',
            repr(self.changes),
            ', target_message=',
            repr(self.target_message),
            ', manager=',
            repr(self.manager),
            '>',
                ]
        
        return ''.join(result)
    
    async def __call__(self, client, message):
        if message.author.is_bot:
            return
        
        if not self.guild.permissions_for(message.author).can_administrator:
            return
        
        parsed = SUB_COMMAND_RP.fullmatch(message.content)
        if parsed is None:
            return
        
        name, content = parsed.groups()
        if not name.islower():
            name = name.lower()
        
        if name == 'apply':
            await self.delete_message(message)
            await self.apply(message)
            return
        
        if name == 'cancel':
            await self.cancel()
            return
        
        if name == 'destroy':
            await self.destroy()
            return
        
        if content is None:
            return
        
        if name == 'add':
            await self.sub_add(client, message, content)
            return
        
        if name == 'del':
            await self.sub_del(client, message, content)
            return
        
        if name == 'behaviour':
            await self.sub_behaviour(message, content)
            return
    
    async def apply(self, message):
        try:
            del AUTO_REACT_ROLE_GUIS[self.target_message]
        except KeyError:
            pass
        
        client = self.client
        client.command_processer.remove(self.message.channel, self)
        
        while True:
            try:
                await client.message_delete(self.message)
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    break
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        break
                    
                    if err.code == ERROR_CODES.missing_access: # client removed
                        return
                
                await client.events.error(client,f'{self!r}.apply',err)
                return
            
            break
        
        changes = self.changes
        if changes.changed():
            manager = self.manager
            if manager is None:
                await AutoReactRoleManager(client, self.target_message, self.guild, changes)
            else:
                await manager.apply_changes(changes)
        
        await self.delete_message(message)
    
    async def cancel(self):
        try:
            del AUTO_REACT_ROLE_GUIS[self.target_message]
        except KeyError:
            pass
        
        client = self.client
        client.command_processer.remove(self.message.channel, self)
        
        try:
            await client.message_delete(self.message)
        except BaseException as err:
            if isinstance(err,ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.cancel', err)
            return
    
    async def destroy(self):
        await self.cancel()
        manager = self.manager
        if manager is None:
            return
        
        await manager.destroy()
    
    @ContentParser(is_method=True)
    async def sub_add(self, client, message, emoji: Emoji, role: ROLE_CONVERTER):
        if not client.can_use_emoji(emoji):
            return
        
        guild = role.guild
        if guild is None:
            return
        
        if (guild is not self.guild) and ((not guild.permissions_for(message.author).can_administrator) or
                                          (not guild.cached_permissions_for(client).can_manage_roles)):
            return
        
        if self.guild not in client.guild_profiles:
            return
        
        if not client.has_higher_role_than(role):
            return
        
        if not self.changes.add(emoji, role):
            return
        
        await self.update()
        await self.delete_message(message)
    
    @ContentParser(is_method=True)
    async def sub_del(self, client, message, emoji: Emoji = None, role: ROLE_CONVERTER = None):
        if emoji is None:
            if role is None:
                return
            else:
                object_ = role
        else:
            if role is None:
                object_ = emoji
            else:
                return
        
        if not self.changes.remove(object_):
            return
        
        await self.update()
        await self.delete_message(message)
    
    async def sub_behaviour(self, message, content):
        
        parsed = SUB_BEHAVIOUR_RP.match(content)
        if parsed is None:
            return
        
        state, type_ = parsed.groups()
        if state is None:
            state = True
        else:
            if not state.islower():
                state = state.lower()
            
            if not type_.islower():
                type_ = type_.lower()
            
            if state == 'enable':
                state = True
            else:
                state = False
        
        if type_ == 'role':
            type_ = 'remove_role_if_emoji'
        else:
            type_ = 'remove_emoji_if_role'
        
        if not self.changes.update_behaviour({type_:state}):
            return
        
        await self.update()
        await self.delete_message(message)
    
    async def update(self):
        client = self.client
        try:
            await client.message_edit(self.message, embed=self.render())
        except BaseException as err:
            client.command_processer.remove(self.message.channel, self)
            
            if isinstance(err,ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client,f'{self!r}.update',err)
            return
    
    async def delete_message(self, message):
        client = self.client
        try:
            await client.message_delete(message)
        except BaseException as err:
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.missing_permissions: # permissions changed meanwhile
                return
            
            client.command_processer.remove(self.message.channel, self)
            
            if isinstance(err,ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client,f'{self!r}.delete_message',err)
            return

class AutoReactRoleManager:
    __slots__ = ('message', 'relations', 'behaviour', 'guild', 'client', 'destroy_called')
    async def __new__(cls, client, message, guild, changes):
        unused_emojis = set(message.reactions.keys())
        used_emojis = {item[0] for item in changes.added}
        unused_emojis -= used_emojis
        
        for emoji in unused_emojis:
            try:
                await client.reaction_delete_emoji(message, emoji)
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        return
                
                await client.events.error(client,f'{cls.__name__}.__new__',err)
                return
        
        for emoji in used_emojis:
            try:
                await client.reaction_add(message, emoji)
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_emoji, # emoji deleted
                            ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        return
                
                await client.events.error(client, f'{cls.__name__}.__new__', err)
                return
        
        data = bytearray(320)
        position = 0
        
        relations = {}
        
        for emoji, role in changes.added:
            data[position:position+8] = emoji.id.to_bytes(8, byteorder='big')
            position +=8
            data[position:position+8] = role.id.to_bytes(8, byteorder='big')
            position +=8

            relations[emoji] = role
            relations[role] = emoji
        
        async with DB_ENGINE.connect() as connector:
            await connector.execute(AUTO_REACT_ROLE_TABLE.insert().values(
                message_id  = message.id,
                channel_id  = message.channel.id,
                data        = data,
                behaviour   = changes.new_behaviour,
                client_id   = client.id))
        
        self = object.__new__(cls)
        self.message = message
        self.relations = relations
        self.behaviour = changes.new_behaviour
        self.guild = guild
        self.client = client
        self.destroy_called = False
        self.add_events()
        return self
    
    @classmethod
    async def from_query(cls, query, connector):
        channel_id = query.channel_id
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            await connector.execute(AUTO_REACT_ROLE_TABLE.delete().where(
                auto_react_role_model.id == query.id))
            return
        
        guild = channel.guild
        if guild is None:
            await connector.execute(AUTO_REACT_ROLE_TABLE.delete().where(
                auto_react_role_model.id == query.id))
            return
        
        try:
            client = CLIENTS[query.client_id]
        except KeyError:
            return
        
        message_id = query.message_id
        try:
            while True:
                try:
                    message = await client.message_get(channel, message_id)
                except ConnectionError:
                    pass
                except DiscordException as err:
                    if err.status < 500:
                        raise
                else:
                    break
                
                await sleep(2.5, KOKORO)
                continue
        
        except BaseException as err:
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                            ):
                    await connector.execute(AUTO_REACT_ROLE_TABLE.delete().where(
                        auto_react_role_model.id == query.id))
                    return
            
            await client.events.error(client,f'{cls.__name__}.from_query',err)
            return
        
        relations = {}
        re_do = False
        data = query.data
        for position in range(0, 320, 16):
            emoji_id = int.from_bytes(data[position:position+8], byteorder='big')
            
            if emoji_id == 0:
                break
            
            try:
                emoji = EMOJIS[emoji_id]
            except KeyError:
                re_do = True
                continue
            
            role_id = int.from_bytes(data[position+8:position+16], byteorder='big')
            
            try:
                role = ROLES[role_id]
            except KeyError:
                re_do = True
                continue
            
            relations[emoji]=role
        
        if re_do:
            if relations:
                data = bytearray(320)
                position = 0
                for emoji, role in relations.items():
                    data[position:position+8]=emoji.id.to_bytes(8, byteorder='big')
                    position +=8
                    data[position:position+8]=role.id.to_bytes(8, byteorder='big')
                    position +=8
                
                await connector.execute(AUTO_REACT_ROLE_TABLE.update().values(
                    data  = data,
                        ).where(auto_react_role_model.id==query.id))
            else:
                await connector.execute(AUTO_REACT_ROLE_TABLE.delete().where(
                    auto_react_role_model.id == query.id))
                return
        
        behaviour = BehaviourFlag(query.behaviour)
        
        self = object.__new__(cls)
        self.message = message
        self.guild = message.guild
        self.relations = relations
        self.behaviour = BehaviourFlag(behaviour)
        self.client = client
        self.destroy_called = False
        self.add_events()
        return self
    
    def add_events(self):
        client = self.client
        message = self.message
        client.events.reaction_add.append(message, self.action_on_reaction_add)
        client.events.reaction_delete.append(message, self.action_on_reaction_delete)
        client.events.message_delete.append(message, self.action_on_message_delete)
        client.events.channel_delete.append(message.channel, self.action_on_channel_delete)
        guild = self.guild
        client.events.guild_delete.append(guild, self.action_on_guild_delete)
        client.events.emoji_delete.append(guild, self.action_on_emoji_delete)
        client.events.role_delete.append(guild, self.action_on_role_delete)
        client.events.role_edit.append(guild, self.action_on_role_edit)
    
    async def action_on_reaction_add(self, client, event):
        try:
            role = self.relations[event.emoji]
        except KeyError:
            return
        
        guild = role.guild
        if guild is None:
            return
        
        try:
            user_profile = event.user.guild_profiles[guild]
        except KeyError:
            return
        
        roles = user_profile.roles
        if (roles is not None) and (role in roles):
            return
        
        try:
            await client.user_role_add(event.user, role)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_user, #user deleted
                        ERROR_CODES.unknown_role, # role deleted
                        ERROR_CODES.unknown_guild, # guild deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.missing_access, # client removed
                            ):
                    #handled by other methods
                    return
            
            await client.events.error(client, f'{self!r}.action_on_reaction_add', err)
            return
    
    async def action_on_reaction_delete(self, client, event):
        try:
            role = self.relations[event.emoji]
        except KeyError:
            return
        
        guild = role.guild
        if guild is None:
            return
        
        try:
            user_profile = event.user.guild_profiles[guild]
        except KeyError:
            return
        
        roles = user_profile.roles
        if (roles is None) or (role not in roles):
            return
        
        try:
            await client.user_role_delete(event.user, role)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_user, #user deleted
                        ERROR_CODES.unknown_role, # role deleted
                        ERROR_CODES.unknown_guild, # guild deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.missing_access, # client removed
                            ):
                    #handled by other events
                    return
            
            await client.events.error(client, f'{self!r}.action_on_reaction_delete', err)
            return
    
    async def action_on_guild_delete(self, client, guild, profile):
        await self.destroy()
    
    async def action_on_message_delete(self, client, message):
        await self.destroy()
    
    async def action_on_channel_delete(self, client, channel, guild):
        await self.destroy()
    
    async def action_on_emoji_delete(self, client, emoji, guild):
        relations = self.relations
        try:
            role = relations.pop(emoji)
        except KeyError:
            return
        
        del relations[role]
        if relations:
            await self.update()
        else:
            await self.destroy()
        
        if not self.behaviour.remove_role_if_emoji:
            return
        
        guild = self.guild
        
        try:
            profile = client.guild_profiles[guild]
        except KeyError:
            await self.destroy()
            return
        
        if not guild.cached_permissions_for(client).can_manage_roles:
            return
        
        if not client.has_higher_role_than(role):
            return
        
        try:
            await client.role_delete(role)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.status >= 500:
                    return
                
                if err.code in (
                        ERROR_CODES.unknown_role, # role deleted
                        ERROR_CODES.unknown_guild, # guild deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client,f'{self!r}.action_on_emoji_delete',err)
            return
    
    async def action_on_role_delete(self, client, role, guild):
        relations = self.relations
        try:
            emoji = relations.pop(role)
        except KeyError:
            return
        
        del relations[emoji]
        if relations:
            await self.destroy()
        else:
            await self.update()
        
        if not self.behaviour.remove_emoji_if_role:
            return
        
        if emoji.is_unicode_emoji():
            return
        
        if not self.guild.cached_permissions_for(client).can_manage_roles:
            return
        
        try:
            await client.emoji_delete(emoji)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.status >= 500:
                    return
                
                if err.code in (
                        ERROR_CODES.unknown_emoji, # emoji deleted
                        ERROR_CODES.unknown_guild, # guild deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client,f'{self!r}.action_on_role_delete',err)
            return
    
    async def action_on_role_edit(self, client, role, old):
        relations = self.relations
        if role not in relations:
            return
        
        if client.has_higher_role_than(role):
            return
        
        emoji = relations.pop(role)
        
        del relations[emoji]
        if relations:
            await self.destroy()
        else:
            await self.update()
        
    async def apply_changes(self, changes):
        self.behaviour = changes.new_behaviour
        
        client = self.client
        message = self.message
        relations = self.relations
        removed = changes.removed
        
        for emoji, role in changes.removed:
            del relations[emoji]
            del relations[role]
        
        unused_emojis = set(message.reactions.keys())
        for item in changes.actual:
            try:
                unused_emojis.remove(item[0])
            except KeyError:
                pass
        
        for item in changes.added:
            try:
                unused_emojis.remove(item[0])
            except KeyError:
                pass
        
        for emoji in unused_emojis:
            try:
                await client.reaction_delete_emoji(message, emoji)
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        await self.destroy()
                        return
                
                await client.events.error(client, f'{self!r}.apply_changes', err)
                return
        
        for emoji, role in changes.added:
            if emoji.guild is None:
                continue
            
            if role.guild is None:
                continue
            
            relations[emoji] = role
            relations[role] = emoji
            try:
                await client.reaction_add(message, emoji)
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_emoji, # emoji deleted
                            ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        
                        await self.destroy()
                        return
                
                await client.events.error(client,f'{self!r}.apply_changes',err)
                return
        
        await self.update()
    
    async def update(self):
        data = bytearray(320)
        position = 0
        for emoji, role in self.relations.items():
            data[position:position+8] = emoji.id.to_bytes(8, byteorder='big')
            position +=8
            data[position:position+8] = role.id.to_bytes(8, byteorder='big')
            position +=8
        
        async with DB_ENGINE.connect() as connector:
            await connector.execute(AUTO_REACT_ROLE_TABLE.update().values(
                data = data,
                behaviour = self.behaviour,
                    ).where(auto_react_role_model.message_id==self.message.id))
    
    async def destroy(self):
        if self.destroy_called:
            return
        
        self.destroy_called = True
        
        client=self.client
        message = self.message
        client.events.reaction_add.remove(message, self.action_on_reaction_add)
        client.events.reaction_delete.remove(message, self.action_on_reaction_delete)
        client.events.message_delete.remove(message, self.action_on_message_delete)
        client.events.channel_delete.remove(message.channel, self.action_on_channel_delete)
        guild = self.guild
        client.events.guild_delete.remove(guild, self.action_on_guild_delete)
        client.events.emoji_delete.remove(guild, self.action_on_emoji_delete)
        client.events.role_delete.remove(guild, self.action_on_role_delete)
        client.events.role_edit.remove(guild, self.action_on_role_edit)
        
        async with DB_ENGINE.connect() as connector:
            await connector.execute(AUTO_REACT_ROLE_TABLE.delete().where(
                auto_react_role_model.message_id == self.message.id))

class load_auto_react_roles:
    called = 0
    
    async def __call__(self, client):
        called = self.called+1
        type(self).called = called
        if called != len(CLIENTS):
            return
        
        async with DB_ENGINE.connect() as connector:
            result = await connector.execute(AUTO_REACT_ROLE_TABLE.select())
            async with ScarletExecutor() as scarlet:
                async for query in result:
                    await scarlet.add(AutoReactRoleManager.from_query(query, connector))

ClientWrapper().events(load_auto_react_roles, name='ready')

async def auto_react_roles_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('show-auto-react-roles', (
        'Starts an auto react role GUI on the specified message.\n'
        'If the message has active auto react role on it, will display that, and if it has active GUI too, will cancel '
        'that.\n'
        f'Usage: `{prefix}auto-react-roles *channel* <message_id>`'
            ), color=AUTO_REACT_ROLE_COLOR).add_footer(
                'Guild only! You must have administrator permission to use this command.')


AUTO_REACT_ROLE.interactions(name='show')
async def show_auto_react_roles(client, event):
    """Lists the currently active `auto-react-roles` in the guild. (Admin only)"""
    guild = event.guild
    if guild is None:
        abort('Guild only command!')
    
    if guild not in client.guild_profiles:
        abort('I must be in the guild to execute this command.')
    
    if not guild.permissions_for(event.user).can_administrator:
        abort('You must have `administrator` permission to invoke this command.')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        abort('I require `send messages` and `add reactions` permissions to execute this command.')
    
    managers = client.events.guild_delete.get_waiters(guild, AutoReactRoleManager, by_type=True, is_method=True)
    
    embed = Embed(f'Auto role managers for: {guild}', color=AUTO_REACT_ROLE_COLOR)
    if not managers:
        embed.description = '*none*'
        await Closer(client, event, embed)
        return
    
    results = []
    for manager in managers:
        message = manager.message
        title = f'{message.channel:m} {message.id}'
        results.append((title, manager),)
    
    await ChooseMenu(client, event, results, select_auto_react_role_gui, embed=embed, prefix='¤')

async def select_auto_react_role_gui(client, channel_or_event, message, title, manager):
    guild = manager.message.channel.guild
    if manager.destroy_called or (guild is None):
        embed = Embed('The selected entity was already destroyed', color=AUTO_REACT_ROLE_COLOR)
        if isinstance(channel_or_event, ChannelBase):
            await client.message_create(channel_or_event, embed=embed)
        else:
            response_state = channel_or_event._response_state
            
            if response_state == INTERACTION_EVENT_RESPONSE_STATE_NONE:
                await client.interaction_response_message_create(channel_or_event, embed=embed)
            elif response_state == INTERACTION_EVENT_RESPONSE_STATE_DEFERRED:
                await client.interaction_response_message_edit(channel_or_event, embed=embed)
            else:
                await client.interaction_followup_message_create(channel_or_event, embed=embed)
        
        return
    
    await AutoReactRoleGUI(client, manager.message, channel_or_event, guild, message=message)
