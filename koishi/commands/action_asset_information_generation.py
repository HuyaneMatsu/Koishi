__all__ = ()

from os import remove as delete_file
from os.path import dirname as get_parent_directory_path, exists, isfile as is_file, join as join_paths

from hata.ext.plugin_loader import import_plugin
from hata.main import register


BREAK_LINE = '\n---\n\n'


def _put_string_into(string, affix, into):
    """
    Puts a string into the given container with a specific affix on both of its sides.
    
    Parameters
    ----------
    string : `str`
        String to put.
    affix : `str`
        Affix to use.
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append(affix)
    into.append(string)
    into.append(affix)
    return into


def _put_nullable_string_into(string, default, into):
    """
    Puts a nullable string into the given container.
    
    Parameters
    ----------
    string : `None | str`
        String to put.
    default : `str`
        Default to use if `string` is `None`.
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    if string is None:
        into = _put_string_into(default, '*', into)
    else:
        into = _put_string_into(string, '**', into)
    
    return into


def _put_strings_into(strings, default, into):
    """
    Puts a nullable string into the given container.
    
    Parameters
    ----------
    string : `None | tuple<str>`
        Strings to put.
    default : `str`
        Default to use if `strings` is `None`.
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    if strings is None:
        limit = 0
    else:
        limit = len(strings)
    
    if limit == 0:
        into = _put_string_into(default, '*', into)
    
    else:
        index = 0
        
        while True:
            string = strings[index]
            index += 1
            
            into = _put_string_into(string, '**', into)
            
            if index == limit:
                break
            
            into.append(', ')
            continue
    
    return into


def _within_title(title, into):
    """
    Wraps a block around the nested code.
    
    This function is a generator.
    
    Parameters
    ----------
    title : `str`
        Title to start with.
    into : `list<str>`
        Container to extend.
    
    Yields
    ------
    step : `None`
    """
    into.append(title)
    into.append(': ')
    yield
    into.append('\n')


def _put_strings_field_into(title, strings, default, into):
    """
    Puts a strings field's parts given into the given container.
    
    Parameters
    ----------
    title : `str`
        Title to start with.
    string : `None | tuple<str>`
        Strings to put.
    default : `str`
        Default to use if `strings` is `None`.
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    for _ in _within_title(title, into):
        into = _put_strings_into(strings, default, into)
    
    return into


def _put_string_field_into(title, string, default, into):
    """
    Puts a string field's parts given into the given container.
    
    Parameters
    ----------
    title : `str`
        Title to start with.
    string : `None | str`
        String to put.
    default : `str`
        Default to use if `strings` is `None`.
    into : `list<str>`
        Container to extend.
    
    Returns
    -------
    into : `list<str>`
    """
    for _ in _within_title(title, into):
        into = _put_nullable_string_into(string, default, into)
    
    return into


def _get_character_names(characters):
    """
    Gets the given characters' names.
    
    Parameters
    ----------
    characters : `None | tuple<TouhouCharacter>`
        Characters to get their names of.
    
    Returns
    -------
    character_names : `None | tuple<str>`
    """
    if characters is None:
        character_names = None
    else:
        character_names = (*(character.name for character in characters),)
    
    return character_names


def _build_asset_information_for(image_handler):
    """
    Builds asset information for the given image handler.
    
    Parameters
    ----------
    image_handler : ``ImageHandler``
        Image handler to user.
    
    Returns
    -------
    asset_information : `str`
    """
    into = [
        '### Asset Information\n'
        '\n'
        'Some creators may be unknown. If you know them please create a PR with it.\n'
    ]
    into.append(BREAK_LINE)
    
    for image_detail in image_handler._images:
        
        into.append('### ')
        into.append(image_detail.name)
        into.append('\n\n')
        
        into = _put_strings_field_into('- Creator', image_detail.creators, 'unknown', into)
        into = _put_strings_field_into('- Editor', image_detail.editors, 'none', into)
        into = _put_strings_field_into('- Characters', _get_character_names(image_detail.characters), 'none', into)
        into = _put_string_field_into('- Source', 'Touhou', 'original', into)
        into.append(BREAK_LINE)
    
    into.append(
        'I don\'t own the image files. The credits goes their respective owners.\n'
        'This feature is purely fan-made, and will not be used for profit or illegal sharing!\n'
        'Please contact me if you\'re the owner of an image and want to remove it from this repository!\n'
        'Contact me via opening a new issue.\n'
        '\n'
        'Thank you!\n'
    )
    
    return ''.join(into)


@register
def generate_action_assets():
    """
    Generates asset information readme.md file for action commands such as /hug.
    """
    # import plugins
    import_plugin(__package__[: __package__.rfind('.')] + '.plugins')
    
    # import actions & location
    from ..plugins.image_commands_actions import TOUHOU_ACTION_ALL, __file__ as IMAGE_COMMANDS_ACTIONS_LOCATION
    
    # build location
    location = join_paths(get_parent_directory_path(IMAGE_COMMANDS_ACTIONS_LOCATION), 'assets', 'README.md')
    
    if exists(location):
        if not is_file(location):
            return (
                f'Cannot create file because at the desired location is already something else with the same name.\n'
                f'Location: {location!r}\n'
                f'Please review what is located there.'
            )
        
        delete_file(location)
    
    asset_information = _build_asset_information_for(TOUHOU_ACTION_ALL)
    
    with open(location, 'w') as file:
        file.write(asset_information)
    
    return 'Action asset information generated.'
