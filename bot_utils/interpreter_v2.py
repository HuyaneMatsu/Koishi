from hata import KOKORO, Embed, cchunkify
from scarletio import is_awaitable, Lock
import hata
import re
from io import StringIO
from functools import partial as partial_func
from types import FunctionType
from hata.ext.slash.menus import Pagination

try:
    from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
except ImportError:
    PyCF_ALLOW_TOP_LEVEL_AWAIT = 1 << 13

# No other flag right now
COMPILE_FLAGS = PyCF_ALLOW_TOP_LEVEL_AWAIT


def get_buffer_value(buffer):
    buffer.seek(0)
    data = buffer.read()
    if data:
        lines = data.split('\n')
        chunks = cchunkify(lines, lang='py')
    else:
        chunks = None
    
    return chunks


LINE_START = re.compile('[ \t]*')
BLOCK_START = re.compile('(```|`|)(.*?)?(```|`|)')
PYTHON_RP = re.compile('(?:python|py|)[ \t]*', re.I)
ENDER_1_RP = re.compile('[^\\\]`')
ENDER_3_RP = re.compile('[^\\\]```')

def parse_code_content(content, no_code_output=None):
    lines = content.splitlines()
    if not lines:
        return 'No content was provided', True
    
    line = lines[0]
    starter, center, ender = BLOCK_START.fullmatch(line).groups()
    if starter:
        if ender:
            if starter != ender:
                return '1 code line starter should be same long as it\'s ender.', True
            else:
                lines = [center]
        else:
            lang_match = PYTHON_RP.fullmatch(center)
            if lang_match is None:
                return 'Invalid language', True
            else:
                del lines[0]
                if len(starter) == 1:
                    pattern = ENDER_1_RP
                else: #3
                    pattern = ENDER_3_RP
                index = 0
                ln = len(lines)
                while index < ln:
                    line = lines[index]
                    if line.startswith(starter):
                        del lines[index:]
                        break
                    matched = pattern.search(line)
                    if matched is None:
                        index = index + 1
                        continue
                    line = line[:matched.start() + 1]
                    lines[index] = line
                    index += 1
                    del lines[index:]
                    break
                else:
                    return 'Code block was never ended.', True
                    
    index = len(lines)
    while index:
        index = index - 1
        line = lines[index]
        start = LINE_START.match(line).end()
        if (start != len(line)) and (line[0] != '#'):
            continue

        del lines[index]
    
    if not lines:
        return no_code_output,True
    
    return '\n'.join(lines), False


def raw_input():
    raise RuntimeError('Input disabled')

def raw_print(buffer, *args, file=None, flush=False, **kwargs):
    if file is None:
        file = buffer
    
    print(*args, file=file, **kwargs)


class Interpreter:
    __slots__ = ('locals', 'lock')
    def __init__(self, locals_):
        
        for variable_name in {
                '__name__',
                '__package__',
                '__loader__',
                '__spec__',
                '__builtins__',
                '__file__'
                    }:
            locals_[variable_name] = getattr(hata, variable_name)
        
        for variable_name in hata.__all__:
            locals_[variable_name] = getattr(hata, variable_name)
        
        self.lock = Lock(KOKORO)
        self.locals = locals_
    
    
    async def __call__(self, client, message, content):
        if not client.is_owner(message.author):
            await client.message_create(message.channel, 'You are not my boss!')
            return
        
        if self.lock.is_locked():
            await client.message_create(message.channel, 'An execution is already running.')
            return
        
        async with self.lock:
            result, is_exception = parse_code_content(content, 'No code to execute.')
            if is_exception:
                await client.message_create(message.channel, embed=Embed('Parsing error', result))
                return
            
            with StringIO() as buffer:
                try:
                    code_object = compile(result, 'online_interpreter', 'exec', flags=COMPILE_FLAGS)
                except SyntaxError as err:
                    buffer.write(
                        f'{err.__class__.__name__} at line {err.lineno}: {err.msg}\n'
                        f'{result[err.lineno - 1]}\n'
                        f'{" "*(err.offset - 1)}^'
                    )
                
                else:
                    locals_ = self.locals
                    locals_['print'] = partial_func(raw_print, buffer)
                    locals_['input'] = partial_func(raw_input)
                
                    try:
                        function = FunctionType(code_object, locals_)
                        coroutine = function()
                        if is_awaitable(coroutine):
                            await coroutine
                    except BaseException as err:
                        await KOKORO.render_exception_async(err, file=buffer)
                
                page_contents = get_buffer_value(buffer)
            
            
            pages = []
            
            if (page_contents is not None) and page_contents:
                amount = len(page_contents)
                for index, page_content in enumerate(page_contents, 1):
                    pages.append(Embed('Output:', page_content).add_footer(f'page {index}/{amount}'))
            
            else:
                pages.append(Embed('No output'))
        
        await Pagination(client, message.channel, pages, timeout=240.)
