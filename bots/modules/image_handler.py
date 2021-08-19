# -*- coding: utf-8 -*-
import re, os, functools
from io import BytesIO

from hata import is_mention, ReuAsyncIO, AsyncIO, Embed, Color, KOKORO, Lock, Client, parse_message_reference, \
    MESSAGES, DiscordException, ERROR_CODES, CHANNELS, Attachment, sanitize_mentions, Permission
from hata.ext.slash import InteractionResponse, abort

try:
    from PIL.BmpImagePlugin import BmpImageFile as image_type_BMP
    from PIL.JpegImagePlugin import JpegImageFile as image_type_JPG
    UPLOAD = True
except ImportError:
    UPLOAD = False

from bot_utils.tools import choose
from bot_utils.shared import PATH__KOISHI, GUILD__NEKO_DUNGEON


SLASH_CLIENT : Client
UPLOAD_LOCK = Lock(KOKORO)

splitext = os.path.splitext
join = os.path.join

IMAGE_COLOR = Color(0x5dc66f)

IMAGES = []

IMAGE_TAG_HASHES = {}
IMAGE_STATISTICS = {}

FIND_TAGS_RP = re.compile('\S+')

class ImageDetail(set):
    __slots__ = ('path', 'animated')
    @classmethod
    def create(cls, path):
        name, ext = splitext(path)
        ext = ext[1:]
        if ext in IMAGE_FORMATS_STATIC:
            animated = False
        elif ext in IMAGE_FORMATS_ANIMATED:
            animated = True
        else:
            return
        
        self = set.__new__(cls)
        self.animated = animated
        set.__init__(self)
        
        tags = name.split('_')
        del tags[0]
        
        self.path = path
        for tag in tags:
            self.add(tag)
        
        IMAGES.append(self)
    
    def has_tags(self, tags):
        for tag in tags:
            if tag not in self:
                return False
        
        return True
    
    def add(self, value):
        try:
            hash_result = IMAGE_TAG_HASHES[value]
        except KeyError:
            hash_result = len(IMAGE_TAG_HASHES)
            IMAGE_TAG_HASHES.setdefault(value, hash_result)
        
        try:
            IMAGE_STATISTICS[value] += 1
        except KeyError:
            IMAGE_STATISTICS[value] = 1
        
        set.add(self, hash_result)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.path}>'
    
    __str__ = __repr__

IMAGE_FORMATS_STATIC = {'jpg', 'png', 'bmp', 'jpeg'}
IMAGE_FORMATS_ANIMATED = {'mp4', 'gif'}

IMAGE_PATH = join(PATH__KOISHI, 'images')

for file_name in os.listdir(IMAGE_PATH):
    ImageDetail.create(file_name)

RESERVED_TAGS = {'animated', 'static', 'count'}

IMAGE_ANY = 0
IMAGE_STATIC = 1
IMAGE_ANIMATED = 2

@SLASH_CLIENT.interactions(is_global=True)
async def image_(client, event,
        tags : ('str', 'Give some tags!') = None,
        type_ : ([
            ('Any', IMAGE_ANY),
            ('static', IMAGE_STATIC),
            ('animated', IMAGE_ANIMATED),
                ], 'Specific image type?') = IMAGE_ANY,
        count : ('bool', 'Do you want to get the amount of images instead?') = False,
        index : ('number', 'Do you want to get a specific indexed image?') = None,
            ):
    """Gets an image from my local storage!"""
    # Check for permissions!
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if client.get_guild_profile_for(guild) is None:
        abort('I must be in the guild to execute this command.')
    
    hashes = None
    missing_tag = False
    
    if (tags is not None) and tags:
        for tag in FIND_TAGS_RP.findall(tags):
            if is_mention(tag):
                continue
            
            tag = tag.lower()
            
            try:
                hash_ = IMAGE_TAG_HASHES[tag]
            except KeyError:
                missing_tag = True
                break
            
            if hashes is None:
                hashes = set()
            
            hashes.add(hash_)
            continue
    
    image_details = []
    
    if not missing_tag:
        for image_detail in IMAGES:
            if type_ == IMAGE_ANY:
                pass
            elif type_ == IMAGE_STATIC:
                if image_detail.animated:
                    continue
            else: # elif type_ == IMAGE_ANIMATED:
                if not image_detail.animated:
                    continue
            
            if (hashes is not None) and (not hashes.issubset(image_detail)):
                continue
                
            image_details.append(image_detail)
    
    if count:
        return str(len(image_details))
    
    if not image_details:
        return 'Sowwy, no result.'
    
    if index is None:
        image_detail = choose(image_details)
    else:
        image_details_length = len(image_details)
        if (index < 0) or (index >= image_details_length):
            abort('Index: `{index!r}` out of the expected range `[0:{image_details_length}]`.')
        
        image_detail = image_details[index]
    
    image = await ReuAsyncIO(join(IMAGE_PATH, image_detail.path))
    return InteractionResponse(file=image)


PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def upload(client, event,
        message : ('str', 'Link to the message'),
        tags : ('str', 'Give some tags!'),
            ):
    """Uploads an image to my local storage. (Bot owner only!)"""
    # Check for permissions!
    if not client.is_owner(event.user):
        yield Embed('Ohoho', 'Bot owner only!', color=IMAGE_COLOR)
        return
    
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command', color=IMAGE_COLOR)
        return
    
    if client.get_guild_profile_for(guild) is None:
        yield Embed('Error', 'I must be in the guild to execute this command.', color=IMAGE_COLOR)
        return
    
    if not event.channel.cached_permissions_for(client)&PERMISSION_MASK_MESSAGING:
        yield Embed('Permission denied', 'I need `send messages` permission to execute this command.',
            color=IMAGE_COLOR)
        return
    
    if not UPLOAD:
        yield Embed('Ayaya', 'Upload is not supported, PIL library not found.', color=IMAGE_COLOR)
        return
    
    image_tags = []
    for tag in FIND_TAGS_RP.findall(tags):
        if is_mention(tag):
            continue
        
        tag = tag.lower()
        if tag in image_tags:
            continue
        
        image_tags.append(tag)
        continue
    
    if not tags:
        yield Embed('Ayaya', 'Please give tags as well!', color=IMAGE_COLOR)
        return
    
    message_reference = parse_message_reference(message)
    if message_reference is None:
        yield Embed('Error', 'Could not identify the message.', color=IMAGE_COLOR)
        return
    
    guild_id, channel_id, message_id = message_reference
    try:
        message = MESSAGES[message_id]
    except KeyError:
        if channel_id:
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                yield Embed('Ohoho', 'I have no access to the channel.', color=IMAGE_COLOR)
                return
        else:
            channel = event.channel
        
        if not channel.cached_permissions_for(client).can_read_message_history:
            yield Embed('Ohoho', 'I have no permission to get that message.', color=IMAGE_COLOR)
            return
        
        yield
        
        try:
            message = client.message_get(channel, message_id)
        except ConnectionError:
            # No internet
            return
        except DiscordException as err:
            if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                        ):
                # The message is already deleted.
                yield Embed('OOf', 'The referenced message is already yeeted.', color=IMAGE_COLOR)
                return
            
            if err.code == ERROR_CODES.missing_access: # client removed
                # This is not nice.
                return
            
            if err.code == ERROR_CODES.missing_permissions: # permissions changed meanwhile
                yield Embed('Ohoho', 'I have no permission to get that message.', color=IMAGE_COLOR)
                return
            
            raise
    
    attachments = message.attachments
    found_images = []
    if (attachments is not None):
        for attachment in attachments:
            file_name = attachment.name
            
            index = file_name.rfind('.')
            if index < 0:
                continue
            
            extension = file_name[index+1:].lower()

            if not ((extension in IMAGE_FORMATS_STATIC) or (extension in IMAGE_FORMATS_ANIMATED)):
                continue
            
            found_images.append(attachment)
            continue
    
    embeds = message.embeds
    if (embeds is not None):
        for embed in embeds:
            embed_image = embed.image
            if embed_image is None:
                continue
            
            file_name = embed_image.url
            if file_name is None:
                continue
            
            index = file_name.rfind('.')
            if index < 0:
                continue
            
            extension = file_name[index+1:].lower()

            if not ((extension in IMAGE_FORMATS_STATIC) or (extension in IMAGE_FORMATS_ANIMATED)):
                continue
            
            found_images.append(embed_image)
            continue
    
    found_images_count = len(found_images)
    if found_images_count != 1:
        if found_images_count:
            description_parts = ['Multiple attachments found:\n']
            
            for index, found_image in zip(range(1, 6), found_images):
                image_url = found_image.url
                if len(image_url) > 200:
                    image_url = image_url[:200]+' ...'
                
                description_parts.append(str(index))
                description_parts.append('.: `')
                description_parts.append(image_url)
                description_parts.append('`\n')
                
            if found_images_count > 5:
                description_parts.append('And ')
                description_parts.append(str(found_images_count-5))
                description_parts.append('more.')
            else:
                del description_parts[-1]
            
            description = ''.join(description_parts)
        else:
            description = 'No images found.'
        
        yield Embed('Ayaya', description, color=IMAGE_COLOR)
        return
    
    yield
    
    found_image = found_images[0]
    
    async with UPLOAD_LOCK:
        data = await client.download_attachment(found_image)
        if isinstance(found_image, Attachment):
            file_name = found_image.name
        else:
            file_name = found_image.url
        
        extension = file_name[file_name.rfind('.')+1:].lower()
        
        file_path_parts = [len(IMAGES).__format__('08X'), '_']
        
        index = 0
        limit = len(image_tags)
        while True:
            tag = image_tags[index]
            file_path_parts.append(tag)
            
            index += 1
            if index == limit:
                break
            
            file_path_parts.append('_')
        
        file_path_parts.append('.')
        
        if extension in IMAGE_FORMATS_ANIMATED:
            file_path_extension = extension
        else:
            file_path_extension = 'png'
        
        file_path_parts.append(file_path_extension)
        
        file_path = ''.join(file_path_parts)
        full_file_path = join(IMAGE_PATH, file_path)
        
        if (extension not in IMAGE_FORMATS_ANIMATED) and (extension != 'png'):
            if extension in ('jpg', 'jpeg'):
                image_type = image_type_JPG
            elif extension == 'bmp':
                image_type = image_type_BMP
            image = object.__new__(image_type)
            image.fp = BytesIO(data)
            image.info = {}
            image.palette = None
            image.im = None
            image.file_name = None
            image._exclusive_fp = None
            image.decoderconfig = ()
            image.decodermaxblock = 65536
            image.readonly = False
            image._exif = None
            image.pyaccess = None
            image._open()
            await KOKORO.run_in_executor(functools.partial(image.save, full_file_path))
        else:
            with (await AsyncIO(full_file_path, 'wb')) as file:
                await file.write(data)
        
        ImageDetail.create(file_path)
    
    yield Embed('Done Masuta!!!', color=IMAGE_COLOR)
    return

def random_with_tag(tag):
    results = []
    for image in IMAGES:
        if tag in image:
            results.append(image)
    
    if results:
        result = choose(results)
    else:
        result = None
    
    return result


class ImageWithTag:
    __slots__ = ('tag_id', 'name_form__ing', 'name_form__s')
    def __init__(self, name, name_form__ing, name_form__s):
        try:
            tag_id = IMAGE_TAG_HASHES[name]
        except KeyError:
            tag_id = len(IMAGE_TAG_HASHES)
            IMAGE_TAG_HASHES[name] = tag_id
        
        self.tag_id = tag_id
        self.name_form__ing = name_form__ing
        self.name_form__s = name_form__s
        
    async def __call__(self, client, event,
            message : ('str', 'Additional message to send?') = '',
                ):
        # Check for permissions!
        guild = event.guild
        if guild is None:
            abort('Guild only command')
        
        if client.get_guild_profile_for(guild) is None:
            abort('I must be in the guild to execute this command.')
        
        image = random_with_tag(self.tag_id)
        
        if image is None:
            abort(f'No {self.name_form__ing} image is added :\'C')
        
        if message:
            first_word = event.user.name
            last_word = sanitize_mentions(message, event.guild)
            # Security goes brrr
            if len(last_word) > 200:
                last_word = last_word[:200] + ' ...'
        else:
            first_word = client.name
            last_word = event.user.name
        
        title = f'{first_word} {self.name_form__s} {last_word}.'
        
        embed = Embed(title, color=(event.id>>22)&0xffffff) \
            .add_image(f'attachment://{os.path.basename(image.path)}')
        
        file = await ReuAsyncIO(join(IMAGE_PATH, image.path))
        return InteractionResponse(embed=embed, file=file)

for name, name_form__ing, name_form__s, description in (
        ('pat', 'patting', 'pats', 'Do you like pats as well?'),
        ('hug', 'hugging', 'hugs', 'Huh.. Huggu? HUGG YOUUU!!!'),
        ('kiss', 'kissing', 'kisses', 'If you really really like your onee, give her a kiss <3'),
        ('slap', 'slapping', 'slaps', 'Slapping others is not nice.'),
        ('lick', 'licking', 'licks', 'Licking is a favored activity of cat girls.'),
            ):

    SLASH_CLIENT.interactions(ImageWithTag(name, name_form__ing, name_form__s),
        name=name, description=description, is_global=True)
