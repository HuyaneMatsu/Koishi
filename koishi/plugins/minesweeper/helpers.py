__all__ = ()

from math import floor
from random import random

from .constants import SIZE_TOTAL, SIZE_X, TILE_VALUE_BOMB, TILE_VALUE_EMPTY, TILE_VALUE_FLAG, TILE_VALUE_UNIDENTIFIED


def to_index(position_x, position_y):
    """
    Converts the given positions to tiles index.
    
    Parameters
    ----------
    position_x : `int`
        The X axis position of the tile.
    position_y : `int`
        The Y axis position of the tile.
    
    Returns
    -------
    index : `int`
    """
    return position_x + position_y * SIZE_X


def from_index(index):
    """
    Yields the position of the given index.
    
    This method is an iterable generator.
    
    Yields
    ------
    position_x / position_y : `int`
    """
    yield from reversed(divmod(index, SIZE_X))


def iter_tiles_indexes_around(position_x, position_y):
    """
    Iterates over the tiles indexes around the given position.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    position_x : `int`
        The X axis position of the tile.
    position_y : `int`
        The Y axis position of the tile.
    
    Yields
    ------
    tile_index : `int`
    """
    for index_change_x, index_change_y in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
        local_x = position_x + index_change_x
        local_y = position_y + index_change_y
        if local_x != SIZE_X and local_x != -1 and local_y != SIZE_X and local_y != -1:
            yield to_index(local_x, local_y)


def iter_tiles_indexes_around_inclusive(position_x, position_y):
    """
    Iterates over the tiles indexes around the given position. Includes the middle position.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    position_x : `int`
        The X axis position of the tile.
    position_y : `int`
        The Y axis position of the tile.
    
    Yields
    ------
    tile_index : `int`
    """
    yield position_x + position_y * SIZE_X
    yield from iter_tiles_indexes_around(position_x, position_y)


def generate_tiles(excluded_index, bomb_count):
    """
    Generates the tiles of a minesweeper game. Excludes the tiles around the given position.
    
    Parameters
    ----------
    excluded_index : `int`
        The tile index to exclude the tiles around.
    bomb_count : `int`
        The maximal amount of bomb to add.
    
    Returns
    -------
    tiles : `list` of `int`
    """
    tiles = [TILE_VALUE_EMPTY for index in range(SIZE_TOTAL)]
    
    excluded_indexes = {*iter_tiles_indexes_around_inclusive(*from_index(excluded_index))}
    available_indexes = [index for index in range(SIZE_TOTAL) if index not in excluded_indexes]
    
    bomb_count = min(bomb_count, len(available_indexes))
    
    while bomb_count:
        bomb_count -= 1
        
        index = available_indexes.pop(floor(random() * len(available_indexes)))
        
        tiles[index] = TILE_VALUE_BOMB
        for index in iter_tiles_indexes_around(*from_index(index)):
            tile_value = tiles[index]
            if tile_value != TILE_VALUE_BOMB:
                tiles[index] = tile_value + 1
    
    return tiles


def generate_flipped_tiles():
    """
    Generates the flipped tiles.
    
    Returns
    -------
    flipped_tiles : `list` of `bool`
    """
    return [False for index in range(SIZE_TOTAL)]


def is_all_non_bomb_flipped(tiles, flipped_tiles):
    """
    Returns whether all non-bomb tiles are flipped.
    
    Parameters
    ----------
    tiles : `list` of `int`
        The tiles of a game.
    flipped_tiles : `list` of `bool`
        Whether a tile is flipped or nah.
    
    Returns
    -------
    is_all_non_bomb_flipped : `bool`
    """
    for tile, flipped in zip(tiles, flipped_tiles):
        if flipped:
            continue
        
        if tile == TILE_VALUE_BOMB:
            continue
        
        return False
    
    return True


def flag_and_flip_bomb_tiles(tiles, flipped_tiles):
    """
    Flags all bomb tiles.
    
    Parameters
    ----------
    tiles : `list` of `int`
        The tiles of a game.
    """
    for index in range(SIZE_TOTAL):
        if tiles[index] == TILE_VALUE_BOMB:
            tiles[index] = TILE_VALUE_FLAG
            flipped_tiles[index] = True


def flip_all(flipped_tiles):
    """
    Flips all tiles.
    
    Parameters
    ----------
    flipped_tiles : `list` of `bool`
        Whether a tile is flipped or nah.
    """
    for index in range(SIZE_TOTAL):
        flipped_tiles[index] = True


def flip_area_around(tiles, flipped_tiles, index):
    """
    Flips the area around the given index.
    
    Parameters
    ----------
    tiles : `list` of `int`
        The tiles of a game.
    flipped_tiles : `list` of `bool`
        Whether a tile is flipped or nah.
    index : `int`
        The tile at the given index to flip.
    """
    queue = {*iter_tiles_indexes_around(*from_index(index))}
    
    while queue:
        index = queue.pop()
        if flipped_tiles[index]:
            continue
        
        flipped_tiles[index] = True
        if tiles[index] == TILE_VALUE_EMPTY:
            queue.update(iter_tiles_indexes_around(*from_index(index)))


def flip_tile(tiles, flipped_tiles, index):
    """
    Flips the tile at the given index.
    
    Parameters
    ----------
    tiles : `list` of `int`
        The tiles of a game.
    flipped_tiles : `list` of `bool`
        Whether a tile is flipped or nah.
    index : `int`
        The tile at the given index to flip.
    """
    flipped_tiles[index] = True
    
    tile_value = tiles[index]
    if tile_value == TILE_VALUE_BOMB:
        flip_all(flipped_tiles)
        return

    if tile_value == TILE_VALUE_EMPTY:
        flip_area_around(tiles, flipped_tiles, index)
    
    if is_all_non_bomb_flipped(tiles, flipped_tiles):
        flag_and_flip_bomb_tiles(tiles, flipped_tiles)
