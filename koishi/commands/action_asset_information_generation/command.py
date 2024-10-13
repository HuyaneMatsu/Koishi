__all__ = ()

from os import remove as delete_file
from os.path import exists, isfile as is_file, join as join_paths

from hata.ext.plugin_loader import import_plugin
from hata.main import register

from .building import _build_asset_information_for
from .constants import SOURCE_PATH


@register
def generate_action_assets():
    """
    Generates asset information README.md file for action commands such as /hug.
    """
    # import plugins
    import_plugin(__package__[: __package__.find('.')] + '.plugins')
    
    # import actions
    from ...plugins.image_commands_actions import TOUHOU_ACTION_ALL
    
    # build location
    location = join_paths(SOURCE_PATH, 'plugins', 'image_commands_actions', 'assets', 'README.md')
    
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
