from hata import Embed
from hata.ext.slash import SlasherApplicationCommand
from hata.ext.extension_loader import import_extension


EMBED_COLOR = import_extension('..constants', 'EMBED_COLOR')
get_player_or_abort = import_extension('..helpers', 'get_player_or_abort')
add_filter_field_to = import_extension('..filtering', 'add_filter_field_to')


COMMAND: SlasherApplicationCommand


@COMMAND.interactions
async def filter_list(client, event):
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
