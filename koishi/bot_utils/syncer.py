import os, re, sys
from os.path import join, isdir, isfile, getmtime, exists
from os import mkdir as make_dir
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from config import HATA_PATH, SCARLETIO_PATH

from hata import KOKORO, Embed, DiscordException
from scarletio import Lock, Task, ReuAsyncIO, AsyncIO, TaskGroup, render_exception_into_async
from hata.ext.command_utils import wait_for_message, Pagination

from .constants import CHANNEL__SYSTEM__SYNC, PATH__KOISHI

CHUNK_SIZE = 128 * 1024 # 128 KB

HATA_HEAD_NAME = 'hata'
KOISHI_HEAD_NAME = 'koishi'
SCARLETIO_HEAD_NAME = 'scarletio'

RELATIONS = {
    HATA_HEAD_NAME: HATA_PATH,
    KOISHI_HEAD_NAME: PATH__KOISHI,
    SCARLETIO_HEAD_NAME: SCARLETIO_PATH,
}

DATETIME_FORMAT_CODE = '%Y.%m.%d-%H:%M:%S'
DATETIME_RP = re.compile('(\\d{4})\\.(\\d{2})\\.(\\d{2})\\-(\\d{2})\\:(\\d{2})\\:(\\d{2})')

IGNORED_NAMES = frozenset((
    '__pycache__',
    '.idea',
    '_sqlite.db',
    'images',
    'library',
    'chesuto_data',
    'channel_names.csv',
    '.git',
))

IGNORED_EXTENSIONS = frozenset((
    'png',
))


def flatten_directory(path, name, access_path):
    access_path.append(name)
    
    directory = os.listdir(path)
    for name in directory:
        if name in IGNORED_NAMES:
            continue
        
        directory_path = join(path, name)
        if isdir(directory_path):
            yield from flatten_directory(directory_path, name, access_path.copy())
            continue
        
        if isfile(directory_path):
            if name.rpartition('.')[2] in IGNORED_EXTENSIONS:
                continue
            
            yield File(directory_path, name, access_path)
            continue


class File:
    __slots__ = ('path', 'modified', 'name', 'access_path',)
    
    def __init__(self, path, name, access_path):
        self.path = path
        self.modified = DateTime.fromtimestamp(getmtime(path), TimeZone.utc)
        self.name = name
        self.access_path = access_path


def flatten_paths():
    for name, path in RELATIONS.items():
        yield from flatten_directory(path, name, [])
        

def check_approved(message):
    return (message.content == REQUEST_APPROVED)

def check_received(message):
    return (message.content == RECEIVED)

class check_any:
    __slots__ = ('partner', )
    def __init__(self, partner):
        self.partner = partner
    
    def __call__(self, message):
        if message.author is self.partner:
            return True
        
        return False


INITIAL_MESSAGE = 'message_initial'
REQUEST_APPROVED = 'message_approved'
RECEIVED = 'message_received'
SYNC_DONE = 'message_done'

SYNC_LOCK = Lock(KOKORO)

def get_modified_files(days_allowed):
    days_allowed = TimeDelta(days = days_allowed)
    should_send = []
    
    min_time = DateTime.now(TimeZone.utc) - days_allowed
    for file in flatten_paths():
        if file.modified > min_time:
            should_send.append(file)
    
    return should_send


async def send_file(client, file):
    with (await ReuAsyncIO(file.path)) as io:
        file_name_parts = []
        for part in file.access_path:
            file_name_parts.append(part)
            file_name_parts.append('.')
        
        if file_name_parts:
            del file_name_parts[-1]
        
        
        file_name_parts.append(':')
        file_name_parts.append(file.name)
        
        file_name = ''.join(file_name_parts)
        
        try:
            await client.message_create(CHANNEL__SYSTEM__SYNC, file_name, file = io)
        except DiscordException as err:
            if err.code == 40005:
                sys.stderr.write(repr(err))
                sys.stderr.write('\n')
                return False
            
            raise
    
    return True


async def request_sync(client, days_allowed):
    async with SYNC_LOCK:
        
        await client.message_create(CHANNEL__SYSTEM__SYNC, INITIAL_MESSAGE)
        
        try:
            await wait_for_message(client, CHANNEL__SYSTEM__SYNC, check_approved, 30.)
        except TimeoutError:
            sys.stderr.write('Sync request failed, timeout.\n')
            return
        
        files = get_modified_files(days_allowed)
        
        for file in files:
            sending_task = Task(KOKORO, send_file(client, file))
            response_task = wait_for_message(client, CHANNEL__SYSTEM__SYNC, check_received, 60.)
            
            await TaskGroup(KOKORO, [sending_task, response_task]).wait_all()
            
            try:
                sent = sending_task.get_result()
            except GeneratorExit:
                response_task.cancel()
                raise
            
            except BaseException as err:
                # Cancel it, so no double exception will be dropped.
                response_task.cancel()
                sys.stderr.write(f'Sync failed, {err!r}.\n')
                raise
            
            if sent:
                try:
                    response_task.get_result()
                except TimeoutError:
                    sys.stderr.write('Sync failed, timeout.\n')
                    return
            else:
                response_task.cancel()
                continue
        
        await client.message_create(CHANNEL__SYSTEM__SYNC, SYNC_DONE)


async def receive_sync(client, partner):
    try:
        async with SYNC_LOCK:
            # some delay is needed or Koishi might answer too fast.
            message_to_send = REQUEST_APPROVED
            
            while True:
                Task(KOKORO, client.message_create(CHANNEL__SYSTEM__SYNC, message_to_send))
                
                try:
                    message = await wait_for_message(client, CHANNEL__SYSTEM__SYNC, check_any(partner), 60.)
                except TimeoutError:
                    sys.stderr.write('Sync request failed, timeout.\n')
                    return
                
                content = message.content
                if content is None:
                    continue
                
                if content == SYNC_DONE:
                    break
                
                if content == INITIAL_MESSAGE:
                    continue
                
                split = content.split(':')
                if len(split) != 2:
                    await client.message_create(
                        CHANNEL__SYSTEM__SYNC,
                        f'Could not split content: {content!r}',
                    )
                    continue
                
                path_full, file_name = split
                
                path_parts = path_full.split('.')
                if not path_parts:
                    sys.stderr.write('Empty content received, aborting sync.\n')
                    return
                
                source_path = path_parts[0]
                try:
                    source_path = RELATIONS[source_path]
                except KeyError:
                    sys.stderr.write(f'Source path not found: {source_path!r}, aborting sync.\n')
                    return
                
                for path_part in path_parts[1:]:
                    source_path = join(source_path, path_part)
                    if not exists(source_path):
                        make_dir(source_path)
                
                attachments = message.attachments
                if (attachments is not None):
                    attachment = attachments[0]
                    binary = await client.download_attachment(attachment)
                    if binary is None:
                        sys.stdout.write(f'{attachment!r} yielded empty binary.\n')
                        continue
                    
                    source_path = join(source_path, file_name)
                    
                    with (await AsyncIO(source_path, 'wb')) as file:
                        await file.write(binary)
                
                # Wait some. It can happen that we send this message, before the other side gets it's answer.
                message_to_send = RECEIVED
                
    except GeneratorExit:
        raise
    
    except BaseException as err:
        into = []
        into.append('```')
        await render_exception_into_async(err, into, loop = KOKORO)
        
        lines = ''.join(into).splitlines()
        into = None
        
        pages = []
        
        page_length = 0
        page_contents = []
        
        index = 0
        limit = len(lines)
        
        while True:
            if index == limit:
                embed = Embed(description = ''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            line = lines[index]
            index = index + 1
            
            line_length = len(line)
            # long line check, should not happen
            if line_length > 500:
                line = line[:500]+'...\n'
                line_length = 504
            
            if page_length + line_length > 1997:
                if index == limit:
                    # If we are at the last element, we don't need to shard up,
                    # because the last element is always '```'
                    page_contents.append(line)
                    embed = Embed(description = ''.join(page_contents))
                    pages.append(embed)
                    page_contents = None
                    break
                
                page_contents.append('```')
                embed = Embed(description = ''.join(page_contents))
                pages.append(embed)
                
                page_contents.clear()
                page_contents.append('```py\n')
                page_contents.append(line)
                
                page_length = 6 + line_length
                continue
            
            page_contents.append(line)
            page_length += line_length
            continue
        
        limit = len(pages)
        index = 0
        while index < limit:
            embed = pages[index]
            index += 1
            embed.add_footer(f'page {index}/{limit}')
        
        await Pagination(client, message.channel, pages)

async def sync_request_command(client, message, days: int = 7):
    if days < 1 or days > 30:
        await client.message_create(message.channel, f'please enter a valid day between 1 and 30 days, got {days}.')
        return
    
    if SYNC_LOCK.is_locked():
        await client.message_create(message.channel, 'A sync is already running.')
        return
    
    await client.message_create(message.channel, 'sync started')
    await request_sync(client, days)
    await client.message_create(message.channel, 'sync ended')


async def sync_request_waiter(client, message):
    if message.content != INITIAL_MESSAGE:
        return
    
    if SYNC_LOCK.is_locked():
        return
    
    Task(KOKORO, receive_sync(client, message.author))
