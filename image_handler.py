import re
from random import randint as random
import os
from io import BytesIO
from help_handler import HELP
from pers_data import SUPREME_LEADER
from discord_uwu.others import is_mention
from discord_uwu.dereaddons_local import any_to_any
from discord_uwu.channel import get_messages

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD=True
except ImportError:
    UPLOAD=False

IMAGES=[]
VIDS=[]
ALL_img=[]

ITGHL={}
IMAGE_STATISTICS={}

class image_details(set):
    __slots__ = ['path']
    def __init__(self,iterable,path):
        set.__init__(self)
        self.path=path
        for x in iterable:
            self.add(x)
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

image_path=os.path.abspath('.')+'\\images\\'
def load_images():
    global IMAGES,VIDS
    image_statistix={}
    splitext=os.path.splitext
    
    for filename in os.listdir(image_path):
        name,ext=splitext(filename)
        ext=ext[1:]
        tags=name.split('_')
        del tags[0]
        if ext in image_formats:
            new=image_details(tags,filename)
            IMAGES.append(new)
        elif ext in video_formats:
            new=image_details(tags,filename)
            VIDS.append(new)
        else:
            continue
        ALL_img.append(new)

load_images()

def create_help_images():
    text=[
        'Searches image by tags, uploads 1 of the results.\n',
        'Use tag "count" to see how much possible images are with that tag combination\n',
        'Use tag "vid" for gifs or "any" for images and gifs.\n',
        'Use tag "index ~~hex~~ *n*" to not get random result\n',
        'Count doesnt goes with index\n',
        f'Total images: {len(IMAGES)}. Total vids: {len(VIDS)}\n',
        'Tags: '
            ]
    for key,value in IMAGE_STATISTICS.items():
        text.append(f'{key} - {value}, ')
    HELP['image']=''.join(text)

create_help_images()

RESERVED_TAGS={'any','vid','count','index','hex',}

async def on_command_image(client,message,content):
    result=process_on_command_image(content)
    if type(result)==str:
        await client.message_create(message.channel,result)
    else:
        await client.message_create_path(message.channel,image_path+result.path)
    
    
def process_on_command_image(content):
    #TODO ignore mentions
    content=[x.lower() for x in re.split('[ \t]+',content) if not is_mention(x)]
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


    by_index=False
    if index<limit:
        value=content[index]
        if value=='index':
            if count:
                return '"count" and "index" cant be used at the same time BAKA!'

            by_index=True
            
            index+=1
            
            if index>=limit:
                return '"index" needs after it a number!'

            value=content[index]
            if value=='hex':
                index+=1
                if index>=limit:
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
                return (image_path+result.path,)
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
    if not UPLOAD or message.author.id!=SUPREME_LEADER:
        return

    result = await process_on_command_upload(client,message,content)
    await client.message_create(message.channel,result)
    
async def process_on_command_upload(client,message,content):
    content=[x.lower() for x in split('[ \t]+',content) if not is_mention(x)]

    source=message.author
    if message.mentions:
        for mention in mentions:
            if mention!=client:
                source=mention        
    
    if any_to_any(content,RESERVED_TAGS):
        return f'Reserved tag: {tag}'

    result=None
    for msg in get_messages(client,channel,end=26):
        if msg.author==source and msg.attachments:
            result=msg.attachments[0]
            break
    
    if not result:
        return 'Huh?'


    filename=result.filename
    
    try:    
        ext=filename[filename.index('.')+1:].lower()
    except IndexError:
        return
    
    if ext in image_formats:
        img=True
    elif ext in video_formats:
        img=False
    else:
        return 'Unknown image format'

    data = await client.download_attachment(result)
    
    index=f'{len(IMAGES)+len(VIDS):08X}'
    if img:
        path=f'{index}_{"_".join(tags)}.png'
        IMAGES.append(image_details(tags,path))
        path=image_path+path
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
            image.save(path)
        else:
            file=open(path,'wb')
            file.write(data)
            file.close()
    else:
        path=f'{image_path,index}_{"_".join(tags)}.{ext}'
        VIDS.append(image_details(tags,path))
        path=image_path+path
        file=open(path,'wb')
        file.write(data)
        file.close()
    
    create_help_images()
    
    return 'Done Masuta~!'
        
