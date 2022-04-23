__all__ = ('filter_list_',)

from hata import Embed

from ..constants import EMBED_COLOR
from ..filtering import add_filter_field_to
from ..helpers import get_player_or_abort


async def filter_list_(client, event):
    """List the applied filters to the player."""
    player = get_player_or_abort(client, event)
    
    filters = [*player.iter_filters()]
    
    if filters:
        description = None
    else:
        description = '*none*'
    
    embed = Embed(
        None,
        description,
        color = EMBED_COLOR,
    )
    
    guild = event.guild
    if guild is None:
        author_icon_url = None
        author_name = 'Filters'
    else:
        author_icon_url = guild.icon_url_as(size=64)
        author_name = f'Filters for {guild.name}'
    
    embed.add_author(author_name, author_icon_url)
    
    for filter in filters:
        add_filter_field_to(embed, filter)
    
    return embed
