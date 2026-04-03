__all__ = ('load_chapter_data', 'set_new_best')

from os.path import join as join_paths

from scarletio import AsyncIO, Task, from_json, get_event_loop

from .constants import (
    CHAPTERS_PATH, FILE_LOCK, JSON_KEY_CHAPTER_DISPLAY_NAME, JSON_KEY_CHAPTER_FIRST_STAGE_ID, JSON_KEY_CHAPTER_ID,
    JSON_KEY_CHAPTER_NEXT_CHAPTER_ID, JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID, JSON_KEY_CHAPTER_RULE_ID,
    JSON_KEY_CHAPTER_SKILL_ID, JSON_KEY_CHAPTER_STAGES, JSON_KEY_CHAPTER_STYLE_ID,
    JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID, JSON_KEY_STAGE_BEST, JSON_KEY_STAGE_DIFFICULTY_ID,
    JSON_KEY_STAGE_ID, JSON_KEY_STAGE_IN_DIFFICULTY_INDEX, JSON_KEY_STAGE_MAP,
    JSON_KEY_STAGE_NEXT_STAGE_ID, JSON_KEY_STAGE_PREVIOUS_STAGE_ID, JSON_KEY_STAGE_SIZE_X,
    JSON_KEY_STAGE_START_POSITION, JSON_KEY_STAGE_TARGET_COUNT, TILE_NAME_DEFAULT, TILE_VALUE_TO_NAME
)
from .stage import Stage


def load_chapter_data(file_name):
    """
    Loads the stages and fills the chapter with them up.
    
    Parameters
    ----------
    file_name : `str`
        The file's name to load from.
    
    Returns
    -------
    difficulties : ``dict<int, dict<int, Stage>>``
        The difficulties of the chapter.
    """
    path = join_paths(CHAPTERS_PATH, file_name)
    with open(path, 'r') as file:
        chapter_data = from_json(file.read())
    
    return chapter_data


def set_new_best(stage, steps):
    """
    Sets a new best value to the given stage.
    
    Parameters
    ----------
    stage : ``Stage``
        The stage to modify it's best value.
    
    steps : `int`
        The stage's new best rating.
    
    Returns
    -------
    task : ``Task``
    """
    stage.best = steps
    return Task(get_event_loop(), _save_chapter(stage.get_chapter()))


async def _save_chapter(chapter):
    """
    Saves stage sources.
    
    This function is a coroutine.
    
    Parameters
    ----------
    chapter : ``Chapter``
    """
    file_name = chapter.file_name
    if file_name is None:
        return
    
    async with FILE_LOCK:
        path = join_paths(CHAPTERS_PATH, file_name)
        
        with await AsyncIO(path, 'w') as file:
            await file.write(''.join([*_produce_chapter_data(chapter)]))


def _make_indent(indent_level):
    """
    Makes an indent.
    
    Parameters
    ----------
    indent_level : `int`
        Indent level to make.
    
    Returns
    -------
    indent : `str`
    """
    return ' ' * (indent_level << 2)


def _produce_key(indent_level, json_key):
    """
    Produces a key.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    indent_level : `int`
        Indent level to put before the key.
    
    json_key : `str`
        Key to use.
    
    Yields
    ------
    part : `str`
    """
    yield _make_indent(indent_level)
    yield '"'
    yield json_key
    yield '": '


def _produce_nested(indent_level, json_key, value):
    """
    Produces a nested key-value pair.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    indent_level : `int`
        Indent level to put before the key.
    
    json_key : `str`
        Key to use.
    
    value : `str`
        Value to use.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_key(indent_level, json_key)
    yield value
    yield ',\n'


def _produce_chapter_data(chapter):
    """
    Produces chapter data.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    chapter : ``Chapter``
        Chapter to produce.
    
    Yields
    ------
    part : `str`
    """
    yield '{\n'
    yield from _produce_nested(1, JSON_KEY_CHAPTER_ID, str(chapter.id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID, str(chapter.unlock_prerequisite_stage_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_FIRST_STAGE_ID, str(chapter.first_stage_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID, str(chapter.previous_chapter_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_NEXT_CHAPTER_ID, str(chapter.next_chapter_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_SKILL_ID, str(chapter.skill_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_STYLE_ID, str(chapter.style_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_RULE_ID, str(chapter.rule_id))
    yield from _produce_nested(1, JSON_KEY_CHAPTER_DISPLAY_NAME, f'"{chapter.display_name}"')
    
    yield from _produce_key(1, JSON_KEY_CHAPTER_STAGES)
    yield '[\n'
    yield _make_indent(2)
    yield '{\n'
    
    stages = chapter.stages
    for stage in stages:
        yield from _produce_nested(3, JSON_KEY_STAGE_DIFFICULTY_ID, str(stage.difficulty_id))
        yield from _produce_nested(3, JSON_KEY_STAGE_IN_DIFFICULTY_INDEX, str(stage.in_difficulty_index))
        yield from _produce_nested(3, JSON_KEY_STAGE_ID, str(stage.id))
        yield from _produce_nested(3, JSON_KEY_STAGE_START_POSITION, str(stage.start_position))
        yield from _produce_nested(3, JSON_KEY_STAGE_TARGET_COUNT, str(stage.target_count))
        yield from _produce_nested(3, JSON_KEY_STAGE_SIZE_X, str(stage.size_x))
        yield from _produce_nested(3, JSON_KEY_STAGE_BEST, str(stage.best))
        yield from _produce_nested(3, JSON_KEY_STAGE_PREVIOUS_STAGE_ID, str(stage.previous_stage_id))
        yield from _produce_nested(3, JSON_KEY_STAGE_NEXT_STAGE_ID, str(stage.next_stage_id))
        
        yield from _produce_key(3, JSON_KEY_STAGE_MAP)
        yield '[\n'
        
        map_ = stage.map
        size_x = stage.size_x
        size_y = len(map_) // size_x
        
        map_iterator = iter(map_)
        
        for size_y_index in range(size_y):
            yield _make_indent(4)
            for size_x_index in range(size_x):
                if size_x_index:
                    yield ' '
                tile_value = next(map_iterator, 0)
                tile_name = TILE_VALUE_TO_NAME.get(tile_value, TILE_NAME_DEFAULT)
                yield '"'
                yield tile_name
                yield '"'
                
                if not (size_y_index == size_y - 1 and size_x_index == size_x - 1):
                    yield ' ' * (10 - len(tile_name))
                    yield ','
            
            yield '\n'
        
        yield _make_indent(3)
        yield ']\n'
        yield _make_indent(2)
        yield '}'
        
        if stage is not stages[-1]:
            yield ', {'
        
        yield '\n'
    
    yield _make_indent(1)
    yield ']\n'
    
    yield '}\n'
