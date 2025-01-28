import vampytest
from hata.ext.plugin_loader import PluginError
from hata.ext.plugin_loader.constants import (
    PLUGIN_ACTION_FLAG_LOAD, PLUGIN_ACTION_FLAG_NAME_LOOKUP, PLUGIN_ACTION_FLAG_SYNTAX_CHECK, PLUGIN_ACTION_FLAG_UNLINK,
    PLUGIN_ACTION_FLAG_UNLOAD
)
from hata.ext.plugin_loader.plugin import Plugin
from hata.ext.slash import InteractionResponse

from ..helpers import build_plugin_coroutine_result_response


def _iter_options():
    yield (
        'koishi.plugins.nyanner',
        'load',
        None,
        None,
        InteractionResponse(
            content = f'> Loading was successful!',
            attachments = None,
        ),
    )
    
    
    def _get_exception():
        try:
            raise ValueError('pudding')
        except ValueError as exception:
            return exception
    
    plugin_0 = Plugin(
        'koishi.plugins.nyanner', '/koishi/plugins/nyanner.py', None, None, False, False, True, None
    )
    plugin_1 = Plugin(
        'koishi.plugins.nyanner_core', '/koishi/plugins/nyanner_core.py', None, None, False, False, False, None
    )
    
    yield (
        'koishi.plugins.nyanner',
        'load',
        [
            plugin_0,
            plugin_1,
        ],
        PluginError(
            'Plugin failed to load due to no miauing.',
            action = (
                PLUGIN_ACTION_FLAG_LOAD | PLUGIN_ACTION_FLAG_NAME_LOOKUP | PLUGIN_ACTION_FLAG_SYNTAX_CHECK |
                PLUGIN_ACTION_FLAG_UNLINK | PLUGIN_ACTION_FLAG_UNLOAD
            ),
            cause = _get_exception(),
        ),
        InteractionResponse(
            content = (
                '> Loading koishi.plugins.nyanner failed. Plugin failed to load due to no miauing.\n'
                '\n'
                'ValueError(\'pudding\')'
            ),
            attachments = [
                (
                    'traceback.py',
                    (
                        f'Traceback (most recent call last):\n'
                        f'  File "{__file__}", line {_get_exception.__code__.co_firstlineno + 2}, in {_get_exception.__name__}\n'
                        f'    raise ValueError(\'pudding\')\n'
                        f'ValueError: pudding\n'
                        f'\n'
                        f'The above exception was the direct cause of the following exception:\n'
                        f'\n'
                        f'Traceback (most recent call last):\n'
                        f'<PluginError message = \'Plugin failed to load due to no miauing.\' with 1 cause>\n'
                    ),
                ),
            ]
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__build_plugin_coroutine_result_response(plugin_name, action_name, plugins, exception):
    """
    Tests whether ``build_plugin_coroutine_result_response`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    plugin_name : `str`
        The plugin's name to execute action on.
    
    action_name : `str`
        The action's name.
    
    plugins : `None | list<Plugin>`
        The plugins the operation successfully finished on.
    
    exception : `None | PluginError`
        The occurred exception.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    output = await build_plugin_coroutine_result_response(plugin_name, action_name, plugins, exception)
    vampytest.assert_instance(output, InteractionResponse)
    return output
