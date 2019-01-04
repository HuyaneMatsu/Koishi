# -*- coding: utf-8 -*-
from pers_data import PREFIX
HELP={}

HELP['help']=f'Commands:\n - help\n - image\n - rate\n Use {PREFIX}help *command* for more information.'
HELP['image']=None
HELP['rate']='Use this command to rate someone by @mentionning them.'


async def on_command_help(client,message,content):
    if content:
        try:
            result=HELP[content]
        except KeyError:
            result=f'Invalid command: {content}'
    else:
        result=HELP['help']
    await client.message_create(message.channel,result)
