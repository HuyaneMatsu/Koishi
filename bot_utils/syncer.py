# -*- coding: utf-8 -*-
import os, re, sys
from os.path import join, isdir, isfile, getmtime, exists
from os import mkdir as make_dir
from datetime import datetime, timedelta
from io import StringIO

from config import HATA_PATH

from hata import Lock, KOKORO, Task, ReuAsyncIO, AsyncIO, sleep, Embed
from hata.ext.commands import wait_for_message, Pagination

from .shared import CHANNEL__SYSTEM__SYNC, PATH__KOISHI

CHUNK_SIZE = 128*1024 # 128 KB

HATA_HEAD_NAME = 'hata'
KOISHI_HEAD_NAME = 'koishi'

RELATIONS = {
    HATA_HEAD_NAME: HATA_PATH,
    KOISHI_HEAD_NAME: PATH__KOISHI,
        }

DATETIME_FORMAT_CODE = '%Y.%m.%d-%H:%M:%S'
DATETIME_RP = re.compile('(\d{4})\.(\d{2})\.(\d{2})\-(\d{2})\:(\d{2})\:(\d{2})')

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
            yield File(directory_path, name, access_path)
            continue

class File:
    __slots__ = ('path', 'modified', 'name', 'access_path',)
    
    def __init__(self, path, name, access_path):
        self.path = path
        self.modified = datetime.fromtimestamp(getmtime(path))
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
        if message.author == self.partner:
            return True
        
        return False

INITIAL_MESSAGE = 'message_initial'
REQUEST_APPROVED = 'message_approved'
RECEIVED = 'message_received'
SYNC_DONE = 'message_done'

SYNC_LOCK = Lock(KOKORO)

def get_modified_files(days_allowed):
    days_allowed = timedelta(days=days_allowed)
    should_send = []
    
    min_time = datetime.now() - days_allowed
    for file in flatten_paths():
        if file.modified > min_time:
            should_send.append(file)
    
    return should_send

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
                
                await client.message_create(CHANNEL__SYSTEM__SYNC, file_name, file=io)
            
            try:
                await wait_for_message(client, CHANNEL__SYSTEM__SYNC, check_received, 60.)
            except TimeoutError:
                sys.stderr.write('Sync request failed, timeout.\n')
                return
        
        await client.message_create(CHANNEL__SYSTEM__SYNC, SYNC_DONE)

async def receive_sync(client, partner):
    try:
        async with SYNC_LOCK:
            # some delay is needed or Koishi might answer too fast.
            await sleep(0.4, KOKORO)
            await client.message_create(CHANNEL__SYSTEM__SYNC, REQUEST_APPROVED)
            
            while True:
                try:
                    message = await wait_for_message(client, CHANNEL__SYSTEM__SYNC, check_any(partner), 60.)
                except TimeoutError:
                    sys.stderr.write('Sync request failed, timeout.\n')
                    return
                
                content = message.content
                if content == SYNC_DONE:
                    break
                
                path_full, file_name = content.split(':')
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
                    
                    source_path = join(source_path, file_name)
                    
                    with (await AsyncIO(source_path, 'wb')) as file:
                        if (binary is not None):
                            await file.write(binary)
                
                # Wait some. It can happen that we send this message, before the other side gets it's answer.
                await sleep(0.4, KOKORO)
                await client.message_create(CHANNEL__SYSTEM__SYNC, RECEIVED)
    except BaseException as err:
        with StringIO() as buffer:
            await KOKORO.render_exc_async(err, ['```'], file=buffer)
            
            buffer.seek(0)
            lines = buffer.readlines()
        
        pages = []
        
        page_length = 0
        page_contents = []
        
        index = 0
        limit = len(lines)
        
        while True:
            if index == limit:
                embed = Embed(description=''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            line = lines[index]
            index = index+1
            
            line_length = len(line)
            # long line check, should not happen
            if line_length > 500:
                line = line[:500]+'...\n'
                line_length = 504
            
            if page_length+line_length > 1997:
                if index == limit:
                    # If we are at the last element, we don't need to shard up,
                    # because the last element is always '```'
                    page_contents.append(line)
                    embed = Embed(description=''.join(page_contents))
                    pages.append(embed)
                    page_contents = None
                    break
                
                page_contents.append('```')
                embed = Embed(description=''.join(page_contents))
                pages.append(embed)
                
                page_contents.clear()
                page_contents.append('```py\n')
                page_contents.append(line)
                
                page_length = 6+line_length
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
        await client.message_create(message.channel, f'lease enter a valid day between 1 and 30 days, got {days}')
        return
    
    if SYNC_LOCK.locked():
        await client.message_create(message.channel, 'A sync is already running.')
        return
    
    await client.message_create(message.channel, 'sync started')
    await request_sync(client, days)
    await client.message_create(message.channel, 'sync ended')


async def sync_request_waiter(client, message):
    if message.content != INITIAL_MESSAGE:
        return
    
    if SYNC_LOCK.locked():
        return
    
    Task(receive_sync(client, message.author), KOKORO)
