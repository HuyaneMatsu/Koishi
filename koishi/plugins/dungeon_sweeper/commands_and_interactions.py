__all__ = ()

from hata import KOKORO
from hata.ext.slash import InteractionResponse
from scarletio import TaskGroup

from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from .component_building import build_components_rules
from .constants import CHAPTERS, DUNGEON_SWEEPER_GAMES
from .custom_ids import CUSTOM_ID_RULES_SELECT
from .runner import DungeonSweeperRunner


DUNGEON_SWEEPER = FEATURE_CLIENTS.interactions(
    None,
    name = 'ds',
    description = 'Touhou themed puzzle game.',
    is_global = True,
)


@DUNGEON_SWEEPER.interactions
async def rules(client, event):
    """
    Shows the rules of the Dungeon sweeper!
    
    This function is a coroutine.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return InteractionResponse(
        components = build_components_rules(None),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RULES_SELECT)
async def handle_rules_select(event):
    """
    Handles a rules select event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : ``None | InteractionResponse``
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    select_value = event.value
    if (select_value is None) or (not select_value.isdecimal()):
        return
    
    chapter_id = int(select_value)
    if chapter_id:
        chapter = CHAPTERS.get(chapter_id, None)
    else:
        chapter = None
    
    return InteractionResponse(
        components = build_components_rules(chapter),
    )


@DUNGEON_SWEEPER.interactions(default = True)
async def begin(client, event):
    """
    Launches the game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    game = DUNGEON_SWEEPER_GAMES.get(event.user.id, None)
    if game is None:
        await DungeonSweeperRunner(client, event)
    else:
        await game.renew(client, event)


@MAIN_CLIENT.events
async def shutdown(client):
    """
    Runs when the clients are shut down.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client shutting down.
    """
    tasks = []
    exception = SystemExit()
    
    for game in DUNGEON_SWEEPER_GAMES.values():
        task = game.cancel(exception)
        if (task is not None):
            tasks.append(task)
    
    task = None
    game = None
    
    if tasks:
        await TaskGroup(KOKORO, tasks).wait_all()
