__all__ = ('apply_mode_orin', 'should_show_orin',)

from .constants import AUDIT_LOG_INTERVA_ORIN, COLOR_ORIN, ENTRY_TYPES_ORIN, IMAGE_URL_ORIN
from .shared import count_entries


def apply_mode_orin(embed):
    """
    Applies orin mode to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to orinify.
    """
    embed.add_image(IMAGE_URL_ORIN)
    embed.color = COLOR_ORIN


async def should_show_orin(client, guild, user):
    """
    Returns whether the body collect image should be shown.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client with who the actions were executed.
    guild : ``Guild``
        The respective guild.
    user : ``ClientUserBase``
        The user who is checked.
    
    Returns
    -------
    should_show_orin : `bool`
    """
    count = await count_entries(client, guild, user, AUDIT_LOG_INTERVA_ORIN, ENTRY_TYPES_ORIN)
    return count == 5
