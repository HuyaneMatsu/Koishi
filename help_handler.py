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
    ' - upload\n'
    ' - emoji\n'
    ' - move\n'
    ' - edit\n'
    ' - delete\n'
    f'Use {PREFIX}help *command* for more information.'
        )
HELP['image']=''
HELP['rate']='Use this command to rate someone by @mentionning them.'
HELP['roles']='Lists roles fo the guild/mentioned person.'
HELP['emojis']='Lists the guild\'s emoojis'
HELP['message_details']='Loads an older message and shows it\'s deatils'
HELP['dice']='Throws a/more dices.'
HELP['ping']='Searches a user by name at the guild, and ping is'
HELP['emoji']='type an :emoji: and I will show it! (works only on emojis which u cant use on the server)'
HELP['edit']='With edit command u can edit "user", "role".'
HELP['upload']='You can can upload images with tags, which u can access with the "image" command. On mention it will upload the mentioned\s image. (Supreme leader only!)'
HELP['voice']=( \
    'Use "join (n%)" to make the bot to join your voice channel\n'
    'Use "pause" to pause the player\n'
    'Use "stop" to stop the player\n'
    'Use "resume" to resume the player\n'
    'Use "play <link or title>" to play music\n'
    'Use "volume (n%)" to get/set volume\n'
    'Use "skip" to skip the actual source\n'
    'Use "move <channel name>" to move the player to an another channel'
        )
HELP['move']='With move command you can move "role" and "channel" arround.'
HELP['delete']='With delete command you can delete "role" objects.'

async def on_command_help(client,message,content):
    if content:
        try:
            result=HELP[content]
        except KeyError:
            result=f'Invalid command: {content}'
    else:
        result=HELP['help']
    await client.message_create(message.channel,result)
