import re
from hata import Client, AnsiBackgroundColor, AnsiForegroundColor, AnsiTextDecoration, create_ansi_format_code
from hata.ext.slash import abort
from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT : Client

PATTERN = re.compile('\!\[([a-z]{0,2})\]')

RESET = create_ansi_format_code()

STYLE_CODES = {
    '': RESET,
    'dn': create_ansi_format_code(text_decoration=AnsiTextDecoration.none),
    'db': create_ansi_format_code(text_decoration=AnsiTextDecoration.bold),
    'du': create_ansi_format_code(text_decoration=AnsiTextDecoration.underline),
    'bd': create_ansi_format_code(background_color=AnsiBackgroundColor.black),
    'br': create_ansi_format_code(background_color=AnsiBackgroundColor.red),
    'bg': create_ansi_format_code(background_color=AnsiBackgroundColor.gray),
    'bb': create_ansi_format_code(background_color=AnsiBackgroundColor.blue),
    'bs': create_ansi_format_code(background_color=AnsiBackgroundColor.silver),
    'bw': create_ansi_format_code(background_color=AnsiBackgroundColor.white),
    'fd': create_ansi_format_code(foreground_color=AnsiForegroundColor.black),
    'fr': create_ansi_format_code(foreground_color=AnsiForegroundColor.red),
    'fg': create_ansi_format_code(foreground_color=AnsiForegroundColor.green),
    'fo': create_ansi_format_code(foreground_color=AnsiForegroundColor.orange),
    'fb': create_ansi_format_code(foreground_color=AnsiForegroundColor.blue),
    'fp': create_ansi_format_code(foreground_color=AnsiForegroundColor.pink),
    'ft': create_ansi_format_code(foreground_color=AnsiForegroundColor.teal),
    'fw': create_ansi_format_code(foreground_color=AnsiForegroundColor.white),
}

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, target='message', allowed_mentions=None)
async def style_text(target):
    content = target.content
    if content is None:
        abort('The message has no content.')
    
    content_length = len(content)
    if content_length > 2000:
        abort(f'Content length ({content_length}) over limit (2000).')
    
    if '```' in content:
        abort('Triple backtick in content disallowed.')
    
    parts = ['```ansi\n', RESET]
    text_start = 0
    for matched in PATTERN.finditer(content):
        text_end = matched.start()
        
        if text_start != text_end:
            parts.append(content[text_start:text_end])
        text_start = matched.end()
        
        chunk_content = matched.group(1)
        format_code = STYLE_CODES.get(chunk_content, None)
        if (format_code is None):
            abort(f'No format code for: {chunk_content}')
        
        parts.append(format_code)
    
    text_end = len(content)
    if text_start != text_end:
        parts.append(content[text_start:text_end])
    
    parts.append('\n```')
    
    output = ''.join(parts)
    output_length = len(output)
    
    if output_length > 2000:
        abort(f'Output length ({content_length}) over limit (2000).')
    
    return output
