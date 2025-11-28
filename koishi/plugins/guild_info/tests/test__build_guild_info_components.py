from datetime import datetime as DateTime

import vampytest
from hata import (
    Component, Guild, Icon, IconType, StringSelectOption, create_row, create_section, create_separator,
    create_string_select, create_text_display, create_thumbnail_media
)

from ..constants import GUILD_INFO_FLAG_EVEN_IF_EMPTY, GUILD_INFO_FLAG_INFO
from ..component_building import build_guild_info_components


def _iter_options():
    guild_id = 202511210050
    
    guild = Guild.precreate(
        guild_id,
        name = 'Orin\'s corpse yard',
        icon = Icon(IconType.static, 133),
    )
    
    yield (
        guild,
        GUILD_INFO_FLAG_EVEN_IF_EMPTY | GUILD_INFO_FLAG_INFO,
        [
            create_section(
                create_text_display('# Orin\'s corpse yard'),
                create_text_display(
                     '## Guild information\n'
                     '**Created**: 2015-01-01 00:00:48 [*2 years ago*]'
                ),
                thumbnail = create_thumbnail_media(
                    'https://cdn.discordapp.com/icons/202511210050/00000000000000000000000000000085.png?size=128'
                ),
            ),
            create_separator(),
            create_row(
                create_string_select(
                    [
                        StringSelectOption('3', 'info'),
                        StringSelectOption('5', 'counts'),
                        StringSelectOption('9', 'emojis'),
                        StringSelectOption('11', 'stickers'),
                        StringSelectOption('21', 'boost perks'),
                        StringSelectOption('41', 'boosters'),
                        StringSelectOption('7e', 'all'),
                    ],
                    custom_id = 'guild.info.select',
                    placeholder = 'Select an other field!',
                ),
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_info_components(guild, even_if_empty):
    """
    Tests whether ``build_guild_info_components`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to builds components for.
    
    guild_info_flags : `int`
        Flags describing what to render.
    
    Returns
    -------
    output : ``list<Component>``
    """
    def elapsed_time_mock(input_created_at):
        vampytest.assert_instance(input_created_at, DateTime)
        return '2 years'
    
    mocked = vampytest.mock_globals(
        build_guild_info_components,
        elapsed_time = elapsed_time_mock,
        recursion = 2,
    )
    
    output = mocked(guild, even_if_empty)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
