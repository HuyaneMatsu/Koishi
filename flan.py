import re

from hata import Guild, eventlist, Embed, Color, Role, sleep
from hata.events import Cooldown, Pagination

from help_handler import FLAN_HELPER, FLAN_HELP_COLOR, flan_invalid_command
from tools import CooldownHandler
from chesuto import Rarity, CARDS_BY_NAME, Card

CHESUTO_GUILD   = Guild.precreate(598706074115244042)
CHESUTO_COLOR   = Color.from_rgb(73,245,73)
CARDS_ROLE      = Role.precreate(598708907816517632)
CARD_HDR_RP     = re.compile(' *(?:\*\*)? *(.+?) *(?:\[((?:token)|(?:passive))\])? *(?:\(([a-z]+)\)?)? *(?:\*\*)?',re.I)

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
        return True
    
    avatar_url=client.application.icon_url_as(ext='png',size=4096)
    if avatar_url is None:
        await client.message_create(message.channel,'The application has no avatar set.')
        return True
    
    avatar = await client.download_url(avatar_url)
    await client.client_edit(avatar=avatar)
    
    await client.message_create(message.channel,'Avatar synced.')
    return False

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
            return True
        
        if CARDS_ROLE in profile.roles:
            break
        
        return True
    
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
                name,special_rarity,rarity=parsed.groups()
                
                if special_rarity is None:
                    special_rarity=-1
                else:
                    special_rarity=special_rarity.lower()
                    if special_rarity=='token':
                        special_rarity=0
                    elif special_rarity=='passive':
                        special_rarity=1
                    else:
                        special_rarity=-1
                
                if special_rarity==-1:
                    if rarity is None:
                        special_rarity=0
                    else:
                        rarity=rarity.lower()
                
                if special_rarity!=-1:
                    try:
                        rarity=Rarity.INSTANCES[special_rarity]
                    except IndexError:
                        continue
                else:
                    try:
                        rarity=Rarity.BY_NAME[rarity]
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
            if Card.update(description,next_id,name,rarity):
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
    return False

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
    
    title_parts=['**']
    name=card.name
    if len(name)>200:
        title=name[:200]
        title_parts.append(title)
        title_parts.append('...')
    else:
        title_parts.append(name)
   
    title_parts.append('** ')
    
    rarity=card.rarity
    if rarity is Rarity.token:
        title_parts.append(' [TOKEN]')
    elif rarity is Rarity.passive:
        title_parts.append(' [PASSIVE]')
    else:
        title_parts.append(' (')
        title_parts.append(card.rarity.name)
        title_parts.append(')')
    
    title=''.join(title_parts)
    
    description=card.description
    if len(description)>1700:
        description = description[:1700]+'...'
    
    embed=Embed(title,description,CHESUTO_COLOR)
    
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
            rarity=Rarity.BY_NAME.get(search_for)
            if rarity is None:
                for name,card in CARDS_BY_NAME.items():
                    if search_for in name:
                        filtered.append(card)
            else:
                for card in CARDS_BY_NAME.values():
                    if card.rarity is rarity:
                        filtered.append(card)
            
            title=f'Search results for : `{content}`'
        else:
            filtered=list(CARDS_BY_NAME.values())
            title='All cards'
        
        if not filtered:
            result=None
            break
        
        filtered.sort(key=lambda card:card.name)
        result=filtered
        break
    
    if result is None:
        pages=[Embed(f'No search results for : `{content}`',color=CHESUTO_COLOR)]
    else:
        pages=CardPaginator(title,result)
    
    await Pagination(client,message.channel,pages)
    
class CardPaginator(object):
    __slots__ = ('title', 'rendered', 'collected', 'page_information')
    def __init__(self, title, collected):
        self.title=title
        self.collected=collected
        
        page_information=[]
        self.page_information=page_information
        
        total_length=0
        
        page_information_start=0
        
        index=0
        limit=len(collected)
        
        while True:
            if index==limit:
                page_information.append((page_information_start,index),)
                break
            
            card=collected[index]
            
            local_length=50+len(card.name)+len(card.description)
            
            if total_length+local_length>2000:
                page_information.append((page_information_start,index),)
                page_information_start=index
                index=index+1
                total_length=local_length
                continue
            
            index=index+1
            total_length+=local_length
            continue
        
        self.rendered=list(None for _ in range(len(page_information)))
        
    def __len__(self):
        return len(self.page_information)
    
    def __getitem__(self,index):
        page=self.rendered[index]
        if page is None:
            page=self.render(index)
            self.rendered[index]=page
        
        return page
    
    def render(self,page_index):
        start, end = self.page_information[page_index]
        
        page_parts=[]
        # The card's description or title might be too long, lets check them.
        if start+1 == end:
            card=self.collected[start]
            
            name=card.name
            description=card.description
            
            local_length=50+len(name)+len(description)
            # No good, our fear happens
            if local_length>2000:
                page_parts.append('**')
                
                if len(name)>200:
                    title=name[:200]
                    page_parts.append(title)
                    page_parts.append('...')
                else:
                    page_parts.append(name)
               
                page_parts.append('** ')
                
                rarity=card.rarity
                if rarity is Rarity.token:
                    page_parts.append(' [TOKEN]')
                elif rarity is Rarity.passive:
                    page_parts.append(' [PASSIVE]')
                else:
                    page_parts.append(' (')
                    page_parts.append(card.rarity.name)
                    page_parts.append(')')
                
                page_parts.append('\n\n')
                
                if len(description)>1700:
                    description = description[:1700]
                    page_parts.append(description)
                    page_parts.append('...')
                else:
                    page_parts.append(description)
                
            else:
                page_parts.append('**')
                page_parts.append(name)
                page_parts.append('** ')
                
                rarity=card.rarity
                if rarity is Rarity.token:
                    page_parts.append(' [TOKEN]')
                elif rarity is Rarity.passive:
                    page_parts.append(' [PASSIVE]')
                else:
                    page_parts.append(' (')
                    page_parts.append(card.rarity.name)
                    page_parts.append(')')
                
                page_parts.append('\n\n')
                page_parts.append(description)
        
        else:
            index=start
            
            while True:
                
                card=self.collected[index]
                index=index+1
                
                page_parts.append('**')
                page_parts.append(card.name)
                page_parts.append('** ')
                
                rarity=card.rarity
                if rarity is Rarity.token:
                    page_parts.append(' [TOKEN]')
                elif rarity is Rarity.passive:
                    page_parts.append(' [PASSIVE]')
                else:
                    page_parts.append(' (')
                    page_parts.append(card.rarity.name)
                    page_parts.append(')')
                
                page_parts.append('\n\n')
                page_parts.append(card.description)
            
                if index==end:
                    break
                
                page_parts.append('\n\n')
                continue
        
        return Embed(self.title,''.join(page_parts),color=CHESUTO_COLOR).add_footer(
            f'Page: {page_index+1}/{len(self.page_information)}. Results {start+1}-{end}/{len(self.collected)}')
        
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
