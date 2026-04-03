__all__ = ()

from hata import create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import ARROW_BLOCKS


def build_lucky_spin_response_components(client, guild_id, index, amount):
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
    components : ``list<<Component>``
    """
    return [
        create_text_display(f'{client.name_at(guild_id)}\'s lucky wheel'),
        create_text_display(ARROW_BLOCKS[index]),
        create_text_display(f'You won {amount} {EMOJI__HEART_CURRENCY} !')
    ]
