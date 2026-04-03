import vampytest
from hata import (
    Component, Icon, IconType, User, create_section, create_separator, create_text_display, create_thumbnail_media
)

from ...item_core import ITEM_ID_FISHING_ROD, get_item
from ...user_stats_core import UserStats

from ..component_building import build_user_equipment_components


def _iter_options():
    user_id = 202503310000
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2), name = 'Koishi')
    user_stats = UserStats(user_id)
    user_stats.set_item_id_weapon(ITEM_ID_FISHING_ROD)
    weapon = get_item(ITEM_ID_FISHING_ROD)
    
    yield (
        user,
        user_stats,
        0,
        [
            create_section(
                create_text_display('# Koishi\'s equipment'),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/avatars/{user_id!s}/00000000000000000000000000000002.png'
                ),
            ),
            create_separator(),
            create_text_display(
                '### Species: Neet'
            ),
            create_separator(),
            create_text_display(
                '### Costume: Tracksuit'
            ),
            create_separator(),
            create_text_display(
                '### Head accessory: Hairband'
            ),
            create_separator(),
            create_text_display(
                f'### Weapon: {weapon.emoji} {weapon.name}\n'
                f'- +1 Housewife capabilities\n'
                f'- +1 Bedroom skills\n'
                f'- +1 Loyalty\n'
                f'- -20% Fishing'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_equipment_components(user, user_stats, guild_id):
    """
    tests whether ``build_user_equipment_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The stats.
    
    user_stats : ``UserStats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_user_equipment_components(user, user_stats, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
