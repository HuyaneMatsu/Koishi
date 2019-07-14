# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import Activity_game
from hata.channel import Channel_text
from hata.events import (bot_reaction_waitfor,bot_message_event,
    bot_reaction_delete_waitfor,)
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

Koishi.events(bot_reaction_waitfor)
Koishi.events(bot_reaction_delete_waitfor)
Koishi.events(message_delete_waitfor)
Koishi.events(koishi.once_on_ready)
Koishi.events(koishi.guild_user_add)

koishi_commands=Koishi.events(bot_message_event(koishi.PREFIXES)).shortcut
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
        )

Elphelt.events(bot_reaction_waitfor)
Elphelt.events(bot_reaction_delete_waitfor)

elphelt_commands=Elphelt.events(bot_message_event('/')).shortcut
elphelt_commands.extend(elphelt.commands)

############################## TEST COMMANDS ##############################

from hata.guild import Guild
from hata.futures import Task
dungeon=Guild.precreate(388267636661682178)
@koishi_commands
async def write_on_mokou(self,message,client):
    if self.owner is not message.author:
        return
    if message.guild is not dungeon:
        return
    Task(Mokou.message_create(message.channel,'Write on me?'),Mokou.loop)
    Mokou.loop.wakeup()

############################## START ##############################

start_clients()

##def start_console():
##    import code
##    shell = code.InteractiveConsole(globals().copy())
##    shell.interact()
    
#start_console()
