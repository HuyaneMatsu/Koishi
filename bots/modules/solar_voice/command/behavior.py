from hata.ext.slash import SlasherApplicationCommand
from hata.ext.extension_loader import import_extension


(
    BEHAVIOR_CHOICES,
    BEHAVIOR_VALUE_GET,
    BEHAVIOR_VALUE_REPEAT_CURRENT,
    BEHAVIOR_VALUE_REPEAT_QUEUE,
) = import_extension('..constants',
    'BEHAVIOR_CHOICES',
    'BEHAVIOR_VALUE_GET',
    'BEHAVIOR_VALUE_REPEAT_CURRENT',
    'BEHAVIOR_VALUE_REPEAT_QUEUE',
)

get_player_or_abort, get_behavior_string = import_extension('..helpers', 'get_player_or_abort', 'get_behavior_string')

COMMAND: SlasherApplicationCommand

@COMMAND.interactions
async def behavior_(client, event,
    behavior: (BEHAVIOR_CHOICES, 'Choose a behavior') = BEHAVIOR_VALUE_GET,
    value: (bool, 'Set value') = True,
):
    """Get or set the player's behavior."""
    player = get_player_or_abort(client, event)
    
    if behavior == BEHAVIOR_VALUE_GET:
        content = get_behavior_string(player)
    
    elif behavior == BEHAVIOR_VALUE_REPEAT_CURRENT:
        player.set_repeat_current(value)
        if value:
            content = 'Started to repeat the current track.'
        else:
            content = 'Stopped to repeat the current track.'
    
    elif behavior == BEHAVIOR_VALUE_REPEAT_QUEUE:
        player.set_repeat_queue(value)
        if value:
            content = 'Started to repeat the whole queue.'
        else:
            content = 'Stopped to repeat the whole queue.'
    
    # elif behavior == BEHAVIOR_VALUE_SHUFFLE:
    else:
        player.set_shuffle(value)
        if value:
            content = 'Started shuffling the queue.'
        else:
            content = 'Stopped to shuffle the queue.'
    
    
    return content
