__all__ = ('behaviour_',)

from ..constants import (
    BEHAVIOR_CHOICES, BEHAVIOR_VALUE_GET, BEHAVIOR_VALUE_REPEAT_CURRENT, BEHAVIOR_VALUE_REPEAT_QUEUE
)
from ..helpers import get_behaviour_string, get_player_or_abort


async def behaviour_(client, event,
    behaviour: (BEHAVIOR_CHOICES, 'Choose a behaviour') = BEHAVIOR_VALUE_GET,
    value: (bool, 'Set value') = True,
):
    """Get or set the player's behaviour."""
    player = get_player_or_abort(client, event)
    
    if behaviour == BEHAVIOR_VALUE_GET:
        content = get_behaviour_string(player)
    
    elif behaviour == BEHAVIOR_VALUE_REPEAT_CURRENT:
        player.set_repeat_current(value)
        if value:
            content = 'Started to repeat the current track.'
        else:
            content = 'Stopped to repeat the current track.'
    
    elif behaviour == BEHAVIOR_VALUE_REPEAT_QUEUE:
        player.set_repeat_queue(value)
        if value:
            content = 'Started to repeat the whole queue.'
        else:
            content = 'Stopped to repeat the whole queue.'
    
    # elif behaviour == BEHAVIOR_VALUE_SHUFFLE:
    else:
        player.set_shuffle(value)
        if value:
            content = 'Started shuffling the queue.'
        else:
            content = 'Stopped to shuffle the queue.'
    
    
    return content
