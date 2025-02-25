from hata import DiscordException,  cchunkify, Status, EXTRA_EMBED_TYPES, Embed, Color, eventlist, Permission, \
    KOKORO, Client
from scarletio import Task, list_difference
from hata.discord.events.core import DEFAULT_EVENT_HANDLER, EVENT_HANDLER_NAME_TO_PARSER_NAMES
from hata.ext.slash.menus import Pagination, Closer
from types import MethodType
from hata.ext.commands_v2 import Command

DISPATCH_TESTS = eventlist(type_ = Command)
DISPATCH_COLOR = Color.from_rgb(120, 108, 128)
MAIN_CLIENT : Client

def setup(lib):
    MAIN_CLIENT.commands.extend(DISPATCH_TESTS)
    
def teardown(lib):
    MAIN_CLIENT.commands.unextend(DISPATCH_TESTS)


class dispatch_tester:
    channel = None
    old_events = {}
    
    @classmethod
    async def here(self, client, message):
        if message.channel is self.channel:
            try:
                await client.message_create(message.channel, 'Current channel removed')
            except DiscordException:
                return
            self.channel = None
        else:
            try:
                await client.message_create(
                    message.channel,
                    f'Channel set to {message.channel.name} {message.channel.id}',
                )
            except DiscordException:
                return
            self.channel = message.channel
    
    
    @classmethod
    async def switch(self, client, message, content):
        if (not (5 < len(content) < 50)):
            await switch_description(client, message)
            return
        
        if content not in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
            await client.message_create(message.channel, f'Invalid dispatcher: {content}')
            return
        
        event = getattr(self, content, None)
        if event is None:
            await client.message_create(message.channel, f'Unallowed/undefined dispatcher: {content}')
            return
        
        actual = getattr(client.events, content)
        if type(actual) is MethodType and actual.__self__ is self:
            setattr(client.events, content, DEFAULT_EVENT_HANDLER)
            await client.message_create(message.channel, 'Event removed')
        else:
            self.old_events[content] = actual
            setattr(client.events, content, event)
            await client.message_create(message.channel, 'Event set')
    
    
    @classmethod
    async def client_update(self, client, old):
        Task(KOKORO, self.old_events['client_update'](client, old))
        if self.channel is None:
            return
        
        result = []
        result.append(f'Me, {client.full_name} was edited')
        for key, value in old.items():
            result.append(f'{key} changed: {value} -> {getattr(client, key)}')
        
        try:
            await client.message_create(self.channel, '\n'.join(result))
        except DiscordException:
            self.channel = None
    
    
    @classmethod
    async def message_delete(self, client, message):
        Task(KOKORO, self.old_events['message_delete'](client, message))
        if self.channel is None:
            return
        
        text = [repr(message)]
        text.insert(0, f'Message {message.id} got deleted')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def message_update(self, client, message, old):
        Task(KOKORO, self.old_events['message_update'](client, message, old))
        if self.channel is None:
            return
        
        result = [f'Message {message.id} was edited']
        
        channel = message.channel
        result.append(f'At channel : {channel:d} {channel.id}')
        guild = channel.guild
        if guild is not None:
            result.append(f'At guild : {guild.name} {guild.id}')
        
        if old is None:
            result.append('The message is uncached, cannot provide changes!')
            content = message.content
            content_length = len(content)
            result.append(f'content: (len={content_length})')
            if content_length > 500:
                content = content[:500].replace('`', '\\`')
                result.append(f'--------------------\n{content}\n... +{content_length - 500} more\n--------------------')
            else:
                content = content.replace('`', '\\`')
                result.append(f'--------------------\n{content}\n--------------------')
            
        else:
            for key, value in old.items():
                if key in ('pinned', 'activity_party_id', 'everyone_mention'):
                    result.append(f'{key} changed: {value!r} -> {getattr(message, key)!r}')
                    continue
                if key in ('edited_at',):
                    if value is None:
                        result.append(f'{key} changed: None -> {getattr(message, key):%Y.%m.%d-%H:%M:%S}')
                    else:
                        result.append(f'{key} changed: {value:%Y.%m.%d-%H:%M:%S} -> {getattr(message, key):%Y.%m.%d-%H:%M:%S}')
                    continue
                if key in ('application', 'activity', 'attachments', 'embeds'):
                    result.append(f'{key} changed:')
                    if value is None:
                        result.append('From None')
                    else:
                        result.append(repr(value))
                    value = getattr(message, key)
                    if value is None:
                        result.append('To None')
                    else:
                        result.append(repr(value))
                    continue
                if key in ('content',):
                    result.append(f'{key} changed from:')
                    content = value
                    break_ = False
                    while True:
                        content_length = len(content)
                        result.append(f'{key}: (len = {content_length})')
                        if content_length > 500:
                            content = content[:500].replace('`', '\\`')
                            result.append(f'--------------------\n{content}\n... +{content_length - 500} more\n--------------------')
                        else:
                            content = content.replace('`', '\\`')
                            result.append(f'--------------------\n{content}\n--------------------')
                        if break_:
                            break
                        break_ = True
                        content = getattr(message, key)
                        result.append('To:')
                    continue
                if key in ('mentioned_users', 'mentioned_roles', 'mentioned_channels_cross_guild'):
                    removed, added = list_difference(value, getattr(message, key))
                    if removed:
                        result.append(f'{key} removed : {len(removed)}')
                        for obj in removed:
                            result.append(f'- {obj.name} {obj.id}')
                            
                    if added:
                        result.append(f'{key} added : {len(added)}')
                        for obj in added:
                            result.append(f'- {obj.name} {obj.id}')
                        
                    continue
                
                if key in ('flags',):
                    old = list(value)
                    old.sort()
                    value = getattr(message, key)
                    new = list(value)
                    new.sort()
                    removed, added = list_difference(old,new)
                    if removed:
                        result.append(f'{key} removed : {len(removed)}')
                        for name in removed:
                            result.append(f'- {name}')
                            
                    if added:
                        result.append(f'{key} added : {len(added)}')
                        for name in added:
                            result.append(f'- {name}')
                        
                    continue
                
                # for the new stuff
                
                result.append(f'{key} changed:')
                if value is None:
                    result.append('From None')
                else:
                    result.extend(repr(value))
                
                value = getattr(message, key)
                if value is None:
                    result.append('To None')
                else:
                    result.extend(repr(value))
                
                continue
                
        text = cchunkify(result)
        pages = [Embed(description = chunk) for chunk in text]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def embed_update(self, client, message, flag):
        Task(KOKORO, self.old_events['embed_update'](client, message, flag))
        if self.channel is None:
            return
        
        result = [f'Message {message.id} got embed update:']

        channel = message.channel
        result.append(f'At channel : {channel:d} {channel.id}')
        guild = channel.guild
        if guild is not None:
            result.append(f'At guild : {guild.name} {guild.id}')
        
        if flag == 3:
            result.append('Less embeds than before???')
        else:
            if flag == 1:
                result.append('Only sizes were update.')
            elif flag == 2:
                result.append('Links! Links everywhere...')
            
            embeds = message.embeds
            if embeds is None:
                result.append('This should not happen, there are no embeds...')
            else:
                if flag == 1:
                    for index, embed in enumerate(embeds,1):
                        if flag == 1:
                            collected = []
                            image = embed.image
                            if image is not None:
                                collected.append(('image.height', image.height))
                                collected.append(('image.width', image.width))
                            thumbnail = embed.thumbnail
                            if thumbnail is not None:
                                collected.append(('thumbnail.height', thumbnail.height))
                                collected.append(('thumbnail.width', thumbnail.width))
                            video = embed.video
                            if video is not None:
                                collected.append(('video.height', video.height))
                                collected.append(('video.width', video.width))
                            if collected:
                                result.append(f'Sizes got update at embed {index}:')
                                for name, value in collected:
                                    result.append(f'- {name} : {value}')
                elif flag == 2:
                    for index, embed in enumerate(embeds,1):
                        if embed.type in EXTRA_EMBED_TYPES:
                            result.append(f'New embed appeared at index {index}:')
                            result.append(repr(embed))

        text = cchunkify(result)
        pages = [Embed(description = chunk) for chunk in text]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def reaction_clear(self, client, message, old):
        Task(KOKORO, self.old_events['reaction_clear'](client, message, old))
        if self.channel is None:
            return
        
        if old is None:
            text = []
        else:
            text = [repr(old)]
        text.insert(0, f'Reactions got cleared from message {message.id}:')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def reaction_delete_emoji(self, client, message, emoji, users):
        Task(KOKORO, self.old_events['reaction_delete_emoji'](client, message, emoji, users))
        if self.channel is None:
            return
        
        if users is None:
            text = []
        else:
            text = [repr(users)]
        text.insert(0, f'{emoji} were removed from message {message.id}:')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
        
    @classmethod
    async def user_presence_update(self, client, user, old):
        Task(KOKORO, self.old_events['user_presence_update'](client, user, old))
        if self.channel is None:
            return
        
        result = [f'Presence update on user: {user:f} {user.id}']
        try:
            statuses = old['statuses']
        except KeyError:
            pass
        else:
            for key in ('desktop', 'mobile', 'web'):
                result.append(f'{key} status: {statuses.get(key, Status.offline)} -> {user.statuses.get(key, Status.offline)}')
            
            try:
                status = old['status']
            except KeyError:
                pass
            else:
                result.append(f'status changed: {status} -> {user.status}')
        
        try:
            activities = old['activities']
        except KeyError:
            pass
        else:
            added, updated, removed = activities
            if (added is not None):
                for activity in added:
                    result.append('Added activity:')
                    result.append(repr(activity))
            
            if (updated is not None):
                for activity_change in updated:
                    result.append('Activity updated:')
                    activity = activity_change.activity
                    for key, value in activity_change.old_attributes.items():
                        result.append(f'- {key} : {value} -> {getattr(activity, key)}')
             
            if (removed is not None):
                for activity in removed:
                    result.append('Removed activity:')
                    result.append(repr(activity))
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def user_update(self, client, user, old):
        Task(KOKORO, self.old_events['user_update'](client, user, old))
        if self.channel is None:
            return
        
        result = [f'A user was updated: {user:f} {user.id}']
        for key, value in old. items():
            result.append(f'{key} : {value} -> {getattr(user, key)}')

        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def guild_user_update(self, client, user, guild, old):
        Task(KOKORO, self.old_events['guild_user_update'](client, user, old, guild))
        if self.channel is None:
            return
        
        result = [f'{user.full_name} {user.id} profile was edited at guild {guild.name!r} {guild.id}:']
        guild_profile = user.guild_profiles[guild.id]
        for key, value in old.items():
            if key in ('nick', 'boosts_since'):
                result.append(f'{key} changed: {value!r} -> {getattr(guild_profile, key)!r}')
                continue
            
            if key == 'roles':
                removed, added = list_difference(value, guild_profile.roles)
                if removed:
                    result.append(f'Roles removed: ({len(removed)})')
                    for role in removed:
                        result.append(f'- {role.name} {role.id}')
                
                if added:
                    result.append(f'Roles added: ({len(added)})')
                    for role in added:
                        result.append(f'- {role.name} {role.id}')
                continue
            
            raise RuntimeError(key)

        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def channel_delete(self, client, channel, guild):
        Task(KOKORO, self.old_events['channel_delete'](client,channel, guild))
        if self.channel is None:
            return
        
        text = f'```\nA channel was deleted: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def channel_update(self, client, channel, old):
        print(client, channel, old)
        Task(KOKORO, self.old_events['channel_update'](client, channel, old))
        if self.channel is None:
            return
        
        result = [
            f'A channel was edited: {channel.name} {channel.id}\n'
            f'channel type: {channel.__class__.__name__} ({channel.type})'
        ]
        
        for key, value in old.items():
            if key == 'overwrites':
                removed,added = list_difference(sorted(value), sorted(channel.overwrites))
                if removed:
                    result.append(f'Overwrites removed : ({len(removed)})')
                    for value in removed:
                        result.append(f'- {value.target!r} : {value.allow} {value.deny}')
                if added:
                    result.append(f'Overwrites added: ({len(added)})')
                    for value in added:
                        result.append(f'- {value.target!r} : {value.allow} {value.deny}')
                continue
            
            if key == 'region':
                other = getattr(channel, key)
                result.append(f'- {key} : {value!s} {value.value} -> {other!s} {other.value}')
                continue
            
            result.append(f'{key} changed: {value!r} -> {getattr(channel, key)!r}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def channel_create(self, client,channel):
        Task(KOKORO, self.old_events['channel_create'](client,channel))
        if self.channel is None:
            return
        
        result = [repr(channel)]
        result.insert(0, f'A channel was created: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})')
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def channel_pin_update(self, client,channel):
        Task(KOKORO, self.old_events['channel_pin_update'](client,channel))
        if self.channel is None:
            return
        
        text = f'```\nA channel\'s pins changed: {channel.name} {channel.id}\nchannel type: {channel.__class__.__name__} ({channel.type})```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def emoji_create(self, client, emoji):
        Task(KOKORO, self.old_events['emoji_create'](client, emoji))
        if self.channel is None:
            return
    
        result = [repr(emoji)]
        result.insert(0, f'Emoji created: {emoji.name} {emoji.id} at guild {emoji.guild!r}')
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def emoji_delete(self, client, emoji):
        Task(KOKORO, self.old_events['emoji_delete'](client, emoji))
        if self.channel is None:
            return
        
        result = [repr(emoji)]
        result.insert(0, f'Emoji deleted: {emoji.name} {emoji.id} at guild {emoji.guild!r}')
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
        
    @classmethod
    async def emoji_update(self, client, emoji, old):
        Task(KOKORO, self.old_events['emoji_update'](client, emoji, old))
        if self.channel is None:
            return
    
        result = []
        result.append(f'Emoji edited: {emoji.name} {emoji.id} at guild {emoji.guild!r}')
        for key, value in old.items():
            if key == 'roles':
                removed, added = list_difference(value, emoji.roles)
                
                if removed:
                    result.append(f'Removed roles: ({len(removed)})')
                    for role in removed:
                        result.append(f'- {role.name} {role.id}')
                
                if added:
                    result.append(f'Added roles: ({len(added)})')
                    for role in added:
                        result.append(f'- {role.name} {role.id}')
                
                continue
            
            result.append(f'{key}: {value} -> {getattr(emoji, key)}')
            continue
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def sticker_create(self, client, sticker):
        Task(KOKORO, self.old_events['sticker_create'](client, sticker))
        if self.channel is None:
            return
        
        embed = Embed(description = f'Sticker created: {sticker.name} {sticker.id} at guild {sticker.guild!r}')
        await Closer(client, self.channel, embed, timeout = 120.0)
    
    @classmethod
    async def sticker_delete(self, client, sticker):
        Task(KOKORO, self.old_events['sticker_delete'](client, sticker))
        if self.channel is None:
            return
        
        embed = Embed(description = f'Sticker deleted: {sticker.name} {sticker.id} at guild {sticker.guild!r}')
        await Closer(client, self.channel, embed, timeout = 120.0)
    
    @classmethod
    async def sticker_update(self, client, sticker, old):
        Task(KOKORO, self.old_events['sticker_update'](client, sticker, old))
        if self.channel is None:
            return
        
        result = []
        result.append(f'Emoji edited: {sticker.name} {sticker.id} at guild {sticker.guild!r}')
        for key, value in old.items():
            result.append(f'{key}: {value} -> {getattr(sticker, key)}')
            continue
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def guild_user_add(self, client, guild, user):
        Task(KOKORO, self.old_events['guild_user_add'](client, guild, user))
        if self.channel is None:
            return
        
        await client.message_create(
            self.channel, f'Welcome to the Guild {user:f}!\nThe guild reached {guild.user_count} members!'
        )

    @classmethod
    async def guild_user_delete(self, client, guild, user, profile):
        Task(KOKORO, self.old_events['guild_user_delete'](client, guild, user, profile))
        if self.channel is None:
            return
        
        roles = profile.roles
        if roles is None:
            role_count = 0
        else:
            role_count = len(roles)
        text = [f'Bai bai {user.full_name}! with your {role_count} roles.']
        if profile.boosts_since is not None:
            text.append('Also rip your boost :c')
        text.append(f'The guild is down to {guild.user_count} members!')
        
        await client.message_create(self.channel, '\n'.join(text))
        
    @classmethod
    async def guild_create(self, client, guild):
        Task(KOKORO, self.old_events['guild_create'](client, guild,))
        if self.channel is None:
            return
        
        result =  [repr(guild)]
        result.insert(0, f'Guild created: {guild.id}')
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    #Unknown:
    #guild_sync
    
    @classmethod
    async def guild_update(self, client, guild, old):
        
        Task(KOKORO, self.old_events['guild_update'](client, guild, old))
        if self.channel is None:
            return
        
        result = [f'A guild got edited {guild.name} {guild.id}']
        for key, value in old.items():
            if key in ('name', 'icon', 'invite_splash', 'user_count', 'afk_timeout', 'available',
                    'description', 'vanity_code', 'banner', 'max_members', 'max_presences', 'premium_tier',
                    'boost_count', 'widget_enabled', 'preferred_language', 'discovery_splash',
                    'max_voice_video_users', 'max_stage_video_users'):
                result.append(f'- {key} : {value} - > {getattr(guild, key)}')
                continue
            
            if key in ('verification_level', 'message_notification', 'mfa', 'content_filter', 'region', 'preferred_language'):
                other = getattr(guild, key)
                result.append(f'- {key} : {value!s} {value.value} -> {other!s} {other.value}')
                continue
            
            if key == 'features':
                removed, added = list_difference(value, [*guild.iter_features()])
                if removed:
                    result.append(f'Features removed: ({len(removed)}')
                    for feature in removed:
                        result.append(f'- {feature.value}')
                
                if added:
                    result.append(f'Features added: ({len(added)})')
                    for feature in added:
                        result.append(f'- {feature.value}')
                
                continue
            
            if key in ('system_channel', 'afk_channel', 'widget_channel', 'rules_channel', 'public_updates_channel'):
                other = getattr(guild, key)
                if value is None:
                    result.append(f'{key} : None -> {other.name} {other.id}')
                elif other is None:
                    result.append(f'{key} : {value.name} {value.id} -> None')
                else:
                    result.append(f'{key} : {value.name} {value.id} -> {other.name} {other.id}')
                continue
            
            if key in ('system_channel_flags',):
                old = list(value)
                old.sort()
                new = list(getattr(guild, key))
                new.sort()
                removed, added = list_difference(old,new)
                
                if removed:
                    result.append(f'{key} removed : ({len(removed)})')
                    for name in removed:
                        result.append(f' - {name}')
                
                if added:
                    result.append(f'{key} added : ({len(added)})')
                    for name in added:
                        result.append(f' - {name}')
                continue
            
            if key in ('owner',):
                other = getattr(guild, 'owner')
                result.append(f'{key} : {value.full_name} {value.id} -> {other.full_name} {other.id}')
                continue
            
            raise RuntimeError(key)

        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
        
    @classmethod
    async def guild_delete(self, client, guild, profile):
        Task(KOKORO, self.old_events['guild_delete'](client, guild, profile))
        if self.channel is None:
            return
        
        result = [repr(guild)]
        result.insert(0, f'Guild deleted {guild.id}')
        result.insert(1, f'I had {len(profile.roles)} roles there')
        result.insert(2, 'At least i did not boost' if (profile.boosts_since is None) else 'Rip by boost ahhhh...')

        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)


    @classmethod
    async def guild_ban_add(self, client, guild, user):
        Task(KOKORO, self.old_events['guild_ban_add'](client, guild, user))
        if self.channel is None:
            return
        
        text = f'```\nUser {user:f} {user.id} got banned at {guild.name} {guild.id}.```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def guild_ban_delete(self, client, guild, user):
        Task(KOKORO, self.old_events['guild_ban_delete'](client, guild, user))
        if self.channel is None:
            return
        
        text = f'```\nUser {user:f} {user.id} got Unbanned at {guild.name} {guild.id}.```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    #Auto dispatched:
    #guild_user_chunk
    #Need integration:
    #integration_update

    @classmethod
    async def role_create(self, client,role):
        Task(KOKORO, self.old_events['role_create'](client,role,))
        if self.channel is None:
            return
        
        result = [repr(role)]
        result.insert(0, f'A role got created at {role.guild.name} {role.guild.id}')
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def role_delete(self, client,role, guild):
        Task(KOKORO, self.old_events['role_delete'](client,role, guild))
        if self.channel is None:
            return
        
        text = f'```\nA role got deleted at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)

    @classmethod
    async def role_update(self, client, role, old):
        Task(KOKORO, self.old_events['role_update'](client, role, old))
        if self.channel is None:
            return
        
        result = [f'A role got edited at {role.guild.name} {role.guild.id}\nRole: {role.name} {role.id}']
        for key, value in old.items():
            if key in ('name', 'separated', 'managed', 'mentionable', 'position',):
                result.append(f'{key} : {value} -> {getattr(role, key)}')
                continue
            if key == 'color':
                result.append(f'{key} : {value.as_html} -> {role.color.as_html}')
                continue
            if key == 'permissions':
                result.append('permissions :')
                other = role.permissions
                for name, index in Permission.__shifts_ordered__:
                    old_value = (value >> index) & 1
                    new_value = (other >> index) & 1
                    if old_value != new_value:
                        result.append(f'{name} : {bool(old_value)} -> {bool(new_value)}')
                continue
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def webhook_update(self, client,channel):
        Task(KOKORO, self.old_events['webhook_update'](client,channel))
        if self.channel is None:
            return
        
        text = f'```\nwebhooks got updated at guild: {channel.name} {channel.id}```'
        pages = [Embed(description = text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def user_voice_update(self, client, voice_state, old_attributes):
        Task(KOKORO, self.old_events['user_voice_update'](client, voice_state, old_attributes))
        if self.channel is None:
            return
        
        result = []
        result.append('Voice state update')
        user = voice_state.user
        if user.partial:
            result.append(f'user : Partial user {user.id}')
        else:
            result.append(f'user : {user.full_name} ({user.id})')
        guild = voice_state.channel.guild
        if guild is not None:
            result.append(f'guild : {guild.name} ({guild.id})')
            
        result.append(f'session_id : {voice_state.session_id!r}')
        result.append('Changes:')
        for key, value in old_attributes.items():
            if key == 'channel':
                other = voice_state.channel
                result.append(f'channel : {value.name} {value.id} -> {other.name} {other.id}')
                continue
            
            result.append(f'{key} : {value} -> {getattr(voice_state, key)}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def user_voice_join(self, client, voice_state):
        Task(KOKORO, self.old_events['user_voice_join'](client, voice_state))
        if self.channel is None:
            return
        
        result = []
        result.append('User voice join')
        result.append(repr(voice_state))
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def user_voice_leave(self, client, voice_state):
        Task(KOKORO, self.old_events['user_voice_leave'](client, voice_state))
        if self.channel is None:
            return
        
        result = []
        result.append('User voice leave')
        result.append(repr(voice_state))
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
            
    @classmethod
    async def typing(self, client,channel, user,timestamp):
        Task(KOKORO, self.old_events['typing'](client,channel, user,timestamp))
        if self.channel is None:
            return
        
        result = ['Typing:']
        if user.partial:
            result.append(f'user : Partial user {user.id}')
        else:
            result.append(f'user : {user.full_name} ({user.id})')
        result.append(f'channel : {channel.name} {channel.id}')
        result.append(f'timestamp : {timestamp:%Y.%m.%d-%H:%M:%S}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(result)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def client_update_settings(self, client, old):
        Task(KOKORO, self.old_events['client_update_settings'](client, old))
        if self.channel is None:
            return
        
        result = ['The client\'s settings were updated:', '```']
        for key, value in old.items():
            result.append(f' {key} : {value!r} -> {getattr(client.settings, key)!r}')
        result.append('```')
        await client.message_create(self.channel, '\n'.join(result))
    
    @classmethod
    async def invite_create(self, client, invite):
        Task(KOKORO, self.old_events['invite_create'](client, invite))
        if self.channel is None:
            return
        
        text = [repr(invite)]
        text.insert(0, f'Invite created:')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def invite_delete(self, client,invite):
        Task(KOKORO, self.old_events['invite_delete'](client, invite))
        if self.channel is None:
            return
    
        text = [repr(invite)]
        text.insert(0, f'Invite deleted:')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def integration_create(self, client, guild, integration):
        Task(KOKORO, self.old_events['integration_create'](client, guild, integration))
        if self.channel is None:
            return
        
        text = [repr(integration)]
        text.insert(0, f'integration_create at {guild.name} ({guild.id}):')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def integration_delete(self, client, guild, integration_id, application_id):
        Task(KOKORO, self.old_events['integration_delete'](client, guild, integration_id, application_id))
        if self.channel is None:
            return
        
        text = [
            f'integration_delete at {guild.name} ({guild.id}):',
            f'- integration_id : {integration_id}',
            f'- application_id : {application_id}',
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def integration_update(self, client, guild, integration):
        Task(KOKORO, self.old_events['integration_update'](client, guild, integration))
        if self.channel is None:
            return
        
        text = [integration]
        text.insert(0, f'integration_update at {guild.name} ({guild.id}):')
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def integration_update(self, client, guild):
        Task(KOKORO, self.old_events['integration_update'](client, guild))
        if self.channel is None:
            return
        
        text = [
            f'integration_update at {guild.name} ({guild.id}):',
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    @classmethod
    async def application_command_permission_update(self, client, permission):
        Task(KOKORO, self.old_events['application_command_permission_update'](client, permission))
        if self.channel is None:
            return
        
        text = [
            f'application_command_permission_update called at {permission.guild_id}',
            f'application_command_id: {permission.application_command_id}',
            'Overwrites:'
        ]
        
        overwrites = permission.overwrites
        if (overwrites is None):
            text.append('*none*')
        else:
            for overwrite in overwrites:
                text.append(f'- {overwrite.target!r}; allow: {overwrite.allow!r}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def stage_create(self, client, stage):
        Task(KOKORO, self.old_events['stage_create'](client, stage))
        
        pages = [Embed(description = f'Stage create: {stage!r}')]
        await Pagination(client, self.channel, pages, timeout = 120.0)


    @classmethod
    async def stage_delete(self, client, stage):
        Task(KOKORO, self.old_events['stage_delete'](client, stage))
        
        pages = [Embed(description = f'Stage delete: {stage!r}')]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def stage_update(self, client, stage, old_attributes):
        Task(KOKORO, self.old_events['stage_update'](client, stage))
        
        text = [
            f'Stage: {stage.id}'
            f'At: {stage.channel.name}'
            'Was edited:'
        ]
        for attribute_name, attribute_value in old_attributes.items():
            text.append(f'`{attribute_name}` : {attribute_value!r} -> {getattr(stage, attribute_name)}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def embedded_activity_create(self, client, embedded_activity):
        Task(KOKORO, self.old_events['embedded_activity_create'](client, embedded_activity))
        if self.channel is None:
            return
        
        text = [
            f'Embedded activity created',
            f'guild_id: {embedded_activity.guild_id!r}',
            f'channel_id: {embedded_activity.guild_id!r}',
            f'activity: {embedded_activity.activity!r}'
            f'users: {", ".join(user.full_name for user in embedded_activity.users)}',
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def embedded_activity_update(self, client, embedded_activity, old_attributes):
        Task(KOKORO, self.old_events['embedded_activity_update'](client, embedded_activity, old_attributes))
        if self.channel is None:
            return
        
        text = [
            f'Embedded activity updated',
            f'guild_id: {embedded_activity.guild_id!r}',
            f'channel_id: {embedded_activity.guild_id!r}',
            f'activity: {embedded_activity.activity!r}'
            f'users: {", ".join(user.full_name for user in embedded_activity.users)}',
            'Changes',
        ]
        
        activity = embedded_activity.activity
        for key, value in old_attributes.items():
            text.append(f'- {key} : {value} -> {getattr(activity, key)}')
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)


    @classmethod
    async def embedded_activity_delete(self, client, embedded_activity):
        Task(KOKORO, self.old_events['embedded_activity_delete'](client, embedded_activity))
        if self.channel is None:
            return
        
        text = [
            f'Embedded activity deleted',
            f'guild_id: {embedded_activity.guild_id!r}',
            f'channel_id: {embedded_activity.guild_id!r}',
            f'activity: {embedded_activity.activity!r}'
            f'users: {", ".join(user.full_name for user in embedded_activity.users)}',
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def embedded_activity_user_add(self, client, embedded_activity, user_id):
        Task(KOKORO, self.old_events['embedded_activity_user_add'](client, embedded_activity, user_id))
        if self.channel is None:
            return
        
        text = [
            f'Embedded activity user add',
            f'guild_id: {embedded_activity.guild_id!r}',
            f'channel_id: {embedded_activity.guild_id!r}',
            f'activity: {embedded_activity.activity!r}'
            f'users: {", ".join(user.full_name for user in embedded_activity.users)}',
            f'user id: {user_id!r}'
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def embedded_activity_user_delete(self, client, embedded_activity, user_id):
        Task(KOKORO, self.old_events['embedded_activity_user_delete'](client, embedded_activity, user_id))
        if self.channel is None:
            return
        
        text = [
            f'Embedded activity user delete',
            f'guild_id: {embedded_activity.guild_id!r}',
            f'channel_id: {embedded_activity.guild_id!r}',
            f'activity: {embedded_activity.activity!r}'
            f'users: {", ".join(user.full_name for user in embedded_activity.users)}',
            f'user id: {user_id!r}'
        ]
        
        pages = [Embed(description = chunk) for chunk in cchunkify(text)]
        await Pagination(client, self.channel, pages, timeout = 120.0)
    
    
    @classmethod
    async def auto_moderation_action_execution(self, client, event):
        Task(KOKORO, self.old_events['auto_moderation_action_execution'](client, event))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('auto_moderation_action_execution', repr(event)))
    
    
    @classmethod
    async def auto_moderation_rule_create(self, client, rule):
        Task(KOKORO, self.old_events['auto_moderation_rule_create'](client, rule))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('auto_moderation_rule_create', repr(rule)))

    @classmethod
    async def auto_moderation_rule_update(self, client, rule, changes):
        Task(KOKORO, self.old_events['auto_moderation_rule_update'](client, rule, changes))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('auto_moderation_rule_update', f'{rule!r}\n\n{changes!r}'))

    @classmethod
    async def auto_moderation_rule_delete(self, client, rule):
        Task(KOKORO, self.old_events['auto_moderation_rule_delete'](client, rule))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('auto_moderation_rule_delete', repr(rule)))


    @classmethod
    async def soundboard_sound_create(self, client, sound):
        Task(KOKORO, self.old_events['soundboard_sound_create'](client, sound))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('soundboard_sound_create', repr(sound)))

    @classmethod
    async def soundboard_sound_update(self, client, sound, changes):
        Task(KOKORO, self.old_events['soundboard_sound_update'](client, sound, changes))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('soundboard_sound_update', f'{sound!r}\n\n{changes!r}'))

    @classmethod
    async def soundboard_sound_delete(self, client, sound):
        Task(KOKORO, self.old_events['soundboard_sound_delete'](client, sound))
        if self.channel is None:
            return
        
        await Closer(client, self.channel, Embed('soundboard_sound_delete', repr(sound)))


async def here_description(client, message):
    prefix = await client.command_processor.get_prefix(message)
    return Embed(
        'here',
        (
            'I set the dispatch tester commands\' output to this channel.\n'
            f'Usage: `{prefix}here`\n'
            'By calling the command again, I ll remove the current channel.\n'
            'You can switch the dispatch testers, like:\n'
            f'`{prefix}switch *event_name*`\n'
            'For the event names, use:\n'
            f'`{prefix}help switch`'
        ),
        color = DISPATCH_COLOR
    ).add_footer(
        'Owner only!',
    )

async def switch_description(client, message):
    prefix = await client.command_processor.get_prefix(message)
    return Embed(
        'here',
        (
            'I can turn on a dispatch tester for you.\n'
            f'`{prefix}switch *event_name*`\n'
            'The list of defined testers:\n'
            '- `channel_create`\n'
            '- `channel_delete`\n'
            '- `channel_update`\n'
            '- `channel_pin_update`\n'
            '- `client_update_settings`\n'
            '- `client_update`\n'
            '- `embed_update`\n'
            '- `emoji_create`\n'
            '- `emoji_delete`\n'
            '- `emoji_update`\n'
            '- `guild_ban_add`\n'
            '- `guild_ban_delete`\n'
            '- `guild_create`\n'
            '- `guild_delete`\n'
            '- `guild_update`\n'
            '- `guild_user_add`\n'
            '- `guild_user_delete`\n'
            '- `invite_create`\n'
            '- `invite_delete`\n'
            '- `message_delete`\n'
            '- `message_update`\n'
            '- `reaction_clear`\n'
            '- `reaction_delete_emoji`\n'
            '- `role_create`\n'
            '- `role_delete`\n'
            '- `role_update`\n'
            '- `typing`\n'
            '- `user_update`\n'
            '- `user_presence_update`\n'
            '- `guild_user_update`\n'
            '- `user_voice_join`\n'
            '- `user_voice_leave`\n'
            '- `user_voice_update`\n'
            '- `integration_create`\n'
            '- `integration_delete`\n'
            '- `integration_update`\n'
            '- `integration_update`\n'
            '- `webhook_update`\n'
            '- `application_command_permission_update`\n'
            '- `stage_create`\n'
            '- `stage_update`\n'
            '- `stage_delete`\n'
            '- `sticker_create`\n'
            '- `sticker_delete`\n'
            '- `sticker_update`\n'
            '- `auto_moderation_action_execution`\n'
            '- `auto_moderation_rule_create`\n'
            '- `auto_moderation_rule_update`\n'
            '- `auto_moderation_rule_delete`\n'
            '- `soundboard_sound_create`\n'
            '- `soundboard_sound_delete`\n'
            '- `soundboard_sound_update`\n'
            f'For setting channel, use: `{prefix}here`'
        ),
        color = DISPATCH_COLOR
    ).add_footer(
        'Owner only!',
    )

DISPATCH_TESTS(dispatch_tester.here, description = here_description, category = 'TEST COMMANDS')
DISPATCH_TESTS(dispatch_tester.switch, description = switch_description, category = 'TEST COMMANDS')
