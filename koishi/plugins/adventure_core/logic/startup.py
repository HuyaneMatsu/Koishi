__all__ = ('abort_active_adventures', 'resume_active_adventures',)

from scarletio import Task, sleep

from ..adventure import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_DEPARTING, ADVENTURE_STATE_RETURNING
)
from ..constants import ADVENTURES_ACTIVE
from ..queries import get_active_adventures

from .adventure_stepping import LOOP, schedule_adventure_action, scheduled_adventure_arrival, schedule_adventure_return


async def resume_active_adventures():
    """
    Resumes the active adventures.
    
    This function is a coroutine.
    """
    adventures = await get_active_adventures()
    
    for adventure in adventures:
        adventure_state = adventure.state
        if adventure_state == ADVENTURE_STATE_DEPARTING:
            scheduler = scheduled_adventure_arrival
        elif adventure_state == ADVENTURE_STATE_ACTIONING:
            scheduler = schedule_adventure_action
        elif adventure_state == ADVENTURE_STATE_RETURNING or adventure_state == ADVENTURE_STATE_CANCELLED:
            scheduler = schedule_adventure_return
        else:
            continue
        
        Task(LOOP, scheduler(adventure))
        
        # Do not launch all of them at once, sleep some instead.
        await sleep(0.1, LOOP)
        continue


def abort_active_adventures():
    """
    Aborts the active adventures and clears them.
    """
    for adventure in ADVENTURES_ACTIVE.values():
        handle = adventure.handle
        if (handle is not None):
            adventure.handle = None
            handle.cancel()
    
    ADVENTURES_ACTIVE.clear()
