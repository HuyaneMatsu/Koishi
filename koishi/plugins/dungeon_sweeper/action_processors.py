__all__ = ()

from .constants import (
    RUNNER_STATE_CLOSED, RUNNER_STATE_END_SCREEN, RUNNER_STATE_IN_GAME, RUNNER_STATE_IN_MENU,
    STAGE_STEP_MULTI_STEP_BUTTON
)
from .custom_ids import (
    CUSTOM_ID_END_SCREEN_NEXT_STAGE, CUSTOM_ID_END_SCREEN_RESTART_STAGE, CUSTOM_ID_END_SCREEN_RETURN_TO_MENU,
    CUSTOM_ID_IN_GAME_BACK, CUSTOM_ID_IN_GAME_EAST, CUSTOM_ID_IN_GAME_EAST_TO_NORTH, CUSTOM_ID_IN_GAME_EAST_TO_SOUTH,
    CUSTOM_ID_IN_GAME_NORTH, CUSTOM_ID_IN_GAME_NORTH_TO_EAST, CUSTOM_ID_IN_GAME_NORTH_TO_WEST, CUSTOM_ID_IN_GAME_RESTART,
    CUSTOM_ID_IN_GAME_RETURN_TO_MENU, CUSTOM_ID_IN_GAME_SKILL, CUSTOM_ID_IN_GAME_SOUTH, CUSTOM_ID_IN_GAME_SOUTH_TO_EAST,
    CUSTOM_ID_IN_GAME_SOUTH_TO_WEST, CUSTOM_ID_IN_GAME_WEST, CUSTOM_ID_IN_GAME_WEST_TO_NORTH,
    CUSTOM_ID_IN_GAME_WEST_TO_SOUTH, CUSTOM_ID_IN_MENU_CHAPTER_PREVIOUS,
    CUSTOM_ID_IN_MENU_CHAPTER_NEXT, CUSTOM_ID_IN_MENU_CLOSE, CUSTOM_ID_IN_MENU_SELECT_STAGE,
    CUSTOM_ID_IN_MENU_STAGE_PREVIOUS, CUSTOM_ID_IN_MENU_STAGE_PREVIOUS_MULTI,
    CUSTOM_ID_IN_MENU_STAGE_NEXT, CUSTOM_ID_IN_MENU_STAGE_NEXT_MULTI
)
from .helpers import (
    can_play_selected_stage, ensure_user_state_present_and_set_new_best, get_stage_id_at_position
)
from .user_state import GameState


async def action_processor_end_screen_return_to_menu(dungeon_sweeper_runner):
    """
    Processes a return to menu action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_END_SCREEN:
        return False
    
    dungeon_sweeper_runner.user_state.game_state = None
    
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_IN_MENU
    return True


async def action_processor_end_screen_next_stage(dungeon_sweeper_runner):
    """
    Processes a start the next stage action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_END_SCREEN:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    selected_stage = user_state.game_state.stage.get_next_stage()
    if selected_stage is None:
        return False
    
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_IN_GAME
    
    selected_stage_id = selected_stage.id
    user_state.selected_stage_id = selected_stage_id
    
    try:
        stage_result = user_state.stage_results[selected_stage_id]
    except KeyError:
        best = -1
    else:
        best = stage_result.best
    
    user_state.game_state = GameState(selected_stage, best)
    return True


async def action_processor_end_screen_restart_stage(dungeon_sweeper_runner):
    """
    Processes a restart stage action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_END_SCREEN:
        return False
    
    dungeon_sweeper_runner.user_state.game_state.restart()
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_IN_GAME
    return True


async def action_processor_in_game_back(dungeon_sweeper_runner):
    """
    Processes going back in steps action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    game_state = dungeon_sweeper_runner.user_state.game_state
    
    return game_state.back()


async def action_processor_in_game_east(dungeon_sweeper_runner):
    """
    Processes an move east action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    game_state = user_state.game_state
    
    success = game_state.move_east()
    if success and game_state.is_done():
        await ensure_user_state_present_and_set_new_best(user_state, game_state.stage.id, len(game_state.history))
        dungeon_sweeper_runner._runner_state = RUNNER_STATE_END_SCREEN
    
    return success


async def action_processor_in_game_east_to_north(dungeon_sweeper_runner):
    """
    Processes a move east then north action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_east(dungeon_sweeper_runner):
        await action_processor_in_game_north(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_east_to_south(dungeon_sweeper_runner):
    """
    Processes a move east then south action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_east(dungeon_sweeper_runner):
        await action_processor_in_game_south(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_north(dungeon_sweeper_runner):
    """
    Processes a move north action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    game_state = user_state.game_state
    
    success = game_state.move_north()
    if success and game_state.is_done():
        await ensure_user_state_present_and_set_new_best(user_state, game_state.stage.id, len(game_state.history))
        dungeon_sweeper_runner._runner_state = RUNNER_STATE_END_SCREEN
    
    return success


async def action_processor_in_game_north_to_east(dungeon_sweeper_runner):
    """
    Processes a move north then east action
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_north(dungeon_sweeper_runner):
        await action_processor_in_game_east(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_north_to_west(dungeon_sweeper_runner):
    """
    Processes a move north then west action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_north(dungeon_sweeper_runner):
        await action_processor_in_game_west(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_restart(dungeon_sweeper_runner):
    """
    Processes a reset game state action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    game_state = dungeon_sweeper_runner.user_state.game_state
    
    return game_state.restart()


async def action_processor_in_game_return_to_menu(dungeon_sweeper_runner):
    """
    Processes return to menu action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_IN_MENU
    user_state = dungeon_sweeper_runner.user_state
    user_state.game_state = None
    return True


async def action_processor_in_game_skill(dungeon_sweeper_runner):
    """
    Processes a skill activate or use action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    game_state = dungeon_sweeper_runner.user_state.game_state
    
    return game_state.skill_activate()


async def action_processor_in_game_south(dungeon_sweeper_runner):
    """
    Processes a move south action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    game_state = user_state.game_state
    
    success = game_state.move_south()
    if success and game_state.is_done():
        await ensure_user_state_present_and_set_new_best(user_state, game_state.stage.id, len(game_state.history))
        dungeon_sweeper_runner._runner_state = RUNNER_STATE_END_SCREEN
    
    return success


async def action_processor_in_game_south_to_east(dungeon_sweeper_runner):
    """
    Processes a move south then east action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_south(dungeon_sweeper_runner):
        await action_processor_in_game_east(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_south_to_west(dungeon_sweeper_runner):
    """
    Processes a move south then west action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_south(dungeon_sweeper_runner):
        await action_processor_in_game_west(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_west(dungeon_sweeper_runner):
    """
    Processes a move west action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_GAME:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    game_state = user_state.game_state
    
    success = game_state.move_west()
    if success and game_state.is_done():
        await ensure_user_state_present_and_set_new_best(user_state, game_state.stage.id, len(game_state.history))
        dungeon_sweeper_runner._runner_state = RUNNER_STATE_END_SCREEN
    
    return success


async def action_processor_in_game_west_to_north(dungeon_sweeper_runner):
    """
    Processes a move west then north action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_west(dungeon_sweeper_runner):
        await action_processor_in_game_north(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_game_west_to_south(dungeon_sweeper_runner):
    """
    Processes a move west then south action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if await action_processor_in_game_west(dungeon_sweeper_runner):
        await action_processor_in_game_south(dungeon_sweeper_runner)
        return True
    
    return False


async def action_processor_in_menu_chapter_previous(dungeon_sweeper_runner):
    """
    Processes a stage index decrement action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    
    stage = user_state.get_selected_stage()
    chapter = stage.get_chapter().get_previous_chapter()
    if chapter is None:
        return False
    
    stage_id = get_stage_id_at_position(chapter, user_state.stage_results, stage.difficulty_id, stage.in_difficulty_index)
    if not stage_id:
        return False
    
    user_state.selected_stage_id = stage_id
    return True


async def action_processor_in_menu_chapter_next(dungeon_sweeper_runner):
    """
    Processes a stage index increment action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    
    stage = user_state.get_selected_stage()
    chapter = stage.get_chapter().get_next_chapter()
    if chapter is None:
        return False
    
    stage_id = get_stage_id_at_position(chapter, user_state.stage_results, stage.difficulty_id, stage.in_difficulty_index)
    if not stage_id:
        return False
    
    user_state.selected_stage_id = stage_id
    return True


async def action_processor_in_menu_close(dungeon_sweeper_runner):
    """
    Processes a close game action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_CLOSED
    return True


async def action_processor_in_menu_select_stage(dungeon_sweeper_runner):
    """
    Processes a stage select action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    selected_stage = user_state.get_selected_stage()
    if not can_play_selected_stage(user_state.stage_results, selected_stage):
        return False
    
    try:
        stage_result = user_state.stage_results[selected_stage.id]
    except KeyError:
        best = -1
    else:
        best = stage_result.best
    
    user_state.game_state = GameState(selected_stage, best)
    dungeon_sweeper_runner._runner_state = RUNNER_STATE_IN_GAME
    return True


async def action_processor_in_menu_stage_next(dungeon_sweeper_runner):
    """
    Processes a stage index increment action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    
    selected_stage = user_state.get_selected_stage()
    if selected_stage is None:
        return False
    
    if selected_stage.id not in user_state.stage_results:
        return False
    
    next_stage = selected_stage.get_next_stage()
    if (next_stage is None) or (next_stage.chapter_id != selected_stage.chapter_id):
        return False
    
    user_state.selected_stage_id = next_stage.id
    return True


async def action_processor_in_menu_stage_next_multi(dungeon_sweeper_runner):
    """
    Processes a stage index increment multi action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    
    selected_stage = user_state.get_selected_stage()
    stage_results = user_state.stage_results
    if selected_stage.id not in stage_results:
        return False
    
    chapter_id = selected_stage.chapter_id
    
    for counter in range(STAGE_STEP_MULTI_STEP_BUTTON):
        next_stage = selected_stage.get_next_stage()
        if (next_stage is None) or (next_stage.chapter_id != chapter_id):
            if counter:
                break
            
            return False
        
        selected_stage = next_stage
        if selected_stage.id not in stage_results:
            break
        
        continue
        
    user_state.selected_stage_id = selected_stage.id
    return True


async def action_processor_in_menu_stage_previous(dungeon_sweeper_runner):
    """
    Processes a stage index decrement action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    selected_stage = user_state.get_selected_stage()
    
    previous_stage = selected_stage.get_previous_stage()
    if (previous_stage is None) or (previous_stage.chapter_id != selected_stage.chapter_id):
        return False
    
    user_state.selected_stage_id = previous_stage.id
    return True


async def action_processor_in_menu_stage_previous_multi(dungeon_sweeper_runner):
    """
    Processes a stage index decrement multi action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    dungeon_sweeper_runner : ``DungeonSweeperRunner``
        The respective dungeon sweeper runner.
    
    Returns
    -------
    success : `bool`
        Whether the action was executed successfully.
    """
    if dungeon_sweeper_runner._runner_state != RUNNER_STATE_IN_MENU:
        return False
    
    user_state = dungeon_sweeper_runner.user_state
    
    selected_stage = user_state.get_selected_stage()
    chapter_id = selected_stage.chapter_id
    
    for counter in range(STAGE_STEP_MULTI_STEP_BUTTON):
        previous_stage = selected_stage.get_previous_stage()
        if (previous_stage is None) or (previous_stage.chapter_id != chapter_id):
            if counter:
                break
            
            return False
        
        selected_stage = previous_stage
        continue
    
    user_state.selected_stage_id = selected_stage.id
    return True


ACTION_PROCESSORS = {
    CUSTOM_ID_END_SCREEN_RETURN_TO_MENU : action_processor_end_screen_return_to_menu,
    CUSTOM_ID_END_SCREEN_NEXT_STAGE : action_processor_end_screen_next_stage,
    CUSTOM_ID_END_SCREEN_RESTART_STAGE : action_processor_end_screen_restart_stage,
    
    CUSTOM_ID_IN_GAME_BACK : action_processor_in_game_back,
    CUSTOM_ID_IN_GAME_EAST : action_processor_in_game_east,
    CUSTOM_ID_IN_GAME_EAST_TO_NORTH : action_processor_in_game_east_to_north,
    CUSTOM_ID_IN_GAME_EAST_TO_SOUTH : action_processor_in_game_east_to_south,
    CUSTOM_ID_IN_GAME_NORTH : action_processor_in_game_north,
    CUSTOM_ID_IN_GAME_NORTH_TO_EAST : action_processor_in_game_north_to_east,
    CUSTOM_ID_IN_GAME_NORTH_TO_WEST : action_processor_in_game_north_to_west,
    CUSTOM_ID_IN_GAME_RESTART : action_processor_in_game_restart,
    CUSTOM_ID_IN_GAME_RETURN_TO_MENU : action_processor_in_game_return_to_menu,
    CUSTOM_ID_IN_GAME_SKILL : action_processor_in_game_skill,
    CUSTOM_ID_IN_GAME_SOUTH : action_processor_in_game_south,
    CUSTOM_ID_IN_GAME_SOUTH_TO_EAST : action_processor_in_game_south_to_east,
    CUSTOM_ID_IN_GAME_SOUTH_TO_WEST : action_processor_in_game_south_to_west,
    CUSTOM_ID_IN_GAME_WEST : action_processor_in_game_west,
    CUSTOM_ID_IN_GAME_WEST_TO_NORTH : action_processor_in_game_west_to_north,
    CUSTOM_ID_IN_GAME_WEST_TO_SOUTH : action_processor_in_game_west_to_south,
    
    CUSTOM_ID_IN_MENU_CHAPTER_PREVIOUS : action_processor_in_menu_chapter_previous,
    CUSTOM_ID_IN_MENU_CHAPTER_NEXT : action_processor_in_menu_chapter_next,
    CUSTOM_ID_IN_MENU_CLOSE : action_processor_in_menu_close,
    CUSTOM_ID_IN_MENU_SELECT_STAGE : action_processor_in_menu_select_stage,
    CUSTOM_ID_IN_MENU_STAGE_PREVIOUS : action_processor_in_menu_stage_previous,
    CUSTOM_ID_IN_MENU_STAGE_PREVIOUS_MULTI : action_processor_in_menu_stage_previous_multi,
    CUSTOM_ID_IN_MENU_STAGE_NEXT : action_processor_in_menu_stage_next,
    CUSTOM_ID_IN_MENU_STAGE_NEXT_MULTI : action_processor_in_menu_stage_next_multi,
}
