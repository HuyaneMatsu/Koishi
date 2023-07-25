__all__ = ('build_reaction_copy_about_response',)

from hata import BUILTIN_EMOJIS, Embed
from hata.ext.slash import InteractionResponse


EXAMPLE_EMOJI = BUILTIN_EMOJIS['green_heart']


def build_reaction_copy_about_response(client, event):
    """
    Shows the reaction-copy functionality description.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the message.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    name = client.name_at(event.guild_id)
    
    return InteractionResponse(
        allowed_mentions = None,
        embed = Embed(
            'reaction-copy about',
            (
                f'`reaction-copy` is meant to help sort messages and posted media into their appropriate channels '
                f'without deleting them. It sends a copy of the message to a chosen channel by reacting with a '
                f'(default) emoji of your choice, like {EXAMPLE_EMOJI} .\n'
                f'\n'
                f'The trigger emoji must be **uniquely** assigned to a **single** channel (name or topic), but the '
                f'channel may contain multiple emojis.\n'
                f'\n'
                f'The user needs **manage messages** permission to invoke this command in both channels while {name} '
                f'needs **manage webhooks** permission in the target channel.\n'
                f'\n'
                f'A role can be additionally set to allow the feature for users without **manage messages** '
                f'permission. '
                f'Tho they will still need **view channel** permission in both of the channels.'
            )
        ),
    )
