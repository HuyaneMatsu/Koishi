__all__ = ()

from hata import ButtonStyle, create_button, create_row

from .constants import (
    CUSTOM_ID_CONTINUOUS, CUSTOM_ID_INITIAL, SIZE_TOTAL, SIZE_X, STYLE_DEFAULT, STYLE_MAP, TILE_UNKNOWN
)


def render_initial(bomb_count):
    """
    Renders the initial game components.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_row(*(
            create_button(
                emoji = TILE_UNKNOWN,
                style = ButtonStyle.gray,
                custom_id = CUSTOM_ID_INITIAL(tile_index, bomb_count),
            )
            for tile_index in range(line_start_index, line_start_index + SIZE_X)
        )) for line_start_index in range(0, SIZE_TOTAL, SIZE_X)
    ]


def create_continuous_button(tiles, flipped_tiles, index, tile_map):
    """
    Creates a continuous button that holds information about the game's current state.
    
    Parameters
    ----------
    tiles : `list<int>`
        The tiles of the game.
    
    flipped_tiles : `list<bool>`
        Whether a tile is flipped or nah.
    
    index : `int`
        The button's total position.
    
    tile_map : ``list<Emoji>``
        Tile map to use.
    
    Returns
    -------
    button : ``Component``
    """
    flipped = flipped_tiles[index]
    value = tiles[index]
    
    if flipped:
        emoji = tile_map[value]
        style = STYLE_MAP.get(value, STYLE_DEFAULT)
    else:
        emoji = TILE_UNKNOWN
        style = ButtonStyle.gray
    
    return create_button(
        emoji = emoji,
        style = style,
        custom_id = CUSTOM_ID_CONTINUOUS(index, value),
        enabled = not flipped,
    )


def render_continuous(tiles, flipped_tiles, tile_map):
    """
    Renders a step of the game.
    
    Parameters
    ----------
    tiles : `list<int>`
        The tiles of the game.
    
    flipped_tiles : `list<bool>`
        Whether a tile is flipped or nah.
    
    tile_map : ``list<Emoji>``
        Tile map to use.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_row(*(
            create_continuous_button(tiles, flipped_tiles, tile_index, tile_map)
            for tile_index in range(line_start_index, line_start_index + SIZE_X)
        )) for line_start_index in range(0, SIZE_TOTAL, SIZE_X)
    ]
