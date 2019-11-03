# -*- coding: utf-8 -*-
import re, os, functools
from io import BytesIO

from hata.others import is_mention
from hata.channel import messages_till_index
from hata.ios import ReuAsyncIO,AsyncIO
from hata.embed import Embed

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD=True
except ImportError:
    UPLOAD=False

from help_handler import KOISHI_HELP_COLOR, KOISHI_HELPER
from tools import choose

splitext=os.path.splitext
join=os.path.join

IMAGES=[]
VIDS=[]
ALL_img=[]

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

        ALL_img.append(self)
        
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
    
image_formats={'jpg','png','bmp','jpeg'}
video_formats={'mp4','gif'}

IMAGE_PATH=join(os.path.abspath('.'),'images')

def load_images():
    for filename in os.listdir(IMAGE_PATH):
        image_details(filename)

load_images()

async def _help_image(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('image',(
        'I ll search images by tags from my collection, '
        'then send 1 of the results.\n',
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
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('image',_help_image)

async def _help_upload(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('upload',(
        'You can can upload images with tags, which you can access with the '
        f'{prefix}image` command after.\n'
        f'Usage : `{prefix}upload <tag_1> <tag_2> ...`\n'
        'If you mention anyone, I ll check her messages, instead of your, '
        'my dear.\n I look up the last 26 messages searching for an '
        'attachment.\n'
        'You can pass any amount of tags, mentions are ignored.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('upload',_help_upload,KOISHI_HELPER.check_is_owner)


RESERVED_TAGS={'any','vid','pic','count','index','hex',}

async def on_command_image(client,message,content):
    result=process_on_command_image(content)
    if type(result) is str:
        await client.message_create(message.channel,result)
    else:
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
            search_from=ALL_img
        else:
            search_from=(ALL_img,VIDS,IMAGES)[search_from_index]
            index+=1
    else:
        search_from=ALL_img

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

async def on_command_upload(client,message,content):
    if (not UPLOAD) or (not client.is_owner(message.author)):
        return

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
    for msg in (await messages_till_index(client,message.channel,end=26)):
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
        
