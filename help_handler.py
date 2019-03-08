# -*- coding: utf-8 -*-
from pers_data import PREFIX
from hata.embed import Embed,Embed_field,Embed_footer,rendered_embed
from hata.events import pagination
from hata.color import Color
from hata.exceptions import Forbidden,HTTPException
import asyncio

HELP={}

HELP_COLOR=Color.from_html('#ffd21e')

def create_help_help(prefix):
    result=[]

    pages=[]
    part=[]
    index=0
    for name in HELP:
        if index==16:
            pages.append('\n'.join(part))
            part.clear()
            index=0
        part.append(f' **>>** {name}')
        index+=1

    pages.append('\n'.join(part))

    del part

    limit=len(pages)
    index=0
    while index<limit:
        page=Embed(title='Commands:',color=HELP_COLOR,description=pages[index])
        index+=1
        page.fields.append(Embed_field(name=f'Use {prefix}help *command* for more information.',value=f'page {index}/{limit}'))
        result.append({'embed':page})

    return result

HELP['help']=rendered_embed(Embed(title='rate',color=HELP_COLOR,
    description='Shows the list of the commands.'
        ))

HELP['image']=rendered_embed(Embed(title='image',color=HELP_COLOR,description=''))

HELP['upload']=rendered_embed(Embed(title='upload',color=HELP_COLOR,                           
    description=( \
        'You can can upload images with tags, which you can access with the "image" command.'
        'On mention it will upload the mentioned\s image.'
        '(Owner only!)'
            )))

HELP['rate']=rendered_embed(Embed(title='rate',color=HELP_COLOR,
    description='Use this command to rate someone by @mentionning them.'
        ))

HELP['mine']=rendered_embed(Embed(title='mine',color=HELP_COLOR,
    description=( \
        'Creates a minesweeper game.\n'
        'U can ask the result as "text" too\n'
        'Default bomb amount is 12, but you can set it between 8 and 24!'
            )))

HELP['dice']=rendered_embed(Embed(title='dice',color=HELP_COLOR,
    description='Throws a/more dices.'
        ))

##HELP['pong']=rendered_embed(Embed(title='ping',color=HELP_COLOR,
##    description='Searches a user by name at the guild, and pings is'
##        ))

HELP['ping']=rendered_embed(Embed(title='pong',color=HELP_COLOR,
    description='Returns the client\s ping in ms'
        ))


HELP['emoji']=rendered_embed(Embed(title='emoji',color=HELP_COLOR,  
    description=( \
        'type an :emoji: and I will show it!'
        '(works only on emojis which u cant use on the server)'
            )))

HELP['edit']=rendered_embed(Embed(title='edit',color=HELP_COLOR,  
    description= ( \
        'You can edit:\n'
        ' **>>** "user"\n'
        ' **>>** "role"\n'
        ' **>>** "emoji"\n'
        ' **>>** "guild"'
            )))

HELP['voice']=rendered_embed(Embed(title='voice',color=HELP_COLOR,
    description=( \
        'Use "join (n%)" to make the bot to join your voice channel\n'
        'Use "pause" to pause the player\n'
        'Use "stop" to stop the player\n'
        'Use "resume" to resume the player\n'
        'Use "play <link or title>" to play music\n'
        'Use "volume (n%)" to get/set volume\n'
        'Use "skip" to skip the actual source\n'
        'Use "move <channel name>" to move the player to an another channel\n'
        'Use "leave" to make me leave the channel'
            )))

HELP['move']=rendered_embed(Embed(title='move',color=HELP_COLOR,
    description='With move command you can move "role","channel" and "user" arround.'
        ))

HELP['delete']=rendered_embed(Embed(title='delete',color=HELP_COLOR,
    description=( \
        'Currently can delete:\n'
        ' **>>** "role" <name/mention>\n'
        ' **>>** "emoji" <name/emoji>'
            )))

HELP['list']=rendered_embed(Embed(title='list',color=HELP_COLOR,
    description=( \
        'Lits a specific type of object at the guild, it can be:'
        ' **>>** "roles"\n'
        ' **>>** "emojis"\n'
        ' **>>** "channels"\n'
        ' **>>** "pins"\n'
        ' **>>** "webhooks" (channel)'
            )))

HELP['details']=rendered_embed(Embed(title='details',color=HELP_COLOR,
    description=( \
        'Shows details about a specific object, it can be:\n'
        ' **>>** "message" +index'
        ' **>>** "guild"\n'
        ' **>>** "pin" + index\n'
        ' **>>** "role"\n'
        ' **>>** "channel" <> <ow> <>\n'
        ' **>>** "permission" <channel> <> <user> <>'
            )))

HELP['message_me']=rendered_embed(Embed(title='message_me',color=HELP_COLOR,
    description='Sends you something nice'
        ))

##HELP['pm']=rendered_embed(Embed(title='pm',color=HELP_COLOR,
##    description='Sends a private message to the user with the text after the line break'
##        ))

HELP['clear']=rendered_embed(Embed(title='clear',color=HELP_COLOR,
    description='Clears the set amount of messages (default=100)'
        ))

HELP['hug']=rendered_embed(Embed(title='hug',color=HELP_COLOR,
    description='After u said the magic word hugs the choosen one'
        ))

HELP['say']=rendered_embed(Embed(title='say',color=HELP_COLOR,
    description='Write something after I prepared for to say it!'
        ))

HELP['waitemoji']=rendered_embed(Embed(title='waitemoji',color=HELP_COLOR,
    description='Waits for an emoji at the channel'
        ))

HELP['create']=rendered_embed(Embed(title='create',color=HELP_COLOR,
    description=( \
        'You can create a new:\n'
        ' **>>** "role"\n'
        ' **>>** "emoji"'
            )))

HELP['subscribe']=rendered_embed(Embed(title='subscribe',color=HELP_COLOR,
    description='Subscribes u to Announcements role, if possible'
        ))

HELP['type']=rendered_embed(Embed(title='type',color=HELP_COLOR,
    description='No U, I can only read!'
        ))

HELP['user']=rendered_embed(Embed(title='user',color=HELP_COLOR,
    description='Shows your profile'
        ))

HELP['invite']=rendered_embed(Embed(title='ivnite',color=HELP_COLOR,
    description=( \
        'Sends you an invite (only if u can create invite anyways too)\n'
        'Guild owner can create permament invite too with an additinal "perma"'
        )))

HELP['invites']=rendered_embed(Embed(title='invites',color=HELP_COLOR,
    description='Shows the invites of the guild <channel>.'
        ))

HELP['invite_by_code']=rendered_embed(Embed(title='invite_by_code',color=HELP_COLOR,
    description='Returns the code\' invite'
        ))

HELP['invite_delete_by_code']=rendered_embed(Embed(title='invite_delete_by_code',color=HELP_COLOR,
    description='Deletes the code\' invite'
        ))

HELP['invite_clear']=rendered_embed(Embed(title='invite_clear',color=HELP_COLOR,
    description='Deletes every invite of the guild, might take some time'
        ))

##HELP['wait2where']=rendered_embed(Embed(title='wait2where',color=HELP_COLOR,
##    description='Waits on your answer at private and at the source channel. If you answers sends a message at the main channel.'
##        ))

HELP['prune']=rendered_embed(Embed(title='prune',color=HELP_COLOR,
    description='Use it to estimate pruned members. Using with an additional "prune" gonna exesute the prune too'
        ))

##HELP['pinner']=rendered_embed(Embed(title='pinner',color=HELP_COLOR,
##    description='Sends a message, and reaction on it can change it\'s pinned state.'
##        ))

HELP['ban']=rendered_embed(Embed(title='ban',color=HELP_COLOR,
    description='Bans the mentioned user with the reason following the name/mention.'
        ))

HELP['bans']=rendered_embed(Embed(title='bans',color=HELP_COLOR,
    description='Shows the banned users at the guild'
        ))

HELP['bans']=rendered_embed(Embed(title='ban_get_by_id',color=HELP_COLOR,
    description='Shows the banned user, with the id'
        ))

HELP['bans']=rendered_embed(Embed(title='unban',color=HELP_COLOR,
    description='Unbans the user. You can write reason after the user\'s id'
        ))

HELP['leave_guild']=rendered_embed(Embed(title='unban',color=HELP_COLOR,
    description='Leaves the guild. Guild owner only.'
        ))

HELP['guild']=rendered_embed(Embed(title='unban',color=HELP_COLOR,
    description='Shows the guild\'s profile.'
        ))

HELP['bs']=rendered_embed(Embed(title='bs',color=HELP_COLOR,
    description='Requests a batlleship game to the mentioned user.'
        ))

HELP['love']=rendered_embed(Embed(title='love',color=HELP_COLOR,
    description='How much you two fit together?'
        ))

HELP['change_prefix']=rendered_embed(Embed(title='change_prefix',color=HELP_COLOR,
    description='Changes my prefix at the guild (guild owner only)!'
        ))

async def on_command_help(client,message,content):
    if 0<len(content)<50:
        content=content.lower()
        try:
            result=HELP[content]
        except KeyError:
            try:
                message = await client.message_create(message.channel,embed=Embed(title=f'Invalid command: {content}',color=HELP_COLOR))
                await asyncio.sleep(30.,loop=client.loop)
                await client.message_delete(message)
            except (Forbidden,HTTPException):
                pass
            return
        
        await client.message_create(message.channel,embed=result)
    else:
        pagination(client,message.channel,create_help_help(client.events.message_create.prefix(message)))
    
async def invalid_command(client,message,command,content):
    prefix=client.events.message_create.prefix(message)
    try:
        message = await client.message_create(message.channel,embed=Embed(title=f'Invalid command `{command}`, try using: `{prefix}help`',color=HELP_COLOR))
        await asyncio.sleep(30.,loop=client.loop)
        await client.message_delete(message)
    except (Forbidden,HTTPException):
        pass
