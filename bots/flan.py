# -*- coding: utf-8 -*-
import re, os
from itertools import cycle
from random import choice

from hata import Guild, Embed, Color, Role, sleep, ReuAsyncIO, BUILTIN_EMOJIS, AsyncIO, ChannelText, KOKORO, Client, \
    Lock, alchemy_incendiary, DiscordException, ERROR_CODES
from hata.backend.utils import sortedlist
from hata.ext.command_utils import Pagination, wait_for_reaction, wait_for_message
from hata.ext.commands_v2.helps.subterranean import SubterraneanHelpCommand
from hata.ext.commands_v2 import checks

from bot_utils.shared import PREFIX__FLAN, COLOR__FLAN_HELP, PATH__KOISHI
from bot_utils.tools import CooldownHandler, MessageDeleteWaitfor, MessageEditWaitfor
from bot_utils.chesuto import Rarity, CARDS_BY_NAME, Card, PROTECTED_FILE_NAMES, CHESUTO_FOLDER, EMBED_NAME_LENGTH, \
    get_card
from csv import reader as CSVReader, writer as CSVWriter

CHESUTO_GUILD = Guild.precreate(598706074115244042)
CHESUTO_COLOR = Color.from_rgb(73, 245, 73)
CARDS_ROLE = Role.precreate(598708907816517632)
CARD_HDR_RP = re.compile(
    ' *(?:\*\*)? *(.+?) *(?:\[((?:token)|(?:passive)|(?:basic))\])? *(?:\(([a-z]+)\)?)? *(?:\*\*)?',
    re.I,)
VISITORS_ROLE = Role.precreate(669875992159977492)
CHESUTO_BGM_MESSAGES = set()
CHESUTO_BGM_CHANNEL = ChannelText.precreate(707892105749594202)
CHESUTO_BGM_TRACKS = {}
CHESUTO_BGM_TRACKS_SORTED = sortedlist()
BGM_SPLIT_PATTERN = re.compile('([^ _-]+)')
BGM_NAME_PATTERN = re.compile('[a-z0-9]+', re.I)
PERCENT_RP = re.compile('(\d*)[%]?')

BMG_NAMES_W_S = {
    'backstory',
    'est',
    'lucy',
    'corrupted',
    'fatale',
    'overseer',
    'erlmeier',
    'chesuto',
    'grashaw',
    'springwind',
    'lifendel',
    'asterwart',
    'sindarin',
    'market',
    'runesworth',
    'rifengrad',
    'luyavean',
    'tavern',
    'wyvendel',
    'grashawl',
    'lene',
    'castle',
    'firtrun',
    'radialt',
    'yshar',
        }

FILE_NAME = 'bgm_names.csv'

FILE_PATH = os.path.join(PATH__KOISHI, 'chesuto_data', FILE_NAME)
FILE_LOCK = Lock(KOKORO)

def read_bgm_name_task():
    names = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            reader = CSVReader(file)
            for key, value in reader:
                names[key] = value
    
    return names


def write_bgm_name_task():
    with open(FILE_PATH, 'w') as file:
        writer = CSVWriter(file)
        writer.writerows(BGM_NAMES.items())


async def read_bgm_names():
    async with FILE_LOCK:
        return await KOKORO.run_in_executor(read_bgm_name_task)


async def write_bgm_names():
    async with FILE_LOCK:
        await KOKORO.run_in_executor(alchemy_incendiary(write_bgm_name_task, ()))

BGM_NAMES = read_bgm_name_task()


def get_bgm_name_for(name):
    try:
        name = BGM_NAMES[name]
    except KeyError:
        name = get_auto_bgm_name(name)
    
    return name


def get_auto_bgm_name(name):
    parts = BGM_NAME_PATTERN.findall(name)
    if not parts:
        return ''
    
    last = parts[-1]
    if len(last) == 3 and last.lower() == 'mp3':
        del parts[-1]
    
    index = 0
    limit = len(parts)
    while True:
        if index == limit:
            break
        
        part = parts[index]
        if part.endswith('s'):
            word = part[:-1]
            if word.lower() in BMG_NAMES_W_S:
                parts[index] = f'{word}\'s'
        
        index += 1
        continue
    
    return ' '.join(parts)

Flan: Client

Flan.events(MessageDeleteWaitfor)
Flan.events(MessageEditWaitfor)

def flan_help_embed_postprocessor(command_context, embed):
    if embed.color is None:
        embed.color = COLOR__FLAN_HELP

Flan.commands(SubterraneanHelpCommand(embed_postprocessor=flan_help_embed_postprocessor), 'help')
Flan.command_processor.create_category('VOICE', checks=checks.guild_only())

@Flan.events
async def guild_user_add(client, guild, user):
    if guild is not CHESUTO_GUILD:
        return
    
    if user.is_bot:
        return
    
    await client.user_role_add(user, VISITORS_ROLE)
    
    channel = CHESUTO_GUILD.system_channel
    if channel is None:
        return
    
    await client.message_create(channel, f'Welcome to the Che-su-to~ server {user:m} ! Please introduce yourself !')


@Flan.commands.from_class
class ping:
    async def ping(client, message):
        await client.message_create(message.channel, f'{client.gateway.latency*1000.:.0f} ms')
    
    aliases = 'pong'
    
    async def description(command_context):
        return Embed('ping',(
            'Ping - Pong?\n'
            f'Usage: `{command_context.prefix}ping`'
            ), color=COLOR__FLAN_HELP)

@Flan.commands.from_class
class sync_avatar:
    async def command(client, message):
        avatar_url = client.application.icon_url_as(ext='png', size=4096)
        if avatar_url is None:
            await client.message_create(message.channel, 'The application has no avatar set.')
            return
        
        async with client.http.get(avatar_url) as response:
            avatar = await response.read()
        
        await client.client_edit(avatar=avatar)
        
        await client.message_create(message.channel,'Avatar synced.')
    
    checks = checks.owner_only()
    
    async def description(command_context):
        return Embed('sync_avatar',(
            'Hello there Esuto!\n'
            'This is a specific command for You, to sync the bot\'s avatar with '
            'the application\'s. I know, You might struggle with updating the '
            'bot\'s avatar the other way, so I made a command for it.\n'
            'Have a nice day!\n'
            f'Usage: `{command_context.prefix}sync_avatar`'
            ), color=COLOR__FLAN_HELP)

@Flan.commands.from_class
class massadd:
    async def command(client, message):
        try:
            await client.message_at_index(message.channel,1000)
        except IndexError:
            pass
        
        await client.message_delete(message)
        
        messages = []
        for message_ in message.channel.messages:
            guild_profile = message_.author.get_guild_profile_for(CARDS_ROLE.guild)
            if guild_profile is None:
                continue
            
            profile_roles = guild_profile.roles
            if (profile_roles is None) or (CARDS_ROLE not in profile_roles):
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
                    new_ += 1
                else:
                    modified_ += 1
        
        del description_parts
        
        if new_ or modified_:
            await Card.dump_cards(KOKORO)
        
        message = await client.message_create(message.channel,
            embed = Embed(None,f'modified: {modified_}\nnew: {new_}', color=CHESUTO_COLOR))
        await sleep(30., KOKORO)
        await client.message_delete(message)
        return
    
    checks = checks.owner_or_has_role(CARDS_ROLE)
    
    async def description(command_context):
        return Embed('massadd', (
            'Loads the last 100 message at the channel, and check each of them '
            'searching for card definitions. If it finds one, then updates it, if '
            'already added, or creates a new one.\n'
            f'Usage: `{command_context.prefix}massadd`'
            ), color=COLOR__FLAN_HELP).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')

@Flan.commands.from_class
class showcard:
    async def command(client, message, content):
        card = get_card(content)
        
        if card is None:
            await client.message_create(message.channel,embed = Embed(None,'*Nothing found.*',CHESUTO_COLOR))
            return
        
        embed = card.render_to_embed()
        
        image_name = card.image_name
        if image_name is None:
            await client.message_create(message.channel,embed=embed)
            return
        
        embed.add_image(f'attachment://{image_name}')
        
        with client.keep_typing(message.channel):
            with (await ReuAsyncIO(os.path.join(CHESUTO_FOLDER,image_name),'rb')) as file:
                await client.message_create(message.channel,embed=embed,file=file)
    
    async def description(command_context):
        return Embed('showcard', (
            'Shows the specified card by it\'s name.\n'
            f'Usage: `{command_context.prefix}showcard *name*`'
            ), color=COLOR__FLAN_HELP)

@Flan.commands.from_class
class showcards:
    async def command(client, message, content):
        while True:
            if len(content) > 32:
                result = None
                break
            
            if content:
                filtered = []
                search_for = content.lower()
                rarity = Rarity.BY_NAME.get(search_for, None)
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
            pages=[Embed(f'No search results for : `{content}`', color=CHESUTO_COLOR)]
        else:
            pages=CardPaginator(title,result)
        
        await Pagination(client,message.channel,pages)
    
    async def description(command_context):
        return Embed('showcards',(
            'Searches all the cards, which contain the specified string.\n'
            f'Usage: `{command_context.prefix}showcards *name*`'
            ), color=COLOR__FLAN_HELP)

class CardPaginator:
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
            
            # 2 extra linebreak
            local_length=2+len(card)
            
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
        index = start
        while True:
            card=self.collected[index]
            card.render_to(page_parts)
            
            index = index+1
            if index==end:
                break
            
            page_parts.append('\n\n')
            continue
        
        return Embed(self.title,''.join(page_parts), color=CHESUTO_COLOR).add_footer(
            f'Page: {page_index+1}/{len(self.page_information)}. Results {start+1}-{end}/{len(self.collected)}')

ADD_IMAGE_OK = BUILTIN_EMOJIS['ok_hand']
ADD_IMAGE_CANCEL = BUILTIN_EMOJIS['x']
ADD_IMAGE_EMOJIS = (ADD_IMAGE_OK, ADD_IMAGE_CANCEL)

def ADD_IMAGE_CHECKER(event):
    if event.user.is_bot:
        return False
    
    if not event.user.has_role(CARDS_ROLE):
        return False
    
    if event.emoji not in ADD_IMAGE_EMOJIS:
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
            
            if len(attachments) > 1:
                content = 'The message has more attachments.'
                break
            
            attachment = attachments[0]
            name=attachment.name
            extension=os.path.splitext(name)[1].lower()
            
            if extension not in ('.png','.jpg','.jpeg','.bmp','.mp4','.gif'): # are there more?
                content = 'You sure the message format is an image format?\n If you are please request adding it.'
                break
            
            if name in PROTECTED_FILE_NAMES:
                content = 'The file\'s name is same as a protected file\'s name.'
                break
            
            card = CARDS_BY_NAME.get(cards_name.lower(), None)
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
                                  'you will end up with more cards with the same image. Are you sure?'
                else:
                    content = 'The card has an image named differently. Are you sure like this?'
            
            if (content is not None):
                message = await client.message_create(message.channel,
                    embed = Embed(description=content, color=CHESUTO_COLOR))
                
                for emoji in ADD_IMAGE_EMOJIS:
                    await client.reaction_add(message,emoji)
                
                try:
                    event = await wait_for_reaction(client, message, ADD_IMAGE_CHECKER, 40.)
                except TimeoutError:
                    emoji = ADD_IMAGE_CANCEL
                else:
                    emoji = event.emoji
                
                await client.message_delete(message)
                
                if emoji is ADD_IMAGE_CANCEL:
                    content = 'Cancelled.'
                    break
            
            image_data = await client.download_attachment(attachment)
            with (await AsyncIO(file_path,'wb')) as file:
                await file.write(image_data)
            
            if should_dump:
                card.image_name = name
                await Card.dump_cards(KOKORO)
            
            content = f'Image successfully added for {card.name}.'
            break
        
        message = await client.message_create(message.channel,
            embed = Embed(description=content, color=CHESUTO_COLOR))
        
        await sleep(30.)
        await client.message_delete(message)
        return
    
    checks = checks.has_role(CARDS_ROLE)
    
    async def description(command_context):
        return Embed('add_image',(
            'Adds or updates an image of a card.\n'
            f'Usage: `{command_context.prefix}add_image <card name>`\n'
            'Also include an image as attachment.'
            ), color=COLOR__FLAN_HELP).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')

@Flan.commands.from_class
class checklist:

    async def command(client, message, content):
        result = []
        if content:
            rarity = Rarity.BY_NAME.get(content.lower(), None)
            if rarity is None:
                if len(content) > 50:
                    content = content[:50]+'...'
                result.append(Embed(f'{content!r} is not a rarity', color=CHESUTO_COLOR))
                
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
                    if length>EMBED_NAME_LENGTH:
                        name = name[:EMBED_NAME_LENGTH]+'...'
                        length = 203
                    
                    parts.append(name)
                    
                    while True:
                        if index==limit:
                            break
                        
                        card=filtered[index]
                        index=index+1
                        name=card.name
                        
                        name_ln=len(name)
                        if name_ln>EMBED_NAME_LENGTH:
                            name = name[:EMBED_NAME_LENGTH]+'...'
                            name_ln = 203
                        
                        length=length+name_ln+1
                        if length>2000:
                            result.append(Embed(title,''.join(parts), color=CHESUTO_COLOR))
                            length=name_ln
                            parts.clear()
                            parts.append(name)
                            continue
                        
                        parts.append('\n')
                        parts.append(name)
                        continue
                    
                    if parts:
                        result.append(Embed(title,''.join(parts), color=CHESUTO_COLOR))
                    
                    parts=None
                else:
                    result.append(Embed(title, color=CHESUTO_COLOR))
                
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
                    result.append(Embed(title,''.join(parts), color=CHESUTO_COLOR))
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
                if name_ln>EMBED_NAME_LENGTH:
                    name = name[:EMBED_NAME_LENGTH]+'...'
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
                    if name_ln>EMBED_NAME_LENGTH:
                        name = name[:EMBED_NAME_LENGTH]+'...'
                        name_ln=203
                    
                    length = length+1+name_ln
                    if length>2000:
                        result.append(Embed(title,''.join(parts), color=CHESUTO_COLOR))
                        length=len(rarity_name)+name_ln
                        parts.clear()
                        parts.append(rarity_name)
                        parts.append(name)
                        continue
                    
                    parts.append('\n')
                    parts.append(name)
                    continue
                
            if parts:
                result.append(Embed(title,''.join(parts), color=CHESUTO_COLOR))
            
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
    
    checks = checks.has_role(CARDS_ROLE)
    
    async def description(command_context):
        return Embed('checklist',(
            'Lists the cards of the given rarity, which have images added to them.\n'
            'If no rarity is provided, I will list all the cards with images.\n'
            f'Usage: `{command_context.prefix}checklist *rarity*`\n'
            ), color=COLOR__FLAN_HELP).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')
    
@Flan.commands.from_class
class dump_all_card:
    async def command(client, message):
        channel = message.channel
        clients = channel.clients
        if len(clients) < 2:
            await client.message_create(channel.channel,
                'I need at least 2 clients at the channel to execute this command.')
            return
        
        for other_client in clients:
            if client is other_client:
                continue
            
            if channel.cached_permissions_for(other_client).can_send_messages:
                break
        else:
            await client.message_create(channel.channel,
                'I need at least 2 clients at the channel, which can sen messages as well!')
            return
        
        clients = (client,other_client)
        for client in clients:
            if channel.cached_permissions_for(client).can_manage_messages:
                await client.message_delete(message)
                break
        
        cards = list(CARDS_BY_NAME.values())
        cards.sort(key=lambda card:card.name)
        
        for card, client in zip(cards,cycle(clients),):
            embed = card.render_to_embed()
            
            await client.message_create(channel, embed=embed)
    
    checks = checks.has_role(CARDS_ROLE)
    
    async def description(command_context):
        return Embed('dump-all-card',(
            'Lists all the cards to this channel.\n'
            f'Usage: `{command_context.prefix}dump-all-card`\n'
            ), color=COLOR__FLAN_HELP).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')

REMOVE_CARD_OK = BUILTIN_EMOJIS['ok_hand']
REMOVE_CARD_CANCEL = BUILTIN_EMOJIS['x']
REMOVE_CARD_EMOJIS = (REMOVE_CARD_OK, REMOVE_CARD_CANCEL)

@Flan.commands.from_class
class remove_card:
    async def command(client, message, content):
        card = get_card(content)
        
        if card is None:
            await client.message_create(message.channel, embed=Embed(None, '*Nothing found.*', CHESUTO_COLOR))
            return
        
        message = await client.message_create(message.channel, embed = Embed(
            None, f'Are you sure, to remove {card.name!r}?', CHESUTO_COLOR,))
        
        for emoji in REMOVE_CARD_EMOJIS:
            await client.reaction_add(message,emoji)
        
        try:
            event = await wait_for_reaction(client, message, ADD_IMAGE_CHECKER, 40.)
        except TimeoutError:
            emoji = REMOVE_CARD_CANCEL
        else:
            emoji = event.emoji
        
        await client.message_delete(message)
        
        if emoji is REMOVE_CARD_CANCEL:
            content = 'Cancelled.'
        else:
            card._delete()
            await Card.dump_cards(KOKORO)
            content = f'{card.name!r} successfully removed.'
        
        message = await client.message_create(message.channel,
            embed = Embed(description=content, color=CHESUTO_COLOR))
        
        await sleep(30., KOKORO)
        await client.message_delete(message)
        return
    
    checks = checks.has_role(CARDS_ROLE)
    
    async def description(command_context):
        return Embed('remove-card',(
            'Removes the specific card\n'
            f'Usage: `{command_context.prefix}remove-card <name>`\n'
            ), color=COLOR__FLAN_HELP).add_footer(
                f'You must have `{CARDS_ROLE}` role to use this command.')

@Flan.events
async def ready(client):
    async for message in await client.message_iterator(CHESUTO_BGM_CHANNEL):
        Track.create(message)

async def bgm_message_create(client, message):
    Track.create(message)

async def bgm_message_delete(client, message):
    Track.delete(message)

async def bgm_message_edit(client, message, old):
    Track.edit(message)

Flan.command_processor.append(CHESUTO_BGM_CHANNEL, bgm_message_create)
Flan.events.message_delete.append(CHESUTO_BGM_CHANNEL, bgm_message_delete)
Flan.events.message_edit.append(CHESUTO_BGM_CHANNEL, bgm_message_edit)

class Track:
    __slots__ = ('display_name', 'source_name', 'url', 'description', 'id')
    @classmethod
    def create(cls, message):
        attachments = message.attachments
        if attachments is None:
            return
        
        for attachment in attachments:
            if attachment.name.endswith('.mp3'):
                break
        else:
            return
        
        self = cls()
        name = attachment.name
        self.source_name = name
        self.display_name = get_bgm_name_for(name)
        self.url = attachment.url
        self.description = message.content
        self.id = message.id
        
        CHESUTO_BGM_TRACKS_SORTED.add(self)
        CHESUTO_BGM_MESSAGES.add(message)
        CHESUTO_BGM_TRACKS[message.id] = self
    
    @staticmethod
    def delete(message):
        try:
            CHESUTO_BGM_MESSAGES.remove(message)
        except KeyError:
            return
        
        try:
            self = CHESUTO_BGM_TRACKS.pop(message.id)
        except KeyError:
            return
        
        path = os.path.join(os.path.abspath('..'), CHESUTO_FOLDER, self.source_name)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
        
        try:
            CHESUTO_BGM_TRACKS_SORTED.remove(self)
        except ValueError:
            pass
    
    @staticmethod
    def edit(message):
        try:
            self = CHESUTO_BGM_TRACKS[message.id]
        except KeyError:
            return
        
        self.description = message.content
    
    def __gt__(self, other):
        self_source_name = self.source_name
        other_source_name = other.source_name
        
        if self_source_name > other_source_name:
            return True
        
        if self_source_name == other_source_name:
            if self.id > other.id:
                return True
        
        return False
    
    def __ge__(self, other):
        self_source_name = self.source_name
        other_source_name = other.source_name
        
        if self_source_name > other_source_name:
            return True
        
        if self_source_name == other_source_name:
            if self.id >= other.id:
                return True
        
        return False
    
    def __eq__(self, other):
        if self.id == other.id:
            return True
        
        return False
    
    def __le__(self, other):
        self_source_name = self.source_name
        other_source_name = other.source_name
        
        if self_source_name < other_source_name:
            return True
        
        if self_source_name == other_source_name:
            if self.id <= other.id:
                return True
        
        return False
    
    def __lt__(self, other):
        self_source_name = self.source_name
        other_source_name = other.source_name
        
        if self_source_name < other_source_name:
            return True
        
        if self_source_name == other_source_name:
            if self.id < other.id:
                return True
        
        return False


def get_bgm(content):
    if not content:
        return None
    
    if content.isnumeric():
        index = int(content)-1
        if index >= 0 and index < len(CHESUTO_BGM_TRACKS_SORTED):
            return CHESUTO_BGM_TRACKS_SORTED[index]
    
    parts = BGM_SPLIT_PATTERN.findall(content)
    if not parts:
        return None
    
    final = []
    
    index = 0
    limit = len(parts)
    while True:
        part = parts[index]
        part = part.replace('\'','')
        index += 1
        final.append(re.escape(part))
        
        if index == limit:
            break
        
        final.append('[ -_]+')
        continue
    
    search_pattern = re.compile(''.join(final), re.I)
    
    best_found = None
    best_start = 9999
    for track in CHESUTO_BGM_TRACKS_SORTED:
        parsed = search_pattern.search(track.source_name)
        if parsed is None:
            continue
        
        parsed_start = parsed.start()
        
        if parsed_start > best_start:
            continue
        
        if parsed_start < best_start:
            best_found = track
            best_start = parsed_start
            continue
        
        # last case both starts are equal
        # lowest length name wins
        if len(track.display_name) < len(track.display_name):
            best_found = track
            best_start = parsed_start
            continue
        
        # No other optimal case to check.
        continue
    
    return best_found

def get_random_bgm():
    if CHESUTO_BGM_TRACKS_SORTED:
        selected = choice(CHESUTO_BGM_TRACKS_SORTED)
    else:
        selected = None
    
    return selected

async def bgminfo_description(command_context):
    return Embed('bgminfo', (
        'Shows up the given bgm\'s description..\n'
        f'Usage: `{command_context.prefix}bgminfo <name>`\n'
        '\n'
        'Note that the given name can be also given as the position of the track.'
            ), color=COLOR__FLAN_HELP)

async def bgminfo_command(command_context, content):
    if not content:
        await bgminfo_description(command_context)
        return
    
    bgm = get_bgm(content)
    
    if bgm is None:
        title = 'Nothing found.'
        description = None
    else:
        title = bgm.display_name
        description = bgm.description
    
    embed = Embed(title, description, color=CHESUTO_COLOR)
    await command_context.client.message_create(command_context.message.channel, embed=embed)

Flan.commands(bgminfo_command, name='bgminfo', description=bgminfo_description, category='VOICE')

BGM_NOTE = 'Note: If a bgm\'s name has no specified route, it highly likely belongs in the good route.\n\n'

@Flan.commands.from_class
class bgms:
    async def command(client, message):
        chunks = []
        actual_chunk = [BGM_NOTE]
        index = 0
        limit = len(CHESUTO_BGM_TRACKS_SORTED)
        collected = 0
        while True:
            if index == limit:
                break
            
            actual = CHESUTO_BGM_TRACKS_SORTED[index].display_name
            index += 1
            actual_chunk.append(repr(index))
            actual_chunk.append('.: ')
            actual_chunk.append(actual)
            actual_chunk.append('\n')
            
            collected += 1
            if collected == 20:
                del actual_chunk[-1]
                chunks.append(''.join(actual_chunk))
                actual_chunk.clear()
                actual_chunk.append(BGM_NOTE)
                collected = 0
        
        if collected:
            chunks.append(''.join(actual_chunk))
        
        actual_chunk = None
        
        embeds = []
    
        limit = len(chunks)
        index = 0
        while index < limit:
            embed = Embed('Chesuto BGMs:', color=COLOR__FLAN_HELP, description=chunks[index])
            index += 1
            embed.add_footer(f'page {index}/{limit}')
            embeds.append(embed)
        
        await Pagination(client, message.channel, embeds)
    
    category = 'VOICE'
    
    async def description(command_context):
        return Embed('bgms', (
            'Lists the chesuto bgms.\n'
            f'Usage: `{command_context.prefix}bgms`'
            ), color=COLOR__FLAN_HELP)


def check_has_cards_role(message):
    user = message.author
    if user.is_bot:
        return False
    
    if user.has_role(CARDS_ROLE):
        return True
    
    return False

SET_BGM_NAME_EMOJI_OK     = BUILTIN_EMOJIS['ok_hand']
SET_BGM_NAME_EMOJI_CANCEL = BUILTIN_EMOJIS['x']
SET_BGM_NAME_EMOJI_EMOJIS = (SET_BGM_NAME_EMOJI_OK, SET_BGM_NAME_EMOJI_CANCEL)

def check_reaction_cards_role(event):
    if event.emoji not in SET_BGM_NAME_EMOJI_EMOJIS:
        return False
    
    user = event.user
    if user.is_bot:
        return False
    
    if user.has_role(CARDS_ROLE):
        return True
    
    return False

async def set_bgm_name_description(command_context):
    return Embed('set-bgm-name', (
        'Changes a bgm\'s name\n'
        f'Usage: `{command_context.prefix}set-bgm-name <bgm name>`\n'
        'After it please define the new name and react with the OK emoji.'
        ), color=COLOR__FLAN_HELP).add_footer(
            f'You must have `{CARDS_ROLE}` role to use this command.')

@Flan.commands(checks=checks.has_role(CARDS_ROLE), category='VOICE', description=set_bgm_name_description)
async def set_bgm_name(client, message, content):
    bgm = get_bgm(content)
    
    if bgm is None:
        await client.message_create(message.channel, embed=Embed(None, '*Nothing found.*', CHESUTO_COLOR))
        return
    
    embed = Embed(f'Renaming: *{bgm.display_name}*', bgm.description, color=CHESUTO_COLOR) \
        .add_footer('Your next message will be captured as the new display name of the bgm.')
    
    message = await client.message_create(message.channel, embed=embed)
    
    try:
        response = await wait_for_message(client, message.channel, check_has_cards_role, 300.0)
    except TimeoutError:
        content = None
        footer = 'Timeout occurred.'
    else:
        content = response.content
        if len(content) > 100:
            content = None
            footer = '*That\'s pretty long*. That\'s what she said. Please give a display name with maximum of 100 ' \
                     'characters.'
        else:
            footer = f'Are you sure to set the bgm\'s display name as: {content!r}?'
    
    embed.add_footer(footer)
    await client.message_edit(message, embed=embed)
    if content is None:
        return
    
    if message.channel.cached_permissions_for(client).can_manage_messages:
        try:
            await client.message_delete(response)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            raise
    
    for emoji_ in SET_BGM_NAME_EMOJI_EMOJIS:
        await client.reaction_add(message, emoji_)
    
    try:
        event = await wait_for_reaction(client, message, check_reaction_cards_role, 300.)
    except TimeoutError:
        emoji_ = None
    else:
        emoji_ = event.emoji
    
        if message.channel.cached_permissions_for(client).can_manage_messages:
            try:
                await client.reaction_clear(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        return
                
                raise
    
    if emoji_ is None:
        footer = 'Timeout occurred.'
    elif emoji_ is SET_BGM_NAME_EMOJI_OK:
        BGM_NAMES[bgm.source_name] = content
        await write_bgm_names()
        bgm.display_name = content
        footer = 'Rename done.'
    else:
        footer = 'Rename cancelled.'
    
    embed.add_footer(footer)
    await client.message_edit(message, embed=embed)
