__all__ = ()

from hata import BUILTIN_EMOJIS, Embed


EXAMPLE_EMOJI = BUILTIN_EMOJIS['green_heart']


async def copy_message_about(client, event):
    """Shows the command's description."""
    name = client.name_at(event.guild_id)
    
    return Embed(
        'copy-message about',
        (
            f'`copy-message` is meant to help sort messages and posted media into their appropriate channels without '
            f'deleting them it sends a copy of the message to a chosen channel by reacting with a (default) emoji of '
            f'your choice, like {EXAMPLE_EMOJI} .\n'
            f'\n'
            f'The trigger emoji must be **uniquely** assigned to a **single** channel (name or topic), but the channel '
            f'may contain multiple emojis.\n'
            f'\n'
            f'The user needs **manage messages** permission to invoke this command in both channels while {name} needs '
            f'**manage webhooks** permission in the target channel.'
        )
    )
