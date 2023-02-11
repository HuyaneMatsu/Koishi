__all__ = ()

from .constants import CONTINUOUS_VALUE_RP, SIZE_TOTAL


def parse_back_tiles(event):
    """
    Parses the tiles from the given components.
    
    parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    back_parsed_tiles : `None` / `tuple` (`list` of `int`, `list` of `bool)
        Returns `None` if parsing failed.
    """
    tiles = []
    flipped_tiles = []
    
    message = event.message
    if (message is not None):
        for component_row in message.iter_components():
            for component_button in component_row.iter_components():
                match = CONTINUOUS_VALUE_RP.fullmatch(component_button.custom_id)
                if match is None:
                    return
                
                tiles.append(int(match.group(1)))
                flipped_tiles.append(not component_button.enabled)
    
    
    if len(tiles) != SIZE_TOTAL:
        return None
    
    return tiles, flipped_tiles
