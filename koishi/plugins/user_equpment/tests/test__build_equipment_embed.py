import vampytest
from hata import Embed, Icon, IconType, GuildProfile, User

from ...item_core import ITEM_ID_FISHING_ROD, get_item
from ...stats_core import Stats

from ..embed_builders import build_equipment_embed, EMPTY_UNICODE



def _iter_options():
    user_id = 202503310000
    guild_id = 202503310001
    user = User.precreate(user_id, avatar = Icon(IconType.static, 2), name = 'Koishi')
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 3), nick = 'Flower')
    stats = Stats(user_id)
    stats.set('item_id_weapon', ITEM_ID_FISHING_ROD)
    weapon = get_item(ITEM_ID_FISHING_ROD)
    
    embed_base = Embed().add_field(
        'Species',
        (
            f'Neet\n'
            f'```\n'
            f'{EMPTY_UNICODE}\n'
            f'```'
        ),
        True,
    ).add_field(
        'Costume',
        (
            f'Tracksuit\n'
            f'```\n'
            f'{EMPTY_UNICODE}\n'
            f'```'
        ),
        True,
    ).add_field(
        EMPTY_UNICODE,
        EMPTY_UNICODE,
    ).add_field(
        'Head accessory',
        (
            f'Hairband\n'
            f'```\n'
            f'{EMPTY_UNICODE}\n'
            f'{EMPTY_UNICODE}\n'
            f'{EMPTY_UNICODE}\n'
            f'{EMPTY_UNICODE}\n'
            f'```'
        ),
        True,
    ).add_field(
        'Weapon',
        (
            f'{weapon.emoji} Fishing rod\n'
            f'```\n'
            f'+1 Housewife capabilities\n'
            f'+1 Bedroom skills\n'
            f'+1 Loyalty\n'
            f'-2 Fishing\n'
            f'```'
        ),
        True,
    )
    
    yield (
        user,
        stats,
        0,
        embed_base.copy_with(
            title = 'Koishi\'s equipment',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{user_id}/00000000000000000000000000000002.png'
        ),
    )
    
    yield (
        user,
        stats,
        guild_id,
        embed_base.copy_with(
            title = 'Flower\'s equipment',
        ).add_thumbnail(
            f'https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id}/avatars/00000000000000000000000000000003.png'
        ),
    )
    


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_equipment_embed(user, stats, guild_id):
    """
    tests whether ``build_equipment_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The stats.
    
    stats : ``Stats``
        The user's stats.
    
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_equipment_embed(user, stats, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
