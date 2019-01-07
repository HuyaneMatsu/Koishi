# -*- coding: utf-8 -*-
from pers_data import PREFIX
HELP={}

HELP['help']= ( \
    'Commands:\n'
    ' - help\n'
    ' - image\n'
    ' - rate\n'
    ' - roles\n'
    ' - dice\n'
    ' - emojis\n'
    ' - ping\n'
    ' - emoji\n'
    f'Use {PREFIX}help *command* for more information.'
        )
HELP['image']=None
HELP['rate']='Use this command to rate someone by @mentionning them.'
HELP['roles']='Lists roles fo the guild/mentioned person.'
HELP['emojis']='Lists the guild\'s emoojis'
HELP['message_details']='Loads an older message and shows it\'s deatils'
HELP['dice']='Throws a/more dices.'
HELP['ping']='Searches a user by name at the guild, and ping is'
HELP['emoji']='type an :emoji: and I will show it! (works only on emojis which u cant use on the server)'

async def on_command_help(client,message,content):
    if content:
        try:
            result=HELP[content]
        except KeyError:
            result=f'Invalid command: {content}'
    else:
        result=HELP['help']
    await client.message_create(message.channel,result)
