# -*- coding: utf-8 -*-
import re
from random import randint as random
import os
from io import BytesIO
from help_handler import HELP
from hata.others import is_mention
from hata.channel import messages_till_index
from hata.ios import ReuAsyncIO,AsyncIO
import functools

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD=True
except ImportError:
    UPLOAD=False

splitext=os.path.splitext
join=os.path.join

IMAGES=[]
VIDS=[]
ALL_img=[]

ITGHL={}
IMAGE_STATISTICS={}

class image_details(set):
    __slots__ = ['path']
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

def create_help_images():
    text=[
        'Searches image by tags, uploads 1 of the results.',
        'Use tag "count" to see how much possible images are with that tag combination',
        'Use tag "pic" for pictures only, "vid" for gifs or "any" for any.',
        'Use tag "index ~~hex~~ *n*" to not get random result',
        'Count doesnt goes with index',
        f'Total images: {len(IMAGES)}. Total vids: {len(VIDS)}',
        'Top Tags: '
            ]
    textlen=sum(len(l) for l in text)+len(text)
    
    items=list(IMAGE_STATISTICS.items())
    items.sort(key=lambda item: item[1],reverse=True)
    
    for index,(key,value) in enumerate(items[:20],1):
        part=f'{index:}.: {key} - {value}'
        newlen=textlen+len(part)+1
        if newlen>2048:
            break
        text.append(part)
        textlen=newlen
        
    HELP['image'].description='\n'.join(text)
    
create_help_images()

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
            return search_from[random(0,len(search_from)-1)]

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
                return results[random(0,len(results)-1)]
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
                return results[random(0,len(results)-1)]
            else:
                return 'Sowwy, no result.'

async def on_command_upload(client,message,content):
    if not UPLOAD or message.author is not client.owner:
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
    create_help_images()
    
    return 'Done Masuta~!'
        
