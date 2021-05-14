# -*- coding: utf-8 -*-
from hata import Task, User, CHANNELS, Embed, Client, Color, WebhookType, KOKORO

from hata.ext.commands import checks

CHANNELLER_COLOR = Color.from_rgb(129, 158, 0)
    
class Channeller_v_del:
    __slots__ = ('parent',)
    def __init__(self, parent):
        self.parent = parent

    async def __call__(self, client, message):
        if not isinstance(message.author, (Client, User)):
            return

        source_channel = message.channel
        user = message.author
        
        source_content = message.content
        source_embeds = message.embds
        source_attachments = message.attachments
        if source_attachments is None:
            source_attachment_names = None
        else:
            source_attachment_names = [attachment.name for attachment in source_attachments]
        source_tts = message.tts
        
        for channel, webhook in self.parent.pairs:
            if channel is source_channel:
                continue
                
            for message in channel.messages:
                if isinstance(message.author, (Client, User)):
                    continue
                
                if user.name_at(webhook.guild) != message.author.name:
                    continue
                
                if source_content != message.content:
                    continue
                
                if source_embeds != message.emebds:
                    continue
                
                attachments = message.attachments
                if attachments is None:
                    attachment_names = None
                else:
                    attachment_names = [attachment.name for attachment in attachments]
                
                if source_attachment_names != attachment_names:
                    continue
                
                if source_tts != message.tts:
                    continue
                
                Task(client.webhook_message_delete(webhook, message), KOKORO)
                break


class Channeller_v_edit:
    __slots__ = ('parent',)
    def __init__(self, parent):
        self.parent = parent
    
    async def __call__(self, client, message, old_attributes):
        if old_attributes is None:
            return
        
        source_channel = message.channel
        user = message.author
        
        edited = False
        try:
            old_content = old_attributes['content']
        except KeyError:
            old_content = message.content
        else:
            edited = True
        
        try:
            old_embeds = old_attributes['embeds']
        except KeyError:
            old_embeds = message.embeds
        else:
            edited = True
        
        if not edited:
            return
        
        new_content = message.content
        new_embeds = message.embds
        
        attachments = message.attachments
        if attachments is None:
            old_attachment_names = None
        else:
            old_attachment_names = [attachment.name for attachment in attachments]
        
        old_tts = message.tts
        
        for channel, webhook in self.parent.pairs:
            if channel is source_channel:
                continue
                
            for message in channel.messages:
                if isinstance(message.author, (Client, User)):
                    continue
                
                if user.name_at(webhook.guild) != message.author.name:
                    continue
                
                if old_content != message.content:
                    continue
                
                if old_embeds != message.emebds:
                    continue
                
                attachments = message.attachments
                if attachments is None:
                    attachment_names = None
                else:
                    attachment_names = [attachment.name for attachment in attachments]
                
                if old_attachment_names != attachment_names:
                    continue
                
                if old_tts != message.tts:
                    continue
                
                Task(client.webhook_message_edit(webhook, message, new_content, embeds=new_embeds), KOKORO)
                break


class Channeller:
    __slots__ = ('client', 'deleter', 'editer', 'pairs')
    def __init__(self, client, pairs):
        self.client = client
        self.pairs = pairs
        self.deleter = deleter = Channeller_v_del(self)
        self.editer = editer = Channeller_v_edit(self)
        
        event_1 = client.events.message_create
        event_2 = client.events.message_delete
        event_3 = client.events_message_edit
        for pair in pairs:
            channel = pair[0]
            channel.message_keep_limit=30 #if caching is disabled we turn this on
            event_1.append(channel, self)
            event_2.append(channel, deleter)
            event_3.append(channel, editer)
            CHANNELINGS[channel.id] = self
    
    def cancel(self, channel):
        client = self.client
        event_1 = client.events.message_create
        event_2 = client.events.message_delete
        event_3 = client.events_message_edit
        pairs = self.pairs
        deleter = self.deleter
        editer = self.editer
        if channel is None:
            pass
        elif len(pairs) < 3:
            for pair in pairs:
                channel = pair[0]
                channel.message_keep_limit = channel.MESSAGE_KEEP_LIMIT
                del CHANNELINGS[channel.id]
        else:
            for index, pair in enumerate(pairs):
                if pair[0] is channel:
                    del pairs[index]
                    break
            channel.message_keep_limit = channel.MESSAGE_KEEP_LIMIT
            event_1.remove(channel, self)
            event_2.remove(channel, deleter)
            event_3.remove(channel, editer)
            del CHANNELINGS[channel.id]
            return

        for pair in pairs:
            channel = pair[0]
            channel.message_keep_limit = channel.MESSAGE_KEEP_LIMIT
            event_1.remove(channel, self)
            event_2.remove(channel, deleter)
            event_3.remove(channel, editer)
        
        deleter.parent = None
        self.deleter = None

    
    async def __call__(self, client, message):
        if not isinstance(message.author, (Client, User)):
            return
        
        attachments = message.attachments
        if attachments is None:
            files = None
        else:
            files = []
            for attachment in attachments:
                file = await client.download_attachment(attachment)
                files.append((attachment.name, file))

        source_channel = message.channel
        
        for channel, webhook in self.pairs:
            if channel is source_channel:
                continue
            
            Task(client.webhook_message_create(webhook,
                    content     = message.clean_content,
                    embed       = message.clean_embeds,
                    file        = files,
                    tts         = message.tts,
                    name        = message.author.name_at(webhook.guild),
                    avatar_url  = message.author.avatar_url,
                        ),client.loop)

CHANNELINGS = {}

async def channeling_start(client, message, channel_id:int):
    channel_1 = message.channel
    while True:
        permission = channel_1.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text = 'I have no permission at this channel to invoke this command!'
            break

        try:
            channel_2 = CHANNELS[channel_id]
        except KeyError:
            text = f'Unknown channel : {channel_id}'
            break
        
        if channel_1 is channel_2:
            text = 'Same channel...'
            break
        
        permission = channel_2.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at that channel to invoke this command!'
            break
        
        channeling_1 = CHANNELINGS.get(channel_1.id,None)
        channeling_2 = CHANNELINGS.get(channel_2.id,None)
        
        if channeling_1 is not None and channeling_2 is not None and channeling_1 is channeling_2:
            text = 'This connection is already set up'
            break
        
        pairs = []
        if channeling_1 is None:
            webhooks = await client.webhook_get_all_channel(channel_1)
            for webhook in webhooks:
                if webhook.type is WebhookType.bot:
                    break
            else:
                webhook = await client.webhook_create(channel_1, 'Love You')
            pairs.append((channel_1,webhook,),)
        else:
            channeling_1.cancel(None)
            pairs.extend(channeling_1.pairs)
        
        if channeling_2 is None:
            webhooks = await client.webhook_get_all_channel(channel_2)
            for webhook in webhooks:
                if webhook.type is WebhookType.bot:
                    break
            else:
                webhook = await client.webhook_create(channel_2, 'Love You')
            pairs.append((channel_2, webhook,),)
        else:
            channeling_2.cancel(None)
            pairs.extend(channeling_2.pairs)
        
        
        Channeller(client,pairs)
        text = f'Channelling between `{channel_1.guild}/{channel_1}` and `{channel_2.guild}/{channel_2}`'
        break
    
    await client.message_create(channel_1, text)

async def channeling_start_description(client,message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('channeling_start', (
        'I can connect more channels with my youkai powers.\n'
        f'Usage: `{prefix}channeling_start *channel_id*`\n'
        '`channel_id` must be an id of a channel, what I have access too.\n'
        'By connecting two channels, I manipulate them to cross send each '
        'message. I always connect the source channel, with the target '
        'channel to be clean. *More channels can be connected too.*\n'
        f'To cancel channelling use: `{prefix}channeling_stop`'
        ), color=CHANNELLER_COLOR).add_footer(
            'Owner only!')


async def channeling_stop(client, message, content):
    channel = message.channel
    while True:
        try:
            channeller = CHANNELINGS[channel.id]
        except KeyError:
            text = 'There is no active channeller at this channel'
            break
        
        channeller.cancel(channel)
        text = 'Success'
        break

    await client.message_create(channel, text)

async def channeling_stop_description(client, message):
    prefix = client.command_processor.get_prefix_for(message)
    return Embed('channeling_stop', (
        'Cancels the channelling of this channel.\n'
        f'Usage: `{prefix}channeling_stop`\n'
        'If more channels are connected, you need to call this command, '
        'from every of them, to cancel all.\n'
        'If only one channel is left alone, it will be cancelled automatically.'
        ), color=CHANNELLER_COLOR).add_footer(
            'Owner only!')

COMMAND_CLIENT: Client
COMMAND_CLIENT.commands(channeling_start,
    description = channeling_start_description,
    checks = [checks.guild_only(), checks.owner_only()],
    category = 'UTILITY')

COMMAND_CLIENT.commands(channeling_stop,
    description = channeling_stop_description,
    checks = [checks.owner_only()],
    category = 'UTILITY')
