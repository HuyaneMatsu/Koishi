# -*- coding: utf-8 -*-
import re, os, functools
from io import BytesIO

from hata import is_mention, ReuAsyncIO, AsyncIO, Embed, Color, KOKORO, Lock, Client
from hata.ext.commands import checks, Closer

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD = True
except ImportError:
    UPLOAD = False

UPLOAD_LOCK = Lock(KOKORO)

from bot_utils.tools import choose
from bot_utils.shared import KOISHI_PATH
from bot_utils.command_utils import MESSAGE_CONVERTER_ALL


splitext = os.path.splitext
join = os.path.join

IMAGE_COLOR = Color(0x5dc66f)
Koishi: Client

IMAGES_STATIC = []
IMAGES_ANIMATED = []
IMAGES_ALL = []

ITGHL = {}
IMAGE_STATISTICS = {}

FIND_TAGS_RP = re.compile('\S+')

class image_details(set):
    __slots__ = ('path',)
    def __init__(self, path):
        set.__init__(self)
        
        name, ext = splitext(path)
        
        ext = ext[1:]
        if ext in IMAGE_FORMATS_STATIC:
            IMAGES_STATIC.append(self)
        elif ext in IMAGE_FORMATS_ANIMATED:
            IMAGES_ANIMATED.append(self)

        IMAGES_ALL.append(self)
        
        tags = name.split('_')
        del tags[0]

        self.path = path
        for tag in tags:
            self.add(tag)
            
    def hastags(self, tags):
        for tag in tags:
            if tag not in self:
                return False
        return True
    
    def add(self, value):
        try:
            hashresult = ITGHL[value]
        except KeyError:
            hashresult = len(ITGHL)
            ITGHL.setdefault(value, hashresult)
        try:
            IMAGE_STATISTICS[value] += 1
        except KeyError:
            IMAGE_STATISTICS[value] = 1
        
        set.add(self, hashresult)
        
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.path}>'
    
    __str__ = __repr__

IMAGE_FORMATS_STATIC = {'jpg', 'png', 'bmp', 'jpeg'}
IMAGE_FORMATS_ANIMATED = {'mp4', 'gif'}

IMAGE_PATH = join(KOISHI_PATH, 'images')

for filename in os.listdir(IMAGE_PATH):
    image_details(filename)

async def image_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('image', (
        'I ll search images by tags from my collection, then send 1 of the results.\n'
        f'Usage : `{prefix}image (count) (static / animated) (index (hex) *n*) <tag_1> <tag_2> ...`\n'
        'If `count` is passed, I ll count how much image there is with that combination. *Count does not goes with '
        '`index`*\n'
        'With Passing `any`, `pic` or `vid` keywords you can define, if you wanna search anything (default), between '
        'normal images or between animated ones.\n'
        'By passing `index`, then a number, you can define which one result You want from the found ones. If you do '
        '`index hex`, I ll expect a hexadecimal number.\n'
        'You can pass any amount of tags, mentions are ignored.'
            ), color=IMAGE_COLOR)


async def upload_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('upload', (
        f'You can can upload images with tags, which you can access with the `{prefix}image` command after.\n'
        f'Usage : `{prefix}upload *message* <tag_1> <tag_2> ...`\n'
        'You can pass any amount of tags, mentions are ignored.'
            ), color=IMAGE_COLOR).add_footer(
            'Owner only!')


RESERVED_TAGS = {'animated', 'static', 'count', 'index', 'hex',}

@Koishi.commands(category='UTILITY', description=image_description, checks=checks.guild_only())
async def image(client, message, content):
    result = process_on_command_image(content)
    if type(result) is str:
        await client.message_create(message.channel, result)
    else:
        with client.keep_typing(message.channel):
            with (await ReuAsyncIO(join(IMAGE_PATH, result.path))) as image:
                await client.message_create(message.channel, file=image)


def process_on_command_image(content):
    content = [x.lower() for x in FIND_TAGS_RP.findall(content) if not is_mention(x)]
    limit = len(content)
    index = 0
    
    count = False
    if index < limit:
        value = content[index]
        if value == 'count':
            count = True
            index += 1
    
    if index < limit:
        value = content[index]
        if value == 'animated':
            search_from = IMAGES_ANIMATED
            index += 1
        elif value == 'static':
            search_from = IMAGES_STATIC
            index += 1
        else:
            search_from = IMAGES_ALL
        
    else:
        search_from = IMAGES_ALL
    
    by_index = False
    if index < limit:
        value = content[index]
        if value == 'index':
            if count:
                return '"count" and "index" cant be used at the same time BAKA!'
            
            by_index = True
            
            index += 1
            
            if index == limit:
                return '"index" needs after it a number!'
            
            value = content[index]
            if value == 'hex':
                index += 1
                if index == limit:
                    return '"hex" needs after it a number!'
                value = content[index]
                try:
                    number = int(value, 16)
                    index += 1
                except ValueError:
                    return f'Falied to convert "{value}" to integer with base 16'

            else:
                try:
                    number = int(value)
                    index += 1
                except ValueError:
                    return f'Falied to convert "{value}" to integer.'
                
            if number < 0:
                return 'Only positivity pls!'
    
    if index == limit:
        if count:
            return str(len(search_from))
        elif by_index:
            if number < len(search_from):
                return search_from[number]
            else:
                return 'I could not find any image with that criteria.'
        else:
            # must have at least 1 static and naimated image
            return choose(search_from)
    
    left = limit-index
    
    if left == 0:
        try:
            value = ITGHL[content[index]]
        except KeyError:
            if count:
                return '0'
            else:
                return 'No result.'
            
        if count:
            number = 0
            for image in search_from:
                if value in image:
                    number += 1
            return str(number)
        
        elif by_index:
            for image in search_from:
                if value in image:
                    if number == 0:
                        return image
                    else:
                        number -= 1
            return 'Out of index or no result.'
        
        else:
            results = []
            for image in search_from:
                if value in image:
                    results.append(image)
            if results:
                return choose(results)
            else:
                return 'Sowwy, no result.'
    else:
        try:
            values = {ITGHL[x] for x in content[index:]}
        except KeyError:
            if count:
                return '0'
            else:
                return 'No result.'
        
        if count:
            number = 0
            for image in search_from:
                if values.issubset(image):
                    number += 1
            return str(number)
        
        elif by_index:
            for image in search_from:
                if values.issubset(image):
                    if number == 0:
                        return image
                    else:
                        number -= 1
            return 'Sowwy, no result or out of index.'
        
        else:
            results = []
            for image in search_from:
                if values.issubset(image):
                    results.append(image)
            if results:
                return choose(results)
            else:
                return 'Sowwy, no result.'

@Koishi.commands(category='UTILITY', checks=checks.owner_only(), description=upload_description)
async def upload(client, message, target_message: MESSAGE_CONVERTER_ALL, *tags):
    if UPLOAD:
        tags = [tag.lower() for tag in tags if not is_mention(tag)]
        for tag in tags:
            if tag in RESERVED_TAGS:
                result_message = f'Reserved tag: {tag!r}!'
                break
        else:
            if tags:
                found_image = None
                attachments = target_message.attachments
                if (attachments is not None):
                    for attachment in attachments:
                        filename = attachment.name
                        
                        index = filename.rfind('.')
                        if index < 0:
                            continue
                        
                        extension = filename[index+1:].lower()
                        
                        if extension in IMAGE_FORMATS_STATIC:
                            is_static = True
                        elif extension in IMAGE_FORMATS_ANIMATED:
                            is_static = False
                        else:
                            continue
                        
                        found_image = attachment
                        break
                
                if (found_image is None):
                    embeds = target_message.embeds
                    if (embeds is not None):
                        for embed in embeds:
                            embed_image = embed.image
                            if embed_image is None:
                                continue
                            
                            filename = embed_image.url
                            if filename is None:
                                continue
                            
                            index = filename.rfind('.')
                            if index < 0:
                                continue
                            
                            extension = filename[index+1:].lower()
                            
                            if extension in IMAGE_FORMATS_STATIC:
                                is_static = True
                            elif extension in IMAGE_FORMATS_ANIMATED:
                                is_static = False
                            else:
                                continue
                            
                            found_image = embed_image
                            break
                
                if found_image is None:
                    result_message = 'The given message has no image attached.'
                else:
                    with client.keep_typing(message.channel):
                        async with UPLOAD_LOCK:
                            data = await client.download_attachment(found_image)
                            
                            index = f'{(len(IMAGES_STATIC)+len(IMAGES_ANIMATED)):08X}'
                            if is_static:
                                path = f'{index}_{"_".join(tags)}.png'
                                filename=join(IMAGE_PATH, path)
                                if extension != 'png':
                                    #we save everything in png, ~~rasism~~
                                    if extension in ('jpg', 'jpeg'):
                                        image_type = image_type_JPG
                                    elif extension == 'bmp':
                                        image_type = image_type_BMP
                                    image = object.__new__(image_type)
                                    image.fp = BytesIO(data)
                                    image.info = {}
                                    image.palette = None
                                    image.im = None
                                    image.filename = None
                                    image._exclusive_fp = None
                                    image.decoderconfig = ()
                                    image.decodermaxblock = 65536
                                    image.readonly = False
                                    image._exif = None
                                    image.pyaccess = None
                                    image._open()
                                    await KOKORO.run_in_executor(functools.partial(image.save, filename))
                                else:
                                    with (await AsyncIO(filename, 'wb')) as file:
                                        await file.write(data)
                            else:
                                path = f'{index}_{"_".join(tags)}.{extension}'
                                filename = join(IMAGE_PATH, path)
                                with (await AsyncIO(filename, 'wb')) as file:
                                    await file.write(data)
                            
                            image_details(path)
                        
                    result_message = 'Done Masuta~!'
    
            else:
                result_message = 'Please give tags as well!'
            
    else:
        result_message = 'Upload is not supported, PIL library not found.'
        
    await Closer(client, message.channel, Embed(result_message, color = IMAGE_COLOR))


def random_with_tag(tag):
    results = []
    for image in IMAGES_ALL:
        if tag in image:
            results.append(image)
    
    if results:
        result = choose(results)
    else:
        result = None
    
    return result

def generate_cute_content(client, message, action):
    content = []
    mentions = message.user_mentions
    if mentions is None:
        content.append(client.name)
        content.append(' ')
        content.append(action)
        content.append(' ')
        content.append(message.author.name)
        content.append('.')
    else:
        content.append(message.author.name)
        content.append(' ')
        content.append(action)
        content.append(' ')
        content.append(mentions[0].name)
        if len(mentions) > 1:
            for user in mentions[1:-1]:
                content.append(', ')
                content.append(user.name)
            content.append(' and ')
            content.append(mentions[-1].name)
    
    return ''.join(content)


class image_with_tag:
    __slots__ = ('__name__', 'tag_id', 'name_form__ing', 'name_form__s', '__doc__')
    def __init__(self, name, name_form__ing, name_form__s, docs):
        try:
            tag_id = ITGHL[name]
        except KeyError:
            tag_id = len(ITGHL)
            ITGHL[name] = tag_id
        
        self.tag_id = tag_id
        self.__name__ = name
        self.name_form__ing = name_form__ing
        self.name_form__s = name_form__s
        self.__doc__ = docs
        
    async def __call__(self, client, message):
        image = random_with_tag(self.tag_id)
        
        if image is None:
            await client.message_create(message.channel, f'No {self.name_form__ing} image is added :\'C')
        else:
            embed = Embed(generate_cute_content(client, message, self.name_form__s),
                color=(message.id>>22)&0xffffff).add_image(f'attachment://{os.path.basename(image.path)}')
            
            with client.keep_typing(message.channel):
                with (await ReuAsyncIO(join(IMAGE_PATH, image.path))) as file:
                    await client.message_create(message.channel, embed=embed, file=file)


Koishi.commands(
    image_with_tag('pat', 'patting', 'pats', 'Do you like pats as well?'),
    category = 'UTILITY',
    checks = [checks.guild_only()],
    aliases = ['pet'],
        )

Koishi.commands(
    image_with_tag('hug', 'hugging', 'hugs', 'Huh.. Huggu? HUGG YOUUU!!!'),
    category = 'UTILITY',
    checks = [checks.guild_only()],
        )

Koishi.commands(
    image_with_tag('kiss', 'kissing', 'kisses', 'If you really really like your onee, give her a kiss <3'),
    category = 'UTILITY',
    checks = [checks.guild_only()],
        )

Koishi.commands(
    image_with_tag('slap', 'slapping', 'slaps', 'Slapping others is not nice.'),
    category = 'UTILITY',
    checks = [checks.guild_only()],
        )

Koishi.commands(
    image_with_tag('lick', 'licking', 'licks', 'Licking is a favored activity of cat girls.'),
    category = 'UTILITY',
    checks = [checks.guild_only()],
        )
