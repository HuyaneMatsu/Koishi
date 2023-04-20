__all__ = ()

import re
from hata import Client, AnsiBackgroundColor, AnsiForegroundColor, AnsiTextDecoration, create_ansi_format_code, Embed
from hata.ext.slash import abort

SLASH_CLIENT : Client

PATTERN = re.compile('(?<!\\\\)<([a-z]{0,2})>')

RESET = create_ansi_format_code()

STYLE_DECORATION_NONE = create_ansi_format_code(text_decoration = AnsiTextDecoration.none)
STYLE_DECORATION_BOLD = create_ansi_format_code(text_decoration = AnsiTextDecoration.bold)
STYLE_DECORATION_UNDERLINE = create_ansi_format_code(text_decoration = AnsiTextDecoration.underline)
STYLE_BACKGROUND_BLACK = create_ansi_format_code(background_color = AnsiBackgroundColor.black)
STYLE_BACKGROUND_RED = create_ansi_format_code(background_color = AnsiBackgroundColor.red)
STYLE_BACKGROUND_GRAY = create_ansi_format_code(background_color = AnsiBackgroundColor.gray)
STYLE_BACKGROUND_BLUE = create_ansi_format_code(background_color = AnsiBackgroundColor.blue)
STYLE_BACKGROUND_SILVER = create_ansi_format_code(background_color = AnsiBackgroundColor.silver)
STYLE_BACKGROUND_WHITE = create_ansi_format_code(background_color = AnsiBackgroundColor.white)
STYLE_FOREGROUND_BLACK = create_ansi_format_code(foreground_color = AnsiForegroundColor.black)
STYLE_FOREGROUND_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
STYLE_FOREGROUND_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
STYLE_FOREGROUND_ORANGE = create_ansi_format_code(foreground_color = AnsiForegroundColor.orange)
STYLE_FOREGROUND_BLUE = create_ansi_format_code(foreground_color = AnsiForegroundColor.blue)
STYLE_FOREGROUND_PINK = create_ansi_format_code(foreground_color = AnsiForegroundColor.pink)
STYLE_FOREGROUND_TEAL = create_ansi_format_code(foreground_color = AnsiForegroundColor.teal)
STYLE_FOREGROUND_WHITE = create_ansi_format_code(foreground_color = AnsiForegroundColor.white)

STYLE_CODES = {
    '': RESET,
    'dn': STYLE_DECORATION_NONE,
    'db': STYLE_DECORATION_BOLD,
    'du': STYLE_DECORATION_UNDERLINE,
    'bd': STYLE_BACKGROUND_BLACK,
    'br': STYLE_BACKGROUND_RED,
    'bg': STYLE_BACKGROUND_GRAY,
    'bb': STYLE_BACKGROUND_BLUE,
    'bs': STYLE_BACKGROUND_SILVER,
    'bw': STYLE_BACKGROUND_WHITE,
    'fd': STYLE_FOREGROUND_BLACK,
    'fr': STYLE_FOREGROUND_RED,
    'fg': STYLE_FOREGROUND_GREEN,
    'fo': STYLE_FOREGROUND_ORANGE,
    'fb': STYLE_FOREGROUND_BLUE,
    'fp': STYLE_FOREGROUND_PINK,
    'ft': STYLE_FOREGROUND_TEAL,
    'fw': STYLE_FOREGROUND_WHITE,
}


@SLASH_CLIENT.interactions(is_global = True, target = 'message', allowed_mentions = None)
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


STYLE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'style-text',
    description = 'Styling text',
    is_global = True,
)

@STYLE_COMMANDS.interactions()
async def about(client, event):
    client_name = client.name_at(event.guild_id)
    user_name = event.user.name_at(event.guild_id)
    
    return Embed(
        f'{client_name} styles text for you!',
        (
            f'Style your text with `<style shortcut>` tags:\n'
            f'\n'
            f'**<fg>{client_name}**\n'
            f'Translates to: \n'
            f'```ansi\n'
            f'{RESET}{STYLE_FOREGROUND_GREEN}{client_name}'
            f'```\n'
            f'Text styles from each group can be combined:\n'
            f'\n'
            f'**<fg>{client_name} is green. <fr>{client_name} is red. '
            f'<bw>{client_name} is red but behind them is white!'
            f'<> Is {user_name} normal?**\n'
            f'Translates to: \n'
            f'```ansi\n'
            f'{RESET}{STYLE_FOREGROUND_GREEN}{client_name} is green. {STYLE_FOREGROUND_RED}{client_name} is red. '
            f'{STYLE_BACKGROUND_WHITE}{client_name} is red but behind them is white!{RESET} Is {user_name} normal?\n'
            f'```\n'
            f'After posting your text, right click it and use the `style-text` command.'
        )
    ).add_field(
        'Foregrounds',
        (
            f'```ansi\n'
            f'{RESET}'
            f'fd : {STYLE_FOREGROUND_BLACK}black{RESET}\n'
            f'fr : {STYLE_FOREGROUND_RED}red{RESET}\n'
            f'fg : {STYLE_FOREGROUND_GREEN}green{RESET}\n'
            f'fo : {STYLE_FOREGROUND_ORANGE}orange{RESET}\n'
            f'fb : {STYLE_FOREGROUND_BLUE}blue{RESET}\n'
            f'fp : {STYLE_FOREGROUND_PINK}pink{RESET}\n'
            f'ft : {STYLE_FOREGROUND_TEAL}teal{RESET}\n'
            f'fw : {STYLE_FOREGROUND_WHITE}white{RESET}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Backgrounds',
        (
            f'```ansi\n'
            f'{RESET}'
            f'bd : {STYLE_BACKGROUND_BLACK}black{RESET}\n'
            f'br : {STYLE_BACKGROUND_RED}red{RESET}\n'
            f'bg : {STYLE_BACKGROUND_GRAY}gray{RESET}\n'
            f'bb : {STYLE_BACKGROUND_BLUE}blue{RESET}\n'
            f'bs : {STYLE_BACKGROUND_SILVER}silver{RESET}\n'
            f'bw : {STYLE_BACKGROUND_WHITE}white{RESET}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Decorations',
        (
            f'```ansi\n'
            f'{RESET}'
            f'dn : {STYLE_DECORATION_NONE}none{RESET}\n'
            f'db : {STYLE_DECORATION_BOLD}bold{RESET}\n'
            f'du : {STYLE_DECORATION_UNDERLINE}underline{RESET}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Tips',
        (
            f'• Empty tag (`<>`) can be used to clear the existing formatting (same as `<dn>`).\n'
            f'• To escape a tag use `\\` as: `\\<fw>`\n'
            f'• To copy paste the styled-text use the `escape` message-context command on it.'
        ),
    )
