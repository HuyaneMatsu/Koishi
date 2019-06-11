# -*- coding: utf-8 -*-
from hata.embed import Embed
from hata.events import pagination
from hata.color import Color
from hata.exceptions import DiscordException
from hata.futures import sleep

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
        page.add_field(f'Use {prefix}help *command* for more information.',f'page {index}/{limit}')
        result.append({'embed':page})

    return result

HELP['help']=Embed(title='rate',color=HELP_COLOR,
    description='Shows the list of the commands.'
        )

HELP['image']=Embed(title='image',color=HELP_COLOR,description='')

HELP['upload']=Embed(title='upload',color=HELP_COLOR,                           
    description=(
        'You can can upload images with tags, which you can access with the "image" command.\n'
        'On mention it will upload the mentioned\'s image.\n'
        '(Owner only!)'
            ))

HELP['rate']=Embed(title='rate',color=HELP_COLOR,
    description='Use this command to rate someone by @mentionning them.'
        )

HELP['mine']=Embed(title='mine',color=HELP_COLOR,
    description=(
        'Creates a minesweeper game.\n'
        'U can ask the result as "text" too\n'
        'Default bomb amount is 12, but you can set it between 8 and 24!'
            ))

HELP['dice']=Embed(title='dice',color=HELP_COLOR,
    description='Throws a/more dices.'
        )

HELP['ping']=Embed(title='pong',color=HELP_COLOR,
    description='Returns the client\s ping in ms'
        )


HELP['nitro']=Embed(title='emoji',color=HELP_COLOR,  
    description=(
        'Type an emoji what I can use with my nitro. If I find it, I will '
        'send it.'
            ))

HELP['voice']=Embed(title='voice',color=HELP_COLOR,
    description=(
        'Use "join (n%)" to make the bot to join your voice channel\n'
        'Use "pause" to pause the player\n'
        'Use "stop" to stop the player\n'
        'Use "resume" to resume the player\n'
        'Use "play <link or title>" to play music\n'
        'Use "volume (n%)" to get/set volume\n'
        'Use "skip" to skip the actual source\n'
        'Use "move <channel name>" to move the player to an another channel\n'
        'Use "leave" to make me leave the channel'
            ))

HELP['message_me']=Embed(title='message_me',color=HELP_COLOR,
    description='Sends you something nice'
        )


HELP['clear']=Embed(title='clear',color=HELP_COLOR,
    description='Clears the set amount of messages (default=1)'
        )

HELP['hug']=Embed(title='hug',color=HELP_COLOR,
    description='After u said the magic word hugs the choosen one'
        )

HELP['waitemoji']=Embed(title='waitemoji',color=HELP_COLOR,
    description='Waits for an emoji at the channel'
        )

HELP['subscribe']=Embed(title='subscribe',color=HELP_COLOR,
    description='Subscribes u to Announcements role, if possible'
        )

HELP['user']=Embed(title='user',color=HELP_COLOR,
    description='Shows your profile'
        )

HELP['invite']=Embed(title='ivnite',color=HELP_COLOR,
    description=(
        'Sends you an invite (only if u can create invite anyways too)\n'
        'Guild owner can create permament invite too with an additinal "perma"'
        ))

HELP['invites']=Embed(title='invites',color=HELP_COLOR,
    description='Shows the invites of the guild <channel>.'
        )

HELP['bans']=Embed(title='bans',color=HELP_COLOR,
    description='Shows the banned users at the guild'
        )

HELP['leave_guild']=Embed(title='unban',color=HELP_COLOR,
    description='Leaves the guild. Guild owner only.'
        )

HELP['guild']=Embed(title='unban',color=HELP_COLOR,
    description='Shows the guild\'s profile.'
        )

HELP['bs']=Embed(title='bs',color=HELP_COLOR,
    description='Requests a batlleship game to the mentioned user.'
        )

HELP['love']=Embed(title='love',color=HELP_COLOR,
    description='How much you two fit together?'
        )

HELP['change_prefix']=Embed(title='change_prefix',color=HELP_COLOR,
    description='Changes my prefix at the guild (guild owner only)!'
        )

HELP['kanako']=Embed(title='kanako',color=HELP_COLOR,
    description=(
        'Start a hiragana or katakana quiz!\n'
        'There can be only one game each channel.\n\n'
        '- **create <map> <amount of question> <possibilities (0, 3, 4, 5)>**\n'
        'Creates a game.\n'
        '\n'
        '- **start**\n'
        'Stats the game, Oldest user at the game only.\n'
        '\n'
        '- **join**\n'
        'Joins to the current game. Cant join if it is already started.\n'
        '\n'
        '- **leave**\n'
        'Leaves from the actual game.\n'
        '\n'
        '- **cancel**\n'
        'Cancels the current game, oldest user at the game only.\n'
        '\n'
        '- **<name>**\n'
        'Shows you every character at the map.'
            ))

HELP['se']=Embed(title='se',color=HELP_COLOR,
    description='`se` stands for `show emoji`!'
        )

HELP['nikki']=Embed(title='nikki',color=HELP_COLOR,
    description='Your personal yandere <3'
        )

HELP['ds']=Embed(title='ds',color=HELP_COLOR,
    description=(
        'Play **Dungeon sweeper** game!\n'
        'A user can have only one activate game at a time.\n'
        '\n'
        '- *nothing*\n'
        'Starts a game at this channel or moves your actual game.\n'
        '\n'
        '- **rules**\n'
        'The rules of the game desu!\n'
        '\n'
        '- **help**\n'
        'Shows you this message\n'
            ))

HELP['roles']=Embed(title='roles',color=HELP_COLOR,
    description='Show the roles of the guild.'
        )

async def on_command_help(client,message,content):
    if 0<len(content)<50:
        content=content.lower()
        try:
            result=HELP[content]
        except KeyError:
            try:
                message = await client.message_create(message.channel,embed=Embed(title=f'Invalid command: {content}',color=HELP_COLOR))
                await sleep(30.,client.loop)
                await client.message_delete(message)
            except DiscordException:
                pass
            return
        
        await client.message_create(message.channel,embed=result)
    else:
        pagination(client,message.channel,create_help_help(client.events.message_create.prefix(message)))
    
async def invalid_command(client,message,command,content):
    prefix=client.events.message_create.prefix(message)
    try:
        message = await client.message_create(message.channel,embed=Embed(title=f'Invalid command `{command}`, try using: `{prefix}help`',color=HELP_COLOR))
        await sleep(30.,client.loop)
        await client.message_delete(message)
    except DiscordException:
        pass
