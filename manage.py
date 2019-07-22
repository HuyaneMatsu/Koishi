# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import Activity_game
from hata.channel import Channel_text
from hata.events import (reaction_add_waitfor,command_processer,
    reaction_delete_waitfor,)
from hata.webhook import Webhook
from hata.role import Role

import pers_data

import koishi
import mokou
import elphelt

from tools import commit_extractor,message_delete_waitfor

############################## SETUP KOISHI ##############################

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=Activity_game.create(name='with Satori'),
        )

Koishi.events(reaction_add_waitfor)
Koishi.events(reaction_delete_waitfor)
Koishi.events(message_delete_waitfor)
Koishi.events(koishi.once_on_ready)

koishi_commands=Koishi.events(command_processer(koishi.PREFIXES)).shortcut
koishi_commands.extend(koishi.commands)

webhook_sender=commit_extractor(
    Koishi,
    Channel_text.precreate(555476090382974999),
    Webhook.precreate(555476334210580508),
    role=Role.precreate(538397994421190657),
    color=0x2ad300,
        )

Koishi.events.message_create.append(webhook_sender,webhook_sender.channel)

############################## SETUP MOKOU ##############################


Mokou=Client(pers_data.MOKOU_TOKEN,
    client_id=pers_data.MOKOU_ID,
        )

Mokou.events(mokou.message_create)
Mokou.events(mokou.typing)
Mokou.events(mokou.channel_delete)


############################## SETUP ELPHELT ##############################

Elphelt=Client(pers_data.ELPHELT_TOKEN,
    client_id=pers_data.ELPHELT_ID,
               status='idle'
        )

Elphelt.events(reaction_add_waitfor)
Elphelt.events(reaction_delete_waitfor)

elphelt_commands=Elphelt.events(command_processer('/')).shortcut
elphelt_commands.extend(elphelt.commands)
elphelt_commands(Koishi.events.message_create.commands['random'])

############################## TEST COMMANDS ##############################

from hata.dereaddons_local import asyncinit
from hata.prettyprint import pchunkify
from tools import smart_join

@koishi_commands
class unknown_emojier(metaclass=asyncinit):
    __slots__=['events','client','message']
    async def __init__(self,client,message,content):
        if message.author is not client.owner:
            return
        self.client=client
        self.message=message
        message.weakrefer()
        message.channel.messages.clear()
        message.reactions.clear()
        client.events.message_create.append(self,message.channel)
        client.events.reaction_add.append(self,message)
        client.events.reaction_delete.append(self,message)
        
    def __call__(self,*args):
        if len(args)==1:
            return self._process_message(*args)
        else:
            return self.render_emojis()

    async def _process_message(self,message):
        if message.author is not self.client.owner:
            return

        content=message.content
        if len(content)>10:
            return
        
        content=content.lower()
        client=self.client
        
        if content=='cancel':
            
            client.events.message_create.remove(self,message.channel)
            client.events.reaction_add.remove(self,self.message)
            client.events.reaction_delete.remove(self,self.message)
            await client.message_create(message.channel,'cancelled')
            return

        if content=='clear':
            self.message.reactions.clear()
            await client.message_create(message.channel,'reactions \'cleared\'')
            await self.render_emojis()
            return

        if content=='load':
            await client.reaction_load_all(self.message)
            await self.render_emojis()
            return

    #await it
    def render_emojis(self):
        result=['reactions on the message:']
        reactions=self.message.reactions
        if reactions:
            for emoji,line in reactions.items():
                result.append(f'\n{emoji.name} : {len(line)}')
                if line.unknown:
                    result.append(f'\n - *{line.unknown} unknown*')
                for user in line:
                    result.append(f'\n - {user:f}')
        else:
            result.append('*none*')
        content=smart_join(result,sep='')
        return self.client.message_create(self.message.channel,content)
        
    
    
############################## START ##############################

start_clients()

##def start_console():
##    import code
##    shell = code.InteractiveConsole(globals().copy())
##    shell.interact()
    
#start_console()
