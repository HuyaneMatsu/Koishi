import re, warnings
from functools import partial as partial_func
from io import StringIO
from types import FunctionType

import hata
from hata import Embed, KOKORO, cchunkify
from hata.ext.slash.menus import Pagination
from scarletio import (
    Lock, add_console_input, get_highlight_streamer, is_awaitable, render_exception_into, write_exception_async
)
from scarletio.utils.trace.rendering import _produce_exception_representation_syntax_error
from scarletio.utils.trace.exception_representation import ExceptionRepresentationSyntaxError
from scarletio.utils.trace.exception_representation.syntax_error_helpers import (
    fixup_syntax_error_line_from_buffer, is_syntax_error
)

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
        chunks = cchunkify(lines, lang = 'py')
    else:
        chunks = None
    
    return chunks


LINE_START = re.compile('[ \t]*')
BLOCK_START = re.compile('(```|`|)(.*?)?(```|`|)')
PYTHON_RP = re.compile('(?:python|py|)[ \t]*', re.I)
ENDER_1_RP = re.compile('[^\\\]`')
ENDER_3_RP = re.compile('[^\\\]```')

def parse_code_content(content, no_code_output = None):
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
    
    if not lines:
        return no_code_output, True
    
    return '\n'.join(lines), False


def raw_input():
    raise RuntimeError('Input disabled')

def raw_print(buffer, *args, file = None, flush = False, **kwargs):
    if file is None:
        file = buffer
    
    print(*args, file = file, **kwargs)


def _ignore_console_frames(frame):
    """
    Ignores the frames of the online console (``Interpreter`` type).
    
    Parameters
    ----------
    frame : ``FrameProxyBase``
        The frame to check.
    
    Returns
    -------
    should_show_frame : `bool`
        Whether the frame should be shown.
    """
    should_show_frame = True
    
    file_name = frame.file_name
    name = frame.name
    line = frame.line
    
    if file_name == __file__:
        if name == '__call__':
            if line == 'coroutine = function()':
                should_show_frame = False
            
            elif line == 'await coroutine':
                should_show_frame = False
    
    return should_show_frame


class Interpreter:
    __slots__ = ('_input_index', 'locals', 'lock')
    
    def __new__(cls, locals_):
        
        for variable_name in (
            '__name__',
            '__package__',
            '__loader__',
            '__spec__',
            '__builtins__',
            '__file__',
        ):
            locals_[variable_name] = getattr(hata, variable_name)
        
        for variable_name in hata.__all__:
            locals_[variable_name] = getattr(hata, variable_name)
        
        self = object.__new__(cls)
        
        self._input_index = 0
        self.locals = locals_
        self.lock = Lock(KOKORO)
        
        return self
    
    
    def _get_new_file_name(self):
        input_index = self._input_index
        self._input_index = input_index + 1
        return f'<online_console[{input_index}]>'
    
    
    async def __call__(self, client, message, content):
        if not client.is_owner(message.author):
            await client.message_create(message.channel, 'You are not my boss!')
            return
        
        if self.lock.is_locked():
            await client.message_create(message.channel, 'An execution is already running.')
            return
        
        async with self.lock:
            source, is_exception = parse_code_content(content, 'No code to execute.')
            if is_exception:
                await client.message_create(message.channel, embed = Embed('Parsing error', source))
                return
            
            with StringIO() as buffer:
                file_name = self._get_new_file_name()
                
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter('error')
                        
                        try:
                            code_object = compile(source, file_name, 'exec', flags = COMPILE_FLAGS)
                        except SyntaxError:
                            raise
                        
                        except (MemoryError, ValueError, OverflowError) as err:
                            raise SyntaxError(*err.args)
                        
                except SyntaxError as syntax_error:
                    # We re-raise exceptions of compiling instead of capturing extra exceptions from the warning
                    # module.
                    into = []
                    
                    if not is_syntax_error(syntax_error):
                        render_exception_into(syntax_error, into, filter = _ignore_console_frames)
                    
                    else:
                        fixup_syntax_error_line_from_buffer(syntax_error, source.splitlines())
                        
                        highlighter_stream = get_highlight_streamer(None)
                        for item in _produce_exception_representation_syntax_error(
                            ExceptionRepresentationSyntaxError(syntax_error, None)
                        ):
                            into.extend(highlighter_stream.asend(item))
                        
                        into.extend(highlighter_stream.asend(None))
                    
                    buffer.write(''.join(into))
                    into = None
                
                else:
                    add_console_input(file_name, source)
                    
                    locals_ = self.locals
                    locals_['print'] = partial_func(raw_print, buffer)
                    locals_['input'] = partial_func(raw_input)
                
                    try:
                        function = FunctionType(code_object, locals_)
                        coroutine = function()
                        if is_awaitable(coroutine):
                            await coroutine
                    
                    except GeneratorExit:
                        raise
                    
                    except BaseException as err:
                        await write_exception_async(err, file = buffer, filter = _ignore_console_frames, loop = KOKORO)
                
                page_contents = get_buffer_value(buffer)
            
            
            pages = []
            
            if (page_contents is not None) and page_contents:
                amount = len(page_contents)
                for index, page_content in enumerate(page_contents, 1):
                    pages.append(Embed('Output:', page_content).add_footer(f'page {index}/{amount}'))
            
            else:
                pages.append(Embed('No output'))
        
        await Pagination(client, message.channel, pages, timeout = 240.)
