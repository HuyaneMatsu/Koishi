import vampytest
from hata import Component, GuildProfile, User, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..component_building import build_lucky_spin_response_components
from ..constants import ARROW_BLOCKS


def _iter_options():
    user_id = 202506040000
    guild_id = 202506040001
    name = 'momiji'
    nick = 'awoo'
    
    user = User.precreate(user_id, name = name)
    user.guild_profiles[guild_id] = GuildProfile(nick = nick)
    
    yield (
        user,
        guild_id,
        1,
        100,
        [
            create_text_display(f'{nick}\'s lucky wheel'),
            create_text_display(ARROW_BLOCKS[1]),
            create_text_display(f'You won {100} {EMOJI__HEART_CURRENCY} !')
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_lucky_spin_response_components(client, guild_id, index, amount):
    """
    Builds lucky spin response components.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who's lucky spin it is.
    
    guild_id : `int`
        Respective guild identifier.
    
    index : `int`
        The index of the spin to show.
    
    amount : `int`
        The amount of balance the user receives. Even if the user loses, its still positive.
        Example: bet 10 -> gets 0.8 multiplier -> won 2.
    
    Returns
    -------
    output : ``list<<Component>``
    """
    output = build_lucky_spin_response_components(client, guild_id, index, amount)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
