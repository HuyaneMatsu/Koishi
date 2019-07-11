from collections import deque
import re
from random import randint
from datetime import timedelta
from hata.channel import Channel_private

TYPINGS={}
class typing_counter:
    __slots__=['duration', 'timestamp', 'user']
    def __init__(self,user,timestamp):
        self.user=user
        self.timestamp=timestamp
        self.duration=8.

_MOKOU_FIRE_RP=re.compile('i|u|you|we|iam')
_MOKOU_MOKOU_RP=re.compile('mokou?')

async def message_create(client,message):
    while True:
        channel=message.channel
        if type(channel) is Channel_private:
            break
        
        user=message.author
        if user.is_bot:
            break
        
        try:
            channel_q=TYPINGS[channel.id]
        except KeyError:
            TYPINGS[channel.id]=deque()
            break
        ln=len(channel_q)
        if not ln:
            break
        
        index=0
        while True:
            element=channel_q[index]
            if element.user is user:
                del channel_q[index]
                ln-=1
            else:
                index+=1
            if index==ln:
                break
            
        break
    
    while True:
        content=message.content.lower()
        if 'show' in content and 'amount of loaded messages' in content:
            channel=message.channel
            parts=[f'Amount of loaded messages: {len(channel.messages)}.']
            if channel.message_history_reached_end:
                parts.append('The channel is fully loaded.')
            else:
                parts.append('There is even more message at this channel however.')
            if not channel.cached_permissions_for(client).can_read_message_history:
                parts.append('I have no permission to read older messages.')
            if channel.turn_GC_on_at:
                now=time.monotonic()
                if now>channel.turn_GC_on_at:
                    parts.append('The GC will check the channel at the next cycle.')
                else:
                    parts.append(f'The channel will fall under GC after {round(channel.turn_GC_on_at-now)} seconds')
            else:
                parts.append('There is no reason to run GC on this channel.')
            if channel.messages.maxlen:
                parts.append(f'The lenght of the loaded messages at this channel is limited to: {channel.messages.maxlen}')
            else:
                parts.append('The amount of messages kept from this channel is unlimited right now')
                
            text='\n'.join(parts)
            break
        else:
            if randint(0,2):
                text=''
                break
            if 'fire' in content and _MOKOU_FIRE_RP.search(content) is not None:
                text='BURN!!!'
            elif _MOKOU_MOKOU_RP.search(content) is not None:
                text='Yes, its me..'
            else:
                text=''
            break
    if text:    
        await client.message_create(message.channel,text)

async def typing(self,channel,user,timestamp):
    if type(channel) is Channel_private:
        return
    
    try:
        channel_q=TYPINGS[channel.id]
    except KeyError:
        channel_q=TYPINGS[channel.id]=deque()
        channel_q.appendleft(typing_counter(user,timestamp),)
        return
    
    index=len(channel_q)
    if not index:
        channel_q.appendleft(typing_counter(user,timestamp),)
        return
    limit=timestamp-timedelta(seconds=40)
    
    while True:
        index-=1
        if channel_q[index].timestamp<limit:
            del channel_q[index]
            if index:
                continue
            channel_q.appendleft(typing_counter(user,timestamp),)
            return
        break

    ln=len(channel_q)
    index=0
    limit=timestamp-timedelta(seconds=8)
    while True:
        element=channel_q[index]
        if element.timestamp<=limit:
            break
        
        if element.user is user:
            element.duration=(timestamp-element.timestamp).total_seconds()
            break

        index+=1
        if index==ln:
            channel_q.appendleft(typing_counter(user,timestamp),)
            return
        
    index=ln-1
    duration=0
    found=0
    while index:
        element=channel_q[index]
        if element.user is user:
            duration+=element.duration
            found+=1
            if duration>=30:
                break
        index-=1
    
    if duration<30 or found==len(channel_q):
        channel_q.appendleft(typing_counter(user,timestamp),)
        return

    channel_q.clear()
    if not randint(0,3):
        await self.message_create(channel,f'**{user.name_at(channel.guild)}** is typing...')

async def channel_delete(self,channel):
    try:
        del TYPINGS[channel.id]
    except KeyError:
        pass

del re
