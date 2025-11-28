__all__ = ()

from math import ceil, floor
from hata import ComponentType

from ..user_balance import get_user_balance, save_user_balance

from .chapters import STAGE_DEFAULT, set_new_best
from .constants import NEW_RECORD_REWARD, RATINGS, RATING_MAX, RATING_REWARDS, STAGES
from .queries import ensure_user_state_created, save_stage_result
from .user_state import StageResult


def get_rating_for(best, steps):
    """
    Gets the rating for the given stage and step combination.
    
    Parameters
    ----------
    best : `int`
        The minimal amount of steps required to defeat the stage.
    
    steps : `int`
        The user's step count.
    
    Returns
    -------
    rating : `str`
        The step's rating.
    """
    rating_factor = floor(best / 20.0) + 5.0
    
    rating_level = ceil((steps - best) / rating_factor)
    if rating_level > RATING_MAX:
        rating_level = RATING_MAX
    
    elif rating_level < 0:
        rating_level = 0
    
    return RATINGS[rating_level]


def can_play_selected_stage(stage_results, selected_stage):
    """
    Returns whether the user can play the selected chapter.
    
    Returns
    -------
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    selected_stage : ``stage``
        The selected stage by the user.
    
    Returns
    -------
    can_play_selected_stage : `bool`
        Whether the selected chapter can be played.
    """
    if selected_stage.id in stage_results:
        return True
        
    if selected_stage.previous_stage_id in stage_results:
        return True
    
    chapter = selected_stage.get_chapter()
    if chapter.first_stage_id != selected_stage.id:
        return False
    
    unlock_prerequisite_stage_id = chapter.unlock_prerequisite_stage_id
    if unlock_prerequisite_stage_id == 0:
        return True
    
    if unlock_prerequisite_stage_id in stage_results:
        return True
    
    return False


def get_selectable_stages(stage_results, selected_stage):
    """
    Gets the selectable stages around the given one.
    
    Parameters
    ----------
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    selected_stage : ``stage``
        The selected stage by the user.
    
    Returns
    -------
    selectable_stages : ``list<(Stage, int, bool)>``
        The selectable stages in a list of tuples. Contains 3 elements: `stage` , `best`, `selected`.
    """
    stages = []
    chapter_id = selected_stage.chapter_id
    
    stage = selected_stage
    for times in range(3):
        stage = stage.get_previous_stage()
        if (stage is None) or (stage.chapter_id != chapter_id):
            break
        
        stages.append(stage)
        continue
    
    stages.reverse()
    stages.append(selected_stage)
    
    stage = selected_stage
    for times in range(3):
        stage = stage.get_next_stage()
        if (stage is None) or (stage.chapter_id != chapter_id):
            break
        
        stages.append(stage)
        continue
    
    selectable_stages = []
    
    for stage in stages:
        if stage is selected_stage:
            is_selected = True
        else:
            is_selected = False
        
        stage_id = stage.id
        
        try:
            stage_result = stage_results[stage_id]
        except KeyError:
            user_best = -1
        else:
            user_best = stage_result.best
        
        selectable_stages.append((stage, user_best, is_selected))
        
        if user_best == -1:
            break
    
    selectable_stages.reverse()
    
    return selectable_stages


def get_reward_for_steps(stage_id, steps):
    """
    Gets reward amount for the given amount of steps.
    
    Parameters
    ----------
    stage_id : `int`
        The stage's identifier.
    steps : `int`
        The amount of steps.
    
    Returns
    -------
    reward : `str`
        The user's rewards.
    """
    stage = STAGES[stage_id]
    stage_best = stage.best
    
    if steps < stage_best:
        set_new_best(stage, steps)
        return NEW_RECORD_REWARD + RATING_REWARDS[0]
    
    rating_factor = floor(stage_best / 20.0) + 5.0
    
    rating_level = ceil((steps - stage_best) / rating_factor)
    if rating_level > RATING_MAX:
        rating_level = RATING_MAX
    
    return RATING_REWARDS[rating_level]


def get_reward_difference(stage_id, old_steps, new_steps):
    """
    Gets additional reward if a user received better result.
    
    Parameters
    ----------
    stage_id : `int`
        The stage's identifier.
    
    old_steps : `int`
        The old amount of steps.
    
    new_steps : `int`
        The new amount of steps.
    
    Returns
    -------
    reward : `int`
        Extra hearts, what the respective user should get.
    """
    stage = STAGES[stage_id]
    stage_best = stage.best
    rating_factor = floor(stage_best / 20.0) + 5.0
    
    rating_level = ceil((old_steps - stage_best) / rating_factor)
    if rating_level > RATING_MAX:
        rating_level = RATING_MAX
    
    reward_1 = RATING_REWARDS[rating_level]
    
    if new_steps < stage_best:
        set_new_best(stage, new_steps)
        reward_2 = NEW_RECORD_REWARD + RATING_REWARDS[0]
    else:
        rating_level = ceil((new_steps - stage_best) / rating_factor)
        if rating_level > RATING_MAX:
            rating_level = RATING_MAX
        
        reward_2 = RATING_REWARDS[rating_level]
    
    
    reward = reward_2 - reward_1
    if reward < 0:
        reward = 0
    
    return reward


async def ensure_user_state_present_and_set_new_best(user_state, stage_id, steps):
    """
    Ensures that the user state is present in the database, saving it as required.
    Then sets a new best result to the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_state : ``UserState``
        The user's state.
    
    stage_id : `int`
        The stage's identifier to set the new best result for.
    
    steps : `int`
        Step count.
    """
    await ensure_user_state_created(user_state)
    
    stage_result = user_state.stage_results.get(stage_id, None)
    if stage_result is None:
        user_state.stage_results[stage_id] = stage_result = StageResult(0, stage_id, steps)
        reward = get_reward_for_steps(stage_id, steps)
    else:
        self_best = stage_result.best
        if (steps < self_best):
            stage_result.best = steps
            reward = get_reward_difference(stage_id, self_best, steps)
        
        else:
            return
    
    await save_stage_result(user_state.user_id, stage_result)
    
    if reward:
        user_balance = await get_user_balance(user_state.user_id)
        user_balance.modify_balance_by(reward)
        await save_user_balance(user_balance)


def get_stage_id_at_position(chapter, stage_results, difficulty_id, in_difficulty_index):
    """
    Tries ot get a playable stage identifier close to the given position.
    
    Parameters
    ----------
    chapter : ``Chapter``
        The targeted chapter.
    
    stage_results: ``dict<int, StageResult>``
        Result of each completed stage by the user.
    
    difficulty_id : `int`
        The difficulty's identifier.
    
    in_difficulty_index : `int`
        The index of the chapter in the difficulty.
    
    Returns
    -------
    stage : ``Stage``
    """
    while True:
        # Filter for every stage in that difficulty.
        in_difficulty = [stage for stage in chapter.stages if stage.difficulty_id == difficulty_id]
        
        # Try to find difficulty with the given number.
        for stage in in_difficulty:
            if stage.in_difficulty_index == in_difficulty_index:
                break
        else:
            stage = None
        
        if (stage is not None):
            break
        
        # Try to select the best matching one.
        best_match_stage = None
        for stage in in_difficulty:
            if best_match_stage is None:
                best_match_stage = stage
                continue
            
            if stage.in_difficulty_index > in_difficulty_index:
                continue
            
            if stage.in_difficulty_index <= best_match_stage.in_difficulty_index:
                continue
            
            best_match_stage = stage
            continue
        
        if (best_match_stage is not None):
            stage = best_match_stage
            break
        
        # If found nothing, the first one is good enough.
        stage = chapter.get_first_stage()
        if stage is not STAGE_DEFAULT:
            break
        
        return 0
    
    # Now that we have the best matching stage, we can select the closest in the history.
    if stage.id in stage_results:
        return stage.id
    
    while True:
        previous_stage = stage.get_previous_stage()
        if previous_stage is None:
            return stage.id
        
        if previous_stage.chapter_id != chapter.id:
            return stage.id
        
        if previous_stage.id in stage_results:
            return stage.id
        
        stage = previous_stage
        continue


def disable_interactive_components(components):
    """
    Disables the interactive components.
    
    Parameters
    ----------
    components : ``tuple<Component>``
        Components to disable.
    """
    queue = [*components]
    
    while queue:
        component = queue.pop()
        
        component_type = component.type
        if component_type is ComponentType.button or component_type is ComponentType.string_select:
            component.enabled = False
        
        # Add nested components.
        queue.extend(component.iter_components())
        
        # Thumbnail is also a nested component, but is not yielt by `.iter_components`.
        thumbnail = component.thumbnail
        if (thumbnail is not None):
            queue.append(thumbnail)
