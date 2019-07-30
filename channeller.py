from hata.futures import Task
from hata.events_compiler import content_parser
from hata.client import Client
from hata.user import User

class Channeller_v_del:
    __slots__=['parent']
    def __init__(self,parent):
        self.parent=parent

    async def __call__(self,message):
        nonwebhook=(Client,User)
        if type(message.author) not in nonwebhook:
            return

        client=self.parent.client
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
                if type(message.author) in nonwebhook:
                    continue
                if (user.name_at(webhook.guild) != message.author.name or \
                    #avatar_url  != message.author.avatar_url or \
                    content     != message.clean_content or \
                    file        != (None if message.attachments is None else [attachment.name for attachment in message.attachments]) or \
                    embed       != message.clean_embeds or \
                    tts         != message.tts \
                        ):
                    
                    continue
                Task(client.message_delete(message),client.loop)
                break
                    
class Channeller():
    __slots__=['client', 'deleter', 'pairs']
    def __init__(self,client,pairs):
        self.client=client
        self.pairs=pairs
        self.deleter=deleter=Channeller_v_del(self)
        
        event_1=client.events.message_create
        event_2=client.events.message_delete
        for pair in pairs:
            channel=pair[0]
            channel.mc_gc_limit=30 #if caching is diabled we turn this on
            event_1.append(self,channel)
            event_2.append(deleter,channel)
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
                channel.mc_gc_limit = channel.MC_GC_LIMIT
                del CHANNELINGS[channel.id]
        else:
            for index,pair in enumerate(pairs):
                if pair[0] is channel:
                    del pairs[index]
                    break
            channel.mc_gc_limit = channel.MC_GC_LIMIT
            event_1.remove(self,channel)
            event_2.remove(deleter,channel)
            del CHANNELINGS[channel.id]
            return

        for pair in pairs:
            channel=pair[0]
            channel.mc_gc_limit=channel.MC_GC_LIMIT
            event_1.remove(self,channel)
            event_2.remove(deleter,channel)
            
        deleter.parent=None
        self.deleter=None

    
    async def __call__(self,message):
        if type(message.author) not in (Client,User):
            return

        client=self.client
        
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

@content_parser('condition, flags=r, default="not client.is_owner(message.author)"',
                'int, flags="g"',)
async def channeling_start(client,message,channel_id):
    channel_1=message.channel
    while True:
        permission=channel_1.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at this channel to invoke this command!'
            break

        try:
            channel_2=client.channels[channel_id]
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
    
async def channeling_stop(client,message,content):
    if client.is_owner(message.author):
        return
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

del content_parser
