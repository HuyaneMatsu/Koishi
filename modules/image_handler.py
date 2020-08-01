# -*- coding: utf-8 -*-
import re, os, functools
from io import BytesIO

from hata import is_mention, ReuAsyncIO, AsyncIO, Embed, eventlist, Color
from hata.ext.commands import Command, checks

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD=True
except ImportError:
    UPLOAD=False

from tools import choose

splitext=os.path.splitext
join=os.path.join

IMAGE_COLOR = Color(0x5dc66f)
IMAGE_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(IMAGE_COMMANDS)

def teardown(lib):
    Koishi.commands.unextend(IMAGE_COMMANDS)
    
IMAGES=[]
VIDS=[]
ALL=[]

ITGHL={}
IMAGE_STATISTICS={}

class image_details(set):
    __slots__ = ('path',)
    def __init__(self,path):
        set.__init__(self)

        name,ext=splitext(path)
        
        ext=ext[1:]
        if ext in image_formats:
            IMAGES.append(self)
        elif ext in video_formats:
            VIDS.append(self)

        ALL.append(self)
        
        tags=name.split('_')
        del tags[0]

        self.path=path
        for tag in tags:
            self.add(tag)
            
    def hastags(self,tags):
        for tag in tags:
            if tag not in self:
                return False
        return True
    
    def add(self,value):
        try:
            hashresult=ITGHL[value]
        except KeyError:
            hashresult=len(ITGHL)
            ITGHL.setdefault(value,hashresult)
        try:
            IMAGE_STATISTICS[value]+=1
        except KeyError:
            IMAGE_STATISTICS[value]=1
        
        set.add(self,hashresult)
        
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.path}>'
    
    __str__=__repr__

IMAGE_TAG_PAT = ITGHL['pat'] = 0
IMAGE_TAG_HUG = ITGHL['hug'] = 1

image_formats={'jpg','png','bmp','jpeg'}
video_formats={'mp4','gif'}

IMAGE_PATH=join(os.path.abspath('.'),'images')

def load_images():
    for filename in os.listdir(IMAGE_PATH):
        image_details(filename)

load_images()

async def image_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    embed = Embed('image',(
        'I ll search images by tags from my collection, '
        'then send 1 of the results.\n'
        f'Usage : `{prefix}image (count) (any / pic / vid) (index (hex) *n*) <tag_1> <tag_2> ...`\n'
        'If `count` is passed, I ll count how much image there is with that '
        'combination. *Count does not goes with `index`*\n'
        'With Passing `any`, `pic` or `vid` keywords you can define, '
        'if you wanna search anything (default), between normal images or '
        'between animated ones.\n'
        'By passing `index`, then a number, you can define which one result '
        'You want from the found ones. If you do `index hex`, I ll expect '
        'a hexadecimal number.\n'
        'You can pass any amount of tags, mentions are ignored.'
            ), color=IMAGE_COLOR)
    await client.message_create(message.channel, embed=embed)


async def upload_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    embed = Embed('upload',(
        'You can can upload images with tags, which you can access with the '
        f'{prefix}image` command after.\n'
        f'Usage : `{prefix}upload <tag_1> <tag_2> ...`\n'
        'If you mention anyone, I ll check her messages, instead of your, '
        'my dear.\n I look up the last 26 messages searching for an '
        'attachment.\n'
        'You can pass any amount of tags, mentions are ignored.'
            ), color=IMAGE_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel, embed=embed)

RESERVED_TAGS={'any','vid','pic','count','index','hex',}

@IMAGE_COMMANDS(category='UTILITY',description=image_description)
async def image(client,message,content):
    result=process_on_command_image(content)
    if type(result) is str:
        await client.message_create(message.channel,result)
    else:
        with client.keep_typing(message.channel):
            with (await ReuAsyncIO(join(IMAGE_PATH,result.path))) as image:
                await client.message_create(message.channel,file=image)


def process_on_command_image(content):
    content=[x.lower() for x in re.findall(r'\S+',content) if not is_mention(x)]
    limit=len(content)
    if limit==0:
        return 'Need tags!'
    
    index=0
    count=False
    value=content[index]
    if value=='count':
        count=True
        index+=1
    
    if index<limit:
        value=content[index]
        try:
            search_from_index=('any','vid','pic').index(value)
        except ValueError:
            search_from=ALL
        else:
            search_from=(ALL,VIDS,IMAGES)[search_from_index]
            index+=1
    else:
        search_from=ALL

    by_index=False
    if index<limit:
        value=content[index]
        if value=='index':
            if count:
                return '"count" and "index" cant be used at the same time BAKA!'

            by_index=True
            
            index+=1
            
            if index==limit:
                return '"index" needs after it a number!'

            value=content[index]
            if value=='hex':
                index+=1
                if index==limit:
                    return '"hex" needs after it a number!'
                value=content[index]
                try:
                    number=int(value,16)
                    index+=1
                except ValueError:
                    return f'Falied to convert "{value}" to integer with base 16'

            else:
                try:
                    number=int(value)
                    index+=1
                except ValueError:
                    return f'Falied to convert "{value}" to integer.'
                
            if number<0:
                return 'Only positivity pls!'

    if index==limit:
        if count:
            return str(len(search_from))
        elif by_index:
            if index<len(search_from):
                return search_from[number]
            else:
                return 'I could not find any image with that criteria.'
        else:
            #must have at least 1 vid and img
            return choose(search_from)

    left=limit-index-1

    if left==0:
        try:
            value=ITGHL[content[index]]
        except KeyError:
            if count:
                return '0'
            else:
                return 'No result.'
            
        if count:
            number=0
            for image in search_from:
                if value in image:
                    number+=1
            return str(number)
        
        elif by_index:
            for image in search_from:
                if value in image:
                    if number==0:
                        return image
                    else:
                        number-=1
            return 'Out of index or no result.'
        
        else:
            results=[]
            for image in search_from:
                if value in image:
                    results.append(image)
            if results:
                return choose(results)
            else:
                return 'Sowwy, no result.'
    else:
        try:
            values={ITGHL[x] for x in content[index:]}
        except KeyError:
            if count:
                return '0'
            else:
                return 'No result.'
        
        if count:
            number=0
            for image in search_from:
                if values.issubset(image):
                    number+=1
            return str(number)
        
        elif by_index:
            for image in search_from:
                if values.issubset(image):
                    if number==0:
                        return image
                    else:
                        number-=1
            return 'Sowwy, no result or out of index.'
        
        else:
            results=[]
            for image in search_from:
                if values.issubset(image):
                    results.append(image)
            if results:
                return choose(results)
            else:
                return 'Sowwy, no result.'


@IMAGE_COMMANDS(category='UTILITY',checks=[checks.owner_only()],description=upload_description)
async def upload(client,message,content):
    if (not UPLOAD):
        await client.message_create(message.channel,
            'Upload is not supported, PIL library not found.')
        return
    
    with client.keep_typing(message.channel):
        result = await process_on_command_upload(client,message,content)
        await client.message_create(message.channel,result)

async def process_on_command_upload(client,message,content):
    tags=[x.lower() for x in re.findall(r'\S+',content) if not is_mention(x)]

    source=message.author
    if message.user_mentions is not None:
        for mention in message.user_mentions:
            if mention!=client:
                source=mention
    
    for tag in tags:
        if tag in RESERVED_TAGS:
            return f'Reserved tag: {tag}'
    
    result=None
    for msg in (await client.messages_in_range(message.channel,end=26)):
        if msg.author==source and msg.attachments:
            result=msg.attachments[0]
            break
    
    if not result:
        return 'Huh?'
    
    filename=result.name
    
    index=filename.rfind('.')
    if index<0:
        return
    ext=filename[index+1:].lower()
    
    if ext in image_formats:
        img=True
    elif ext in video_formats:
        img=False
    else:
        return 'Unknown image format'
    
    data = await client.download_attachment(result)
    
    index=f'{(len(IMAGES)+len(VIDS)):08X}'
    if img:
        path=f'{index}_{"_".join(tags)}.png'
        filename=join(IMAGE_PATH,path)
        if ext!='png':
            #we save everything in png, ~~rasism~~
            if ext in ('jpg','jpeg'):
                image_type=image_type_JPG
            elif ext=='bmp':
                image_type=image_type_BMP
            image=object.__new__(image_type)
            image.fp=BytesIO(data)
            image.info={}
            image.palette=None
            image.im=None
            image.filename=None
            image._exclusive_fp=None
            image.decoderconfig=()
            image.decodermaxblock=65536
            image.readonly=False
            image._exif=None
            image.pyaccess = None
            image._open()
            await client.loop.run_in_executor(functools.partial(image.save,filename))
        else:
            with (await AsyncIO(filename,'wb')) as file:
                await file.write(data)
    else:
        path=f'{index}_{"_".join(tags)}.{ext}'
        filename=join(IMAGE_PATH,path)
        with (await AsyncIO(filename,'wb')) as file:
            await file.write(data)
        
    image_details(path)
    
    return 'Done Masuta~!'

def tandom_with_tag(tag):
    results = []
    for image in ALL:
        if tag in image:
            results.append(image)
    
    if results:
        result = choose(results)
    else:
        result = None
    
    return result

@IMAGE_COMMANDS.from_class        
class pat:
    async def command(client, message):
        image = tandom_with_tag(IMAGE_TAG_PAT)
        
        if image is None:
            await client.message_create(message.channel, 'No patting image is added :\'C')
        else:
            with client.keep_typing(message.channel):
                with (await ReuAsyncIO(join(IMAGE_PATH, image.path))) as file:
                    await client.message_create(message.channel, file=file)
    
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        
        embed = Embed('pat',(
            'Pat pat pat pat!\n'
            f'Usage : `{prefix}pat`'
            ), color=IMAGE_COLOR)
        
        await client.message_create(message.channel, embed=embed)

@IMAGE_COMMANDS.from_class
class hug:
    async def command(client, message):
        image = tandom_with_tag(IMAGE_TAG_HUG)
        
        if image is None:
            await client.message_create(message.channel, 'No hugging image is added :\'C')
        else:
            with client.keep_typing(message.channel):
                with (await ReuAsyncIO(join(IMAGE_PATH, image.path))) as file:
                    await client.message_create(message.channel, file=file)
    
    category = 'UTILITY'
    
    async def description(client, message):
        prefix = client.command_processer.get_prefix_for(message)
        
        embed = Embed('hug',(
            'Huh.. Huggu? HUGG YOUUU!!!\n'
            f'Usage : `{prefix}hug`'
            ), color=IMAGE_COLOR)
        
        await client.message_create(message.channel, embed=embed)
