import re

from hata import Guild, eventlist, Embed, Color, Role, sleep
from hata.events import Cooldown, Pagination

from help_handler import FLAN_HELPER, FLAN_HELP_COLOR, flan_invalid_command
from tools import CooldownHandler
from chesuto import Rarity, CARDS_BY_NAME, Card

CHESUTO_GUILD   = Guild.precreate(598706074115244042)
CHESUTO_COLOR   = Color.from_rgb(73,245,73)
CARDS_ROLE      = Role.precreate(598708907816517632)
CARD_HDR_RP     = re.compile(' *(?:\*\*)? *(.+?) *(\[token\])? *(?:\(([a-z]+)\)?)? *(?:\*\*)?',re.I)

async def guild_user_add(client, guild, user):
    if guild is not CHESUTO_GUILD:
        return
    
    channel = CHESUTO_GUILD.system_channel
    if channel is None:
        return
    
    if user.is_bot:
        return
    
    await client.message_create(channel,f'Welcome to the Che-su-to~ server {user:m} ! Please introduce yourself !')

commands=eventlist()
commands(FLAN_HELPER,'help')
commands(flan_invalid_command,'invalid_command')

@commands
@Cooldown('user',30.,handler=CooldownHandler())
async def ping(client,message,content):
    await client.message_create(message.channel,f'{client.gateway.latency*1000.:.0f} ms')

async def _help_ping(client,message):
    prefix=client.events.message_create.prefix
    embed=Embed('ping',(
        'Ping - Pong?\n'
        f'Usage: `{prefix}ping`'
        ),color=FLAN_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

FLAN_HELPER.add('ping',_help_ping)

@commands
async def sync_avatar(client,message):
    if not client.is_owner(message.author):
        return
    
    avatar_url=client.application.icon_url_as(ext='png',size=4096)
    if avatar_url is None:
        await client.message_create(message.channel,'The application has no avatar set.')
        return
    
    avatar = await client.download_url(avatar_url)
    await client.client_edit(avatar=avatar)
    
    await client.message_create(message.channel,'Avatar synced.')

async def _help_sync_avatar(client,message):
    prefix=client.events.message_create.prefix
    embed=Embed('sync_avatar',(
        'Hello there Esuto!\n'
        'This is a specific command for You, to sync the bot\'s avatar with '
        'the application\'s. I know, You might struggle with updating the '
        'bot\'s avatar the other way, so I made a command for it.\n'
        'Have a nice day!\n'
        f'Usage: `{prefix}sync_avatar`'
        ),color=FLAN_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

FLAN_HELPER.add('sync_avatar',_help_sync_avatar,FLAN_HELPER.check_is_owner)

@commands
async def massadd(client,message):
    while True:
        user=message.author
        
        if client.is_owner(user):
            break
        
        try:
            profile=user.guild_profiles[CARDS_ROLE.guild]
        except KeyError:
            return
        
        if CARDS_ROLE in profile.roles:
            break
        
        return
    
    try:
        await client.message_at_index(message.channel,1000)
    except IndexError:
        pass
    
    await client.message_delete(message)
    
    messages=[]
    for message_ in message.channel.messages:
        try:
            profile=message_.author.guild_profiles[CARDS_ROLE.guild]
        except KeyError:
            continue

        if CARDS_ROLE not in profile.roles:
            continue
        
        messages.append(message_)

    new_=0
    modified_=0
    
    description_parts=[]
    for message_ in messages:
        lines=message_.content.split('\n')
        
        next_id=message_.id
        state=0 #parse header
        description_parts.clear()
        
        for line in lines:
            if line=='<:nothing:562509134654865418>':
                line=''
            
            if not line and description_parts:
                description='\n'.join(description_parts)
                description_parts.clear()
                
                if Card.update(description,next_id,name,rarity):
                    new_+=1
                    next_id+=1
                else:
                    modified_+=1
                
                state=0
                continue
            
            if state==0:
                parsed=CARD_HDR_RP.fullmatch(line)
                if parsed is None:
                    continue
                name,token,rarity=parsed.groups()
                
                if token is None:
                    token=False
                else:
                    token=True
                
                if token:
                    rarity=Rarity.token
                elif rarity is None:
                    rarity=Rarity.INSTANCES[0]
                else:
                    try:
                        rarity=Rarity.BY_NAME[rarity.title()]
                    except KeyError:
                        continue
                
                state=1 #parse description
                continue
            
            if state==1:
                description_parts.append(line)
                continue
    
        if description_parts:
            description='\n'.join(description_parts)
            description_parts.clear()
            if Card.update(description,next_id,name,rarity,token):
                new_+=1
            else:
                modified_+=1
    
    del description_parts
    
    if new_ or modified_:
        await Card.dump_cards(client.loop)
    
    message = await client.message_create(message.channel,
        embed=Embed(None,f'modified: {modified_}\nnew: {new_}',color=CHESUTO_COLOR))
    await sleep(30.,client.loop)
    await client.message_delete(message)

async def _help_massadd(client,message):
    prefix=client.events.message_create.prefix
    embed=Embed('massadd',(
        'Loads the last 100 message at the channel, and check each of them '
        'searching for card definitions. If it finds one, then updates it, if '
        'already added, or creates a new one.\n'
        f'Usage: `{prefix}massadd`'
        ),color=FLAN_HELP_COLOR).add_footer(
            f'You must have the `{CARDS_ROLE}` role to use this command.')
    await client.message_create(message.channel,embed=embed)

FLAN_HELPER.add('massadd',_help_massadd,FLAN_HELPER.check_role(CARDS_ROLE))

@commands
async def showcard(client,message,content):
    if not 2<len(content)<101:
        return
    try:
        card=CARDS_BY_NAME[content.lower()]
    except KeyError:
        return
    embed=Embed(color=CHESUTO_COLOR)
    embed.add_field('Name',card.name,inline=True)
    
    rarity=card.rarity
    if rarity is Rarity.token:
        embed.add_footer('TOKEN')
    else:
        embed.add_field('Rarity',card.rarity.name,inline=True)
    
    embed.add_field('Description',card.description)
    
    await client.message_create(message.channel,embed=embed)

async def _help_showcard(client,message):
    prefix=client.events.message_create.prefix
    embed=Embed('showcard',(
        'Shows the specified card by it\'s name.\n'
        f'Usage: `{prefix}showcard *name*`'
        ),color=FLAN_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

FLAN_HELPER.add('showcard',_help_showcard)

@commands
async def showcards(client,message,content):
    while True:
        if len(content)>32:
            result=None
            break
        
        if content:
            filtered=[]
            search_for=content.lower()
            for name,card in CARDS_BY_NAME.items():
                if search_for in name:
                    filtered.append(card)
            title=f'Search results for : `{content}`'
        else:
            filtered=list(CARDS_BY_NAME.values())
            title='All cards'
        
        if not filtered:
            result=None
            break
        
        filtered.sort(key=lambda card:card.name)
        
        embeds=[]
        embed=Embed(title,color=CHESUTO_COLOR)
        field_count=0
        total_ln=0 # we do not get the len of the title, we say it is 100 and we check 5900 later.
        
        index=0
        limit=len(filtered)
        while index<limit:
            card=filtered[index]
            index=index+1

            header=[card.name]
            
            rarity=card.rarity
            if rarity is Rarity.token:
                header.append(' [TOKEN]')
            else:
                header.append(' (')
                header.append(card.rarity.name)
                header.append(')')

            header=''.join(header)
            local_ln=len(header)

            description=card.description
            local_ln+=len(description)
            total_ln+=local_ln

            if total_ln>5900 or field_count==24:
                total_ln=local_ln
                embeds.append(embed)
                embed=Embed(title,color=CHESUTO_COLOR)
                embed.add_field(header,description)
                field_count=1
                continue

            embed.add_field(header,description)
            field_count=field_count+1
            continue
        
        embeds.append(embed)
        
        index=0
        field_count=0
        embed_ln=len(embeds)
        result=[]
        while True:
            embed=embeds[index]
            index+=1
            embed.add_footer(f'Page: {index}/{embed_ln}. Results {field_count+1}-{field_count+len(embed.fields)}/{limit}')
            field_count+=len(embed.fields)
            
            result.append(embed)
            
            if index==embed_ln:
                break
        
        break
    
    if result is None:
        result=[Embed(f'No search results for : `{content}`',color=CHESUTO_COLOR)]
    
    await Pagination(client,message.channel,result)

async def _help_showcards(client,message):
    prefix=client.events.message_create.prefix
    embed=Embed('showcards',(
        'Searcher all the cards, which contain the specified string.\n'
        f'Usage: `{prefix}showcards *name*`'
        ),color=FLAN_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

FLAN_HELPER.add('showcards',_help_showcards)

del re
del eventlist
del Cooldown
del CooldownHandler
