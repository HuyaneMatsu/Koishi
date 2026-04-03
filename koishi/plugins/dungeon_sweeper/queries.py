__all__ = ()

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, DS_V2_RESULT_TABLE, DS_V2_TABLE, ds_v2_model, ds_v2_result_model

from .user_state import UserState


async def get_user_state(user_id):
    """
    Requests the user's state from the database.
    
    This function is a coroutine.
    
    Returns
    -------
    user_state : ``UserState``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            DS_V2_TABLE.select(
                ds_v2_model.user_id == user_id,
            )
        )
        ds_entry = await response.fetchone()
        if ds_entry is None:
            return UserState(user_id)
        
        if (ds_entry['game_state'] is not None):
            await connector.execute(
                DS_V2_TABLE.update(
                    ds_v2_model.id == ds_entry['id'],
                ).values(
                    game_state = None,
                )
            )
        
        response = await connector.execute(
            DS_V2_RESULT_TABLE.select(
                ds_v2_result_model.user_id == user_id,
            )
        )
        
        ds_result_entries = await response.fetchall()
        
        return UserState.from_entry(ds_entry, ds_result_entries)


if DB_ENGINE is None:
    @copy_docs(get_user_state)
    async def get_user_state(user_id):
        return UserState(user_id)


async def save_user_game_state_init_failure(user_state):
    """
    Saves the game's state. This function is called when initialization fails.
    
    This function is a coroutine.
    
    Parameters
    -----------
    user_state : ``UserState``
        The user state to save its game state.
    """
    entry_id = user_state.user_state
    if entry_id == 0:
        return
    
    game_state_data = user_state.get_game_state_data()
    if (game_state_data is None):
        return
            
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            DS_V2_TABLE.update(
                ds_v2_model.id == entry_id
            ).values(
                game_state = game_state_data,
            )
        )


if DB_ENGINE is None:
    @copy_docs(save_user_game_state_init_failure)
    async def save_user_game_state_init_failure(user_state):
        return


async def save_user_game_state(user_state):
    """
    Saves the user state's game state.
    
    This function is a coroutine.
    
    Parameters
    -----------
    user_state : ``UserState``
        The user state to save its game state.
    """
    game_state_data = user_state.get_game_state_data()
    selected_stage_id = user_state.selected_stage_id
    entry_id = user_state.entry_id
    
    async with DB_ENGINE.connect() as connector:
        if entry_id != 0:
            await connector.execute(
                DS_V2_TABLE.update(
                    ds_v2_model.id == entry_id,
                ).values(
                    game_state = game_state_data,
                    selected_stage_id = selected_stage_id,
                )
            )
        
        else:
            response = await connector.execute(
                DS_V2_TABLE.insert().values(
                    user_id = user_state.user_id,
                    game_state = game_state_data,
                    selected_stage_id = selected_stage_id,
                ).returning(
                    ds_v2_model.id,
                )
            )
            result = await response.fetchone()
            user_state.entry_id = result[0]


if DB_ENGINE is None:
    @copy_docs(save_user_game_state)
    async def save_user_game_state(user_state):
        return


async def ensure_user_state_created(user_state):
    """
    Ensures that the user state is created in the database. If it is not, creates it.
    
    This function is a coroutine.
    
    Parameters
    -----------
    user_state : ``UserState``
        The user state to save its game state.
    """
    entry_id = user_state.entry_id
    if entry_id != 0:
        return
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            DS_V2_TABLE.insert().values(
                user_id = user_state.user_id,
                game_state = user_state.get_game_state_data(),
                selected_stage_id = user_state.selected_stage_id,
            ).returning(
                ds_v2_model.id,
            )
        )
        result = await response.fetchone()
        user_state.entry_id = result[0]


if DB_ENGINE is None:
    @copy_docs(ensure_user_state_created)
    async def ensure_user_state_created(user_state):
        return


async def save_stage_result(user_id, stage_result):
    """
    Saves the stage result. If it exists updates it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    stage_result : ``StageResult``
        The stage result to save.
    """
    entry_id = stage_result.entry_id
    steps = stage_result.best
    
    async with DB_ENGINE.connect() as connector:
        if entry_id != 0:
            await connector.execute(
                DS_V2_RESULT_TABLE.update(
                    ds_v2_result_model.id == entry_id,
                ).values(
                    best = steps,
                )
            )
        
        else:
            response = await connector.execute(
                DS_V2_RESULT_TABLE.insert().values(
                    user_id = user_id,
                    stage_id = stage_result.stage_id,
                    best = steps,
                ).returning(
                    ds_v2_result_model.id,
                )
            )
            
            result = await response.fetchone()
            stage_result.entry_id = result[0]


if DB_ENGINE is None:
    @copy_docs(save_stage_result)
    async def save_stage_result(user_id, stage_result):
        return
