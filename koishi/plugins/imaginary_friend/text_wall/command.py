__all__ = ('command_test_wall',)

from hata import Client, parse_emoji
from hata.ext.slash import P

from .fonts import FONT_DEFAULT_6_X_6, FONTS
from .modes import MODE_BY_CHARACTER, MODES


FONT_NAME_TO_FONT = {font.name: font for font in FONTS}
MODE_NAME_TO_MODE = {mode.name: mode for mode in MODES}

TEXT_SPLIT_LENGTH_MAX = 6
TEXT_PART_LENGTH_MAX = 5
TEXT_CONTENT_LENGTH_MAX = 2000


async def command_test_wall(
    client,
    interaction_event,
    text : P(str, 'Text to wall', min_length = 1, max_length = 50),
    fill : P(str, 'Fill tile', min_length = 1, max_length = 50),
    blank : P(str, 'Blank tile', min_length = 1, max_length = 50) = None,
    font_name : ([font.name for font in FONTS], 'Select a font.', 'font') = None,
    mode_name : ([mode.name for mode in MODES], 'Select a mode.', 'mode') = None,
    use_attachment : (bool, 'Whether to upload the output as an attachment') = False,
):
    """
    Converts the input text to a wall of text. Dont ask.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    text : `str`
        Text to wall.
    
    fill : `str`
        Value to use as a filling for non empty tiles.
    
    blank : `None | str` = `None`, Optional
        Value to use for filling empty tiles.
    
    font_name : `None | str` = `None`, Optional
        The font's name to use.
    
    mode_name : `None | str` = `None`, Optional
        The mode's name to use.
    
    use_attachment : `bool` = `False`, Optional
        Whether to use attachment to respond with.
    """
    while True:
        if font_name is None:
            font = FONT_DEFAULT_6_X_6
        else:
            try:
                font = FONT_NAME_TO_FONT[font_name]
            except KeyError:
                error_message = f'Font {font_name!r} not found.'
                break
        
        character_resolution_table = font.character_resolution_table
        for character in text:
            if character not in character_resolution_table:
                break
        else:
            character = None
        if (character is not None):
            error_message = f'Font does not contain character: {character!s}.'
            break
        
        
        if mode_name is None:
            mode = MODE_BY_CHARACTER
        else:
            try:
                mode = MODE_NAME_TO_MODE[mode_name]
            except KeyError:
                error_message = f'Mode {mode_name!r} not found.'
                break
        
        fill_emoji = parse_emoji(fill)
        
        if blank is None:
            blank_emoji = None
        else:
            blank_emoji = parse_emoji(blank)
        
        if blank is not None:
            starter = blank
        
        else:
            if (fill_emoji is None):
                starter = '_ _'
                blank = ' '
            else:
                starter = '_ _     '
                blank = '      '
        
        if (not use_attachment) and (fill_emoji is not None) and (not client.can_use_emoji(fill_emoji)):
            error_message = f'I cannot use the fill emoji.'
            break
        
        if (not use_attachment) and (blank_emoji is not None) and (not client.can_use_emoji(blank_emoji)):
            error_message = f'I cannot use the blank emoji.'
            break
        
        text_split = mode.splitter(text)
        text_split_length = len(text_split)
        if not text_split_length:
            error_message = f'Nothing to output after splitting the input.'
            break
        
        if (not use_attachment) and (text_split_length > TEXT_SPLIT_LENGTH_MAX):
            error_message = f'Text split count is over limit; {text_split_length} > {TEXT_SPLIT_LENGTH_MAX}.'
            break
        
        replace_resolution_table = (starter, blank, fill)
        
        contents = [mode.builder(font, part, replace_resolution_table) for part in text_split]
        
        if not use_attachment:
            for part, content in zip(text_split, contents):
                part_length = len(part)
                if part_length > TEXT_PART_LENGTH_MAX:
                    error_message = f'Text part length over limit; {part_length} > {TEXT_PART_LENGTH_MAX}.'
                    break
                
                content_length = len(content)
                if content_length > TEXT_CONTENT_LENGTH_MAX:
                    error_message = (
                        f'Generated content length for part {part!s} is over limit; '
                        f'{content_length} > {TEXT_CONTENT_LENGTH_MAX}.'
                    )
                    break
            else:
                error_message = None
            if (error_message is not None):
                break
        
        
        if use_attachment:
            await client.interaction_application_command_acknowledge(
                interaction_event,
            )
            await client.interaction_response_message_edit(
                interaction_event,
                file = ('output.txt', '\n\n'.join(contents)),
            )
        
        else:
            for index in range(len(contents)):
                if index:
                    function = Client.interaction_followup_message_create
                else:
                    function = Client.interaction_response_message_create
                
                await function(
                    client,
                    interaction_event,
                    allowed_mentions = None,
                    content = contents[index],
                )
        
        return
    
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )
