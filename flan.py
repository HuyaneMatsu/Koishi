import re, os
from itertools import cycle

from hata import Guild, Embed, Color, Role, sleep, ReuAsyncIO, BUILTIN_EMOJIS, AsyncIO

from hata.ext.commands import setup_ext_commands, Cooldown, Pagination, checks, wait_for_reaction

from shared import FLAN_PREFIX
from tools import CooldownHandler
from chesuto import Rarity, CARDS_BY_NAME, Card, PROTECTED_FILE_NAMES, CHESUTO_FOLDER

CHESUTO_GUILD   = Guild.precreate(598706074115244042)
CHESUTO_COLOR   = Color.from_rgb(73,245,73)
CARDS_ROLE      = Role.precreate(598708907816517632)
CARD_HDR_RP     = re.compile(' *(?:\*\*)? *(.+?) *(?:\[((?:token)|(?:passive)|(?:basic))\])? *(?:\(([a-z]+)\)?)? *(?:\*\*)?',re.I)
VISITORS_ROLE   = Role.precreate(669875992159977492)

setup_ext_commands(Flan,FLAN_PREFIX)

@Flan.events
async def guild_user_add(client, guild, user):
    if guild is not CHESUTO_GUILD:
        return
    
    channel = CHESUTO_GUILD.system_channel
    if channel is None:
        return
    
    if user.is_bot:
        return
    
    await client.user_role_add(user, VISITORS_ROLE)
    await client.message_create(channel,f'Welcome to the Che-su-to~ server {user:m} ! Please introduce yourself !')

FLAN_HELP_COLOR=Color.from_rgb(230,69,0)

@Flan.commands
async def help(client, message, content):
    if (0<len(content)<64):
        content=content.lower()
        if content!='help':
            try:
                command=client.events.message_create.commands[content]
            except KeyError:
                pass
            else:
                if command.run_checks(client, message):
                    run_invalid=False
                    description=command.description
                    if description is None:
                        await client.message_create(message.channel,
                            embed=Embed(f'No help is provided for this command',color=FLAN_HELP_COLOR))
                        return
                    
                    await description(client, message)
                    return
            
            embed=Embed(f'Invalid command: {content}',(
                f'Please try using `{FLAN_PREFIX}help` to list the available commands '
                'for you\n'
                'Take care!'
                ),color=FLAN_HELP_COLOR)
            message = await client.message_create(message.channel,embed=embed)
            await sleep(30.,client.loop)
            await client.message_delete(message)
            return
    
    pages=[]
    part=[]
    index=0
    for command in client.events.message_create.get_default_category().commands:
        if not command.run_checks(client, message):
            continue
        
        if index==16:
            pages.append('\n'.join(part))
            part.clear()
            index=0
        part.append(f'**>>** {command.name}')
        index+=1
    
    pages.append('\n'.join(part))
    
    del part
    
    result=[]
    
    limit=len(pages)
    index=0
    while index<limit:
        embed=Embed('Commands:',color=FLAN_HELP_COLOR,description=pages[index])
        index+=1
        embed.add_field(f'Use `{FLAN_PREFIX}help <command>` for more information.',f'page {index}/{limit}')
        result.append(embed)
    
    del pages
    
    await Pagination(client,message.channel,result)

@Flan.commands
async def invalid_command(client,message,command,content):
    prefix = client.command_processer.get_prefix_for(message)
    embed=Embed(
        f'Invalid command `{command}`',
        f'try using: `{prefix}help`',
        color=FLAN_HELP_COLOR,
            )
    
    message = await client.message_create(message.channel,embed=embed)
    await sleep(30.,client.loop)
    await client.message_delete(message)

@Flan.commands.from_class
class ping:
    @Cooldown('user',30.,handler=CooldownHandler())
    async def ping(client, message):
        await client.message_create(message.channel,f'{client.gateway.latency*1000.:.0f} ms')
    
    aliases=['pong']
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('ping',(
            'Ping - Pong?\n'
            f'Usage: `{prefix}ping`'
            ),color=FLAN_HELP_COLOR)
        await client.message_create(message.channel,embed=embed)

@Flan.commands.from_class
class sync_avatar:
    async def command(client,message):
        avatar_url=client.application.icon_url_as(ext='png',size=4096)
        if avatar_url is None:
            await client.message_create(message.channel,'The application has no avatar set.')
            return
        
        avatar = await client.download_url(avatar_url)
        await client.client_edit(avatar=avatar)
        
        await client.message_create(message.channel,'Avatar synced.')
    
    checks=[checks.owner_only()]
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('sync_avatar',(
            'Hello there Esuto!\n'
            'This is a specific command for You, to sync the bot\'s avatar with '
            'the application\'s. I know, You might struggle with updating the '
            'bot\'s avatar the other way, so I made a command for it.\n'
            'Have a nice day!\n'
            f'Usage: `{prefix}sync_avatar`'
            ),color=FLAN_HELP_COLOR)
        await client.message_create(message.channel,embed=embed)

@Flan.commands.from_class
class massadd:
    async def command(client,message):
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
        return
    
    checks = [checks.owner_or_has_role(CARDS_ROLE)]
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('massadd',(
            'Loads the last 100 message at the channel, and check each of them '
            'searching for card definitions. If it finds one, then updates it, if '
            'already added, or creates a new one.\n'
            f'Usage: `{prefix}massadd`'
            ),color=FLAN_HELP_COLOR).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')
        await client.message_create(message.channel,embed=embed)

@Flan.commands.from_class
class showcard:
    async def command(client,message,content):
        if not 2<len(content)<101:
            return
        
        search_value = content.lower()
        
        card = None
        start_index = 1000
        length = 1000
        
        for card_name, card_ in CARDS_BY_NAME.items():
            index = card_name.find(search_value)
            if index==-1:
                continue
            
            if index > start_index:
                continue
            
            if index == start_index:
                if length >= len(card_name):
                    continue
            
            card = card_
            start_index=index
            length=len(card_name)
            continue
        
        if card is None:
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
        title_parts.append(card.rarity.outlook)
        
        title=''.join(title_parts)
        
        description=card.description
        if len(description)>1700:
            description = description[:1700]+'...'
        
        embed=Embed(title,description,CHESUTO_COLOR)
        
        image_name = card.image_name
        if image_name is None:
            await client.message_create(message.channel,embed=embed)
            return
        
        embed.add_image(f'attachment://{image_name}')
        with (await ReuAsyncIO(os.path.join(CHESUTO_FOLDER,image_name),'rb')) as file:
            await client.message_create(message.channel,embed=embed,file=file)
    
    async def description(client,message):
        embed=Embed('showcard',(
            'Shows the specified card by it\'s name.\n'
            f'Usage: `{FLAN_PREFIX}showcard *name*`'
            ),color=FLAN_HELP_COLOR)
        await client.message_create(message.channel,embed=embed)


@Flan.commands.from_class
class showcards:
    async def command(client, message, content):
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
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('showcards',(
            'Searcher all the cards, which contain the specified string.\n'
            f'Usage: `{prefix}showcards *name*`'
            ),color=FLAN_HELP_COLOR)
        await client.message_create(message.channel,embed=embed)

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
                page_parts.append(card.rarity.outlook)
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
                page_parts.append(card.rarity.outlook)
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
                page_parts.append(card.rarity.outlook)
                page_parts.append('\n\n')
                page_parts.append(card.description)
            
                if index==end:
                    break
                
                page_parts.append('\n\n')
                continue
        
        return Embed(self.title,''.join(page_parts),color=CHESUTO_COLOR).add_footer(
            f'Page: {page_index+1}/{len(self.page_information)}. Results {start+1}-{end}/{len(self.collected)}')

ADD_IMAGE_OK = BUILTIN_EMOJIS['ok_hand']
ADD_IMAGE_CANCEL = BUILTIN_EMOJIS['x']
ADD_IMAGE_EMOJIS = (ADD_IMAGE_OK, ADD_IMAGE_CANCEL)

def ADD_IMAGE_CHECKER(message, emoji, user):
    if user.is_bot:
        return False
    
    if not user.has_role(CARDS_ROLE):
        return False
    
    if emoji not in ADD_IMAGE_EMOJIS:
        return False
    
    return True

@Flan.commands.from_class
class add_image:
    async def command(client, message, cards_name):
        while True:
            attachments = message.attachments
            if attachments is None:
                content = 'The message has no attachment provided.'
                break
            
            if len(attachments)>1:
                content = 'The message has more attachmemnts.'
            
            attachment = attachments[0]
            name=attachment.name
            extension=os.path.splitext(name)[1].lower()
            
            if extension not in ('.png','.jpg','.jpeg','.bmp','.mp4','.gif'): # are there more?
                content = 'You sure the message format is an image format?\n If you are please request adding it.'
                break
            
            if name in PROTECTED_FILE_NAMES:
                content = 'The file\'s name is same as a protected file\'s name.'
                break
            
            card = CARDS_BY_NAME.get(cards_name.lower())
            if card is None:
                content = 'Could not find a card with that name.'
                break
            
            actual_image_name = card.image_name
            
            file_path = os.path.join(CHESUTO_FOLDER,name)
            exists = os.path.exists(file_path)
            
            should_dump = True
            if actual_image_name is None:
                if exists:
                    content = 'A file already exists with that name, if you overwrite it, more cards will have the same ' \
                              'image.\nAre you sure?'
                else:
                    content = None
            else:
                if exists:
                    if actual_image_name == name:
                        content = 'Are you sure at overwriting the card\'s image?'
                        should_dump = False
                    else:
                        content = 'A file with that name already exists.\nIf you overwrite this card\'s image like that, ' \
                                  'you will endup with more cards with the same image. Are you sure?'
                else:
                    content = 'The card has an image named differently. Are you sure like this?'
            
            if (content is not None):
                message = await client.message_create(message.channel,
                    embed=Embed(description=content,color=CHESUTO_COLOR))
                
                for emoji in ADD_IMAGE_EMOJIS:
                    await client.reaction_add(message,emoji)
                
                try:
                    _, emoji, _ = await wait_for_reaction(client, message, ADD_IMAGE_CHECKER, 40.)
                except TimeoutError:
                    emoji = ADD_IMAGE_CANCEL
                
                await client.message_delete(message)
                
                if emoji is ADD_IMAGE_CANCEL:
                    content = 'Cancelled.'
                    break
            
            image_data = await client.download_attachment(attachment)
            with (await AsyncIO(file_path,'wb')) as file:
                await file.write(image_data)
            
            if should_dump:
                card.image_name=name
                await Card.dump_cards(client.loop)
            
            content = f'Image successfully added for {card.name}.'
            break
        
        message = await client.message_create(message.channel,
            embed=Embed(description=content,color=CHESUTO_COLOR))
        
        await sleep(30.)
        await client.message_delete(message)
        return
    
    checks=[checks.has_role(CARDS_ROLE)]
    name = 'add-image'
    aliases = ['add_image']
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('add_image',(
            'Adds or updates an image of a card.\n'
            f'Usage: `{prefix}add_image <card name>`\n'
            'Also include an image as attachment.'
            ),color=FLAN_HELP_COLOR).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')
        await client.message_create(message.channel,embed=embed)

@Flan.commands.from_class
class checklist:

    async def command(client, message, content):
        result=[]
        if content:
            rarity=Rarity.BY_NAME.get(content.lower())
            if rarity is None:
                if len(content)>50:
                    content = content[:50]+'...'
                result.append(Embed(f'{content!r} is not a rarity',color=CHESUTO_COLOR))
                
            else:
                filtered=[]
                
                for card in CARDS_BY_NAME.values():
                    if card.rarity is rarity:
                        if card.image_name is None:
                            continue
                        
                        filtered.append(card)
                        continue
                
                title = f'Checklist for {rarity.name}'
                
                limit=len(filtered)
                if limit:
                    parts=[]
                    index=1
                    
                    card=filtered[0]
                    name=card.name
                    length=len(name)
                    if length>200:
                        name = name[:200]+'...'
                        length = 203
                    
                    parts.append(name)
                    
                    while True:
                        if index==limit:
                            break
                        
                        card=filtered[index]
                        index=index+1
                        name=card.name
                        
                        name_ln=len(name)
                        if name_ln>200:
                            name = name[:200]+'...'
                            name_ln = 203
                        
                        length=length+name_ln+1
                        if length>2000:
                            result.append(Embed(title,''.join(parts),color=CHESUTO_COLOR))
                            length=name_ln
                            parts.clear()
                            parts.append(name)
                            continue
                        
                        parts.append('\n')
                        parts.append(name)
                        continue
                    
                    if parts:
                        result.append(Embed(title,''.join(parts),color=CHESUTO_COLOR))
                    
                    parts=None
                else:
                    result.append(Embed(title,color=CHESUTO_COLOR))
                
        else:
            filtered=tuple([] for x in range(len(Rarity.INSTANCES)))
            
            for card in CARDS_BY_NAME.values():
                if card.image_name is None:
                    continue
                
                filtered[card.rarity.index].append(card)
                continue
            
            title='Checklist'
            
            parts=[]
            length=0
            
            for rarity_index in range(len(filtered)):
                container=filtered[rarity_index]
                
                limit=len(container)
                if limit==0:
                    continue
                
                if length>1500:
                    result.append(Embed(title,''.join(parts),color=CHESUTO_COLOR))
                    length=0
                    parts.clear()
                else:
                    parts.append('\n\n')
                    length = length+2
                
                rarity_name=f'**{Rarity.INSTANCES[rarity_index].name}**\n\n'
                length = length+len(rarity_name)
                parts.append(rarity_name)
                
                card=container[0]
                name=card.name
                name_ln=len(name)
                if name_ln>200:
                    name = name[:200]+'...'
                    name_ln = 203
                
                length = length+name_ln
                parts.append(name)
                index=1
                
                while True:
                    if index==limit:
                        break
                    
                    card=container[index]
                    index=index+1
                    name=card.name
                    name_ln=len(name)
                    if name_ln>200:
                        name = name[:200]+'...'
                        name_ln=203
                    
                    length = length+1+name_ln
                    if length>2000:
                        result.append(Embed(title,''.join(parts),color=CHESUTO_COLOR))
                        length=len(rarity_name)+name_ln
                        parts.clear()
                        parts.append(rarity_name)
                        parts.append(name)
                        continue
                    
                    parts.append('\n')
                    parts.append(name)
                    continue
                
            if parts:
                result.append(Embed(title,''.join(parts),color=CHESUTO_COLOR))
            
            parts=None
        
        index=0
        limit=len(result)
        while True:
            if index==limit:
                break
            
            embed=result[index]
            index=index+1
            embed.add_footer(f'Page: {index}/{limit}')
        
        await Pagination(client,message.channel,result)
        return
    
    checks=[checks.has_role(CARDS_ROLE)]
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('checklist',(
            'Lists the cards of the given rarity, which have images added to them.\n'
            'If no rarity is provided, I will list all the cards with images.\n'
            f'Usage: `{prefix}checklist *rarity*`\n'
            ),color=FLAN_HELP_COLOR).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')
        await client.message_create(message.channel,embed=embed)
    
@Flan.commands.from_class
class dump_all_card:
    async def command(client, message):
        channel=message.channel
        clients = channel.clients
        if len(clients)<2:
            await client.message_create(channel.channel,'I need at least 2 clients at the channel to execute this command.')
            return
        
        for other_client in clients:
            if client is other_client:
                continue
            
            if channel.cached_permissions_for(other_client).can_send_messages:
                break
        else:
            await client.message_create(channel.channel,'I need at least 2 clients at the channel, which can sen messages as well!')
            return
        
        clients = (client,other_client)
        for client in clients:
            if channel.cached_permissions_for(client).can_manage_messages:
                await client.message_delete(message)
                break
        
        cards = list(CARDS_BY_NAME.values())
        cards.sort(key=lambda card:card.name)
        
        for card, client in zip(cards,cycle(clients),):
            title_parts=['**']
            name=card.name
            if len(name)>200:
                title=name[:200]
                title_parts.append(title)
                title_parts.append('...')
            else:
                title_parts.append(name)
           
            title_parts.append('** ')
            title_parts.append(card.rarity.outlook)
            
            title=''.join(title_parts)
            
            description=card.description
            if len(description)>1700:
                description = description[:1700]+'...'
            
            embed=Embed(title,description,CHESUTO_COLOR)
            
            await client.message_create(channel,embed=embed)
    
    name = 'dump-all-card'
    checks=[checks.has_role(CARDS_ROLE)]
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('dump-all-card',(
            'Lists all the cards to this channel.\n'
            f'Usage: `{prefix}dump-all-card`\n'
            ),color=FLAN_HELP_COLOR).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')
        await client.message_create(message.channel,embed=embed)

del re
del Cooldown
del CooldownHandler
