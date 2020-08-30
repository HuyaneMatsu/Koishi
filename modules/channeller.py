# -*- coding: utf-8 -*-
from hata import Task, Client, User, CHANNELS, Embed, eventlist, Color

from hata.ext.commands import checks, Command

CHANNELLER_COMMANDS=eventlist(type_=Command)
CHANNELLER_COLOR = Color.from_rgb(129, 158, 0)

def setup(lib):
    Koishi.commands.extend(CHANNELLER_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(CHANNELLER_COMMANDS)
    
class Channeller_v_del(object):
    __slots__=('parent')
    def __init__(self,parent):
        self.parent=parent

    async def __call__(self,client,message):
        if type(message.author) not in (Client,User):
            return

        source_channel=message.channel
        user=message.author
        
        content     = message.clean_content
        embed       = message.clean_embeds
        file        = None if message.attachments is None else [attachment.name for attachment in message.attachments]
        tts         = message.tts
        #avatar_url  = message.author.avatar_url #cannot compare avatar urls.
        
        for channel,webhook in self.parent.pairs:
            if channel is source_channel:
                continue
        
            for message in channel.messages:
                if type(message.author) in (Client,User):
                    continue
                if (user.name_at(webhook.guild) != message.author.name or
                    #avatar_url  != message.author.avatar_url or \
                    content     != message.clean_content or
                    file        != (None if message.attachments is None else [attachment.name for attachment in message.attachments]) or \
                    embed       != message.clean_embeds or
                    tts         != message.tts
                        ):
                    
                    continue
                Task(client.message_delete(message),client.loop)
                break
                    
class Channeller(object):
    __slots__=('client', 'deleter', 'pairs')
    def __init__(self,client,pairs):
        self.client=client
        self.pairs=pairs
        self.deleter=deleter=Channeller_v_del(self)
        
        event_1=client.events.message_create
        event_2=client.events.message_delete
        for pair in pairs:
            channel=pair[0]
            channel.message_keep_limit=30 #if caching is diabled we turn this on
            event_1.append(channel, self)
            event_2.append(channel, deleter)
            CHANNELINGS[channel.id]=self

    def cancel(self,channel):
        event_1=self.client.events.message_create
        event_2=self.client.events.message_delete
        pairs=self.pairs
        deleter=self.deleter
        if channel is None:
            pass
        elif len(pairs)<3:
            for pair in pairs:
                channel = pair[0]
                channel.message_keep_limit = channel.MESSAGE_KEEP_LIMIT
                del CHANNELINGS[channel.id]
        else:
            for index,pair in enumerate(pairs):
                if pair[0] is channel:
                    del pairs[index]
                    break
            channel.message_keep_limit = channel.MESSAGE_KEEP_LIMIT
            event_1.remove(channel, self)
            event_2.remove(channel, deleter)
            del CHANNELINGS[channel.id]
            return

        for pair in pairs:
            channel=pair[0]
            channel.message_keep_limit=channel.MESSAGE_KEEP_LIMIT
            event_1.remove(channel, self)
            event_2.remove(channel, deleter)
            
        deleter.parent=None
        self.deleter=None

    
    async def __call__(self,client,message):
        if type(message.author) not in (Client,User):
            return
        
        attachments=message.attachments
        if attachments is None:
            files=None
        else:
            files=[]
            for attachment in attachments:
                file = await client.download_attachment(attachment)
                files.append((attachment.name,file))

        source_channel=message.channel
        
        for channel,webhook in self.pairs:
            if channel is source_channel:
                continue
            Task(client.webhook_send(webhook,
                    content     = message.clean_content,
                    embed       = message.clean_embeds,
                    file        = files,
                    tts         = message.tts,
                    name        = message.author.name_at(webhook.guild),
                    avatar_url  = message.author.avatar_url,
                        ),client.loop)

CHANNELINGS={}

async def channeling_start(client,message,channel_id:int):
    channel_1=message.channel
    while True:
        permission=channel_1.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at this channel to invoke this command!'
            break

        try:
            channel_2=CHANNELS[channel_id]
        except KeyError:
            text=f'Unknown channel : {channel_id}'
            break
        
        if channel_1 is channel_2:
            text='Same channel...'
            break
        
        permission=channel_2.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at that channel to invoke this command!'
            break

        channeling_1=CHANNELINGS.get(channel_1.id,None)
        channeling_2=CHANNELINGS.get(channel_2.id,None)
        
        if channeling_1 is not None and channeling_2 is not None and channeling_1 is channeling_2:
            text='This connection is already set up'
            break

        pairs=[]
        if channeling_1 is None:
            webhooks = await client.webhook_get_channel(channel_1)
            if webhooks:
                webhook=webhooks[0]
            else:
                webhook = await client.webhook_create(channel_1,'Love You')
            pairs.append((channel_1,webhook,),)
        else:
            channeling_1.cancel(None)
            pairs.extend(channeling_1.pairs)

        if channeling_2 is None:
            webhooks = await client.webhook_get_channel(channel_2)
            if webhooks:
                webhook=webhooks[0]
            else:
                webhook = await client.webhook_create(channel_2,'Love You')
            pairs.append((channel_2,webhook,),)
        else:
            channeling_2.cancel(None)
            pairs.extend(channeling_2.pairs)


        Channeller(client,pairs)
        text=f'Channelling between `{channel_1.guild}/{channel_1}` and `{channel_2.guild}/{channel_2}`'
        break
    
    await client.message_create(channel_1,text)

async def channeling_start_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('channeling_start',(
        'I can connect more channels with my youkai powers.\n'
        f'Usage: `{prefix}channeling_start *channel_id*`\n'
        '`channel_id` must be an id of a channel, what I have access too.\n'
        'By connecting two channels, I manipulate them to cross send each '
        'message. I always connect the source channel, with the target '
        'channel to be clean. *More channels can be connected too.*\n'
        f'To cancel channelling use: `{prefix}channeling_stop`'
        ), color=CHANNELLER_COLOR).add_footer(
            'Owner only!')


async def channeling_stop(client,message,content):
    channel=message.channel
    while True:
        try:
            channeller=CHANNELINGS[channel.id]
        except KeyError:
            text='There is no active channeller at this channel'
            break

        channeller.cancel(channel)
        text='Success'
        break

    await client.message_create(channel,text)

async def channeling_stop_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('channeling_stop',(
        'Cancels the channelling of this channel.\n'
        f'Usage: `{prefix}channeling_stop`\n'
        'If more channels are connected, you need to call this command, '
        'from every of them, to cancel all.\n'
        'If only one channel is left alone, it will be cancelled automatically.'
        ), color=CHANNELLER_COLOR).add_footer(
            'Owner only!')


CHANNELLER_COMMANDS(channeling_start, description=channeling_start_description, checks=[checks.guild_only(),checks.owner_only()],category='UTILITY')
CHANNELLER_COMMANDS(channeling_stop, description=channeling_stop_description,checks=[checks.owner_only()],category='UTILITY')