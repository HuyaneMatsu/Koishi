__all__ = ()

from functools import partial as partial_func
from io import StringIO
from sys import modules as MODULES
from types import FunctionType
from warnings import catch_warnings, simplefilter as apply_simple_filter

from hata import KOKORO
from scarletio import (
    Lock, add_console_input, get_highlight_streamer, is_awaitable, render_exception_into,
    write_exception_async
)
from scarletio.utils.trace.rendering import _produce_exception_representation_syntax_error
from scarletio.utils.trace.exception_representation import ExceptionRepresentationSyntaxError
from scarletio.utils.trace.exception_representation.syntax_error_helpers import (
    fix_up_syntax_error_line_from_buffer, is_syntax_error
)

# Compilation flags
try:
    from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
except ImportError:
    PyCF_ALLOW_TOP_LEVEL_AWAIT = 1 << 13

# For naming each input.
FILE_INDEX = 0

def get_new_file_name():
    global FILE_INDEX
    
    file_index = FILE_INDEX
    FILE_INDEX = file_index + 1
    
    return f'<online_console[{file_index}]>'

LOCALS = {
    '__import__' : __import__,
}

for module_path in ('scarletio', 'hata', 'koishi.bots'):
    try:
        module = MODULES[module_path]
    except KeyError:
        pass
    else:
        try:
            for variable_name in module.__all__:
                LOCALS[variable_name] = getattr(module, variable_name)
        finally:
            module = None


# No other flag right now
COMPILE_FLAGS = PyCF_ALLOW_TOP_LEVEL_AWAIT


# Execution lock
LOCK = Lock(KOKORO)


# Frame filtering.


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


# Replacements for `input` and `print`.
def raw_input():
    raise RuntimeError('Input disabled')


def raw_print(buffer, *args, file = None, flush = False, **kwargs):
    if file is None:
        file = buffer
    
    print(*args, file = file, **kwargs)


async def run(content):
    """
    Executes the given content.
    
    Parameters
    ----------
    content : `str`
        Content to execute.
    
    Returns
    -------
    response : `str`
    """
    async with LOCK:
        with StringIO() as buffer:
            file_name = get_new_file_name()
            
            try:
                with catch_warnings():
                    apply_simple_filter('error')
                    
                    try:
                        code_object = compile(content, file_name, 'exec', flags = COMPILE_FLAGS)
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
                    fix_up_syntax_error_line_from_buffer(syntax_error, content.splitlines())
                    
                    highlighter_stream = get_highlight_streamer(None)
                    for item in _produce_exception_representation_syntax_error(
                        ExceptionRepresentationSyntaxError(syntax_error, None)
                    ):
                        into.extend(highlighter_stream.asend(item))
                    
                    into.extend(highlighter_stream.asend(None))
                
                buffer.write(''.join(into))
                into = None
            
            else:
                add_console_input(file_name, content)
                
                locals_ = LOCALS
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
            
            buffer.seek(0)
            return buffer.read()
