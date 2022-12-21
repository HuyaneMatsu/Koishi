__all__ = ()

from hata import BUILTIN_EMOJIS, Embed
from hata.ext.slash import InteractionResponse

from ..constants import ROLE__MEDIA_SORTER

EXAMPLE_EMOJI = BUILTIN_EMOJIS['green_heart']


async def copy_message_about(client, event):
    """Shows the command's description."""
    name = client.name_at(event.guild_id)
    
    if event.guild_id == ROLE__MEDIA_SORTER.guild_id:
        additional_info = f'or the {ROLE__MEDIA_SORTER:m} role'
    else:
        additional_info = ''
    
    return InteractionResponse(
        embed = Embed(
            'copy-message about',
            (
                f'`copy-message` is meant to help sort messages and posted media into their appropriate channels '
                f'without deleting them. It sends a copy of the message to a chosen channel by reacting with a '
                f'(default) emoji of your choice, like {EXAMPLE_EMOJI} .\n'
                f'\n'
                f'The trigger emoji must be **uniquely** assigned to a **single** channel (name or topic), but the '
                f'channel may contain multiple emojis.\n'
                f'\n'
                f'The user needs **manage messages** permission {additional_info} to invoke this command in both '
                f'channels while {name} needs **manage webhooks** permission in the target channel.'
            )
        ),
        allowed_mentions = None,
    )
