__all__ = ('ChapterStyle',)

from scarletio import RichAttributeErrorBaseType

from ..tile_bit_masks import (
    BIT_FLAG_EAST, BIT_FLAG_NORTH, BIT_FLAG_SOUTH, BIT_FLAG_WEST, BIT_MASK_BOX, BIT_MASK_BOX_ON_HOLE_FILLED,
    BIT_MASK_BOX_ON_OBSTACLE_DESTROYED, BIT_MASK_BOX_ON_TARGET, BIT_MASK_CHARACTER, BIT_MASK_FLOOR, BIT_MASK_HOLE,
    BIT_MASK_HOLE_FILLED, BIT_MASK_OBSTACLE, BIT_MASK_OBSTACLE_DESTROYED, BIT_MASK_TARGET_ON_FLOOR, BIT_MASK_WALL
)


def build_tile_resolution_table(tile_emoji_mapping):
    """
    Builds a tile resolution table from the given tile emoji mapping.
    
    Parameters
    ----------
    tile_emoji_mapping : ``TileEmojiMapping``
        Tile emoji mapping to build from.
    
    Returns
    -------
    tile_resolution_table : `dict<int, str>`
    """
    return {
        BIT_MASK_WALL : tile_emoji_mapping.wall.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_EAST : tile_emoji_mapping.wall_east.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_SOUTH : tile_emoji_mapping.wall_south.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_WEST : tile_emoji_mapping.wall_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_SOUTH | BIT_FLAG_WEST : tile_emoji_mapping.wall_north_east_south_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_SOUTH : tile_emoji_mapping.wall_east_south.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_SOUTH | BIT_FLAG_WEST : tile_emoji_mapping.wall_south_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST : tile_emoji_mapping.wall_north_east.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_WEST : tile_emoji_mapping.wall_north_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_SOUTH : tile_emoji_mapping.wall_north_east_south.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_SOUTH | BIT_FLAG_WEST : tile_emoji_mapping.wall_north_south_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_SOUTH : tile_emoji_mapping.wall_north_south.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_WEST : tile_emoji_mapping.wall_east_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_NORTH | BIT_FLAG_EAST | BIT_FLAG_WEST : tile_emoji_mapping.wall_north_east_west.as_emoji,
        BIT_MASK_WALL | BIT_FLAG_EAST | BIT_FLAG_SOUTH | BIT_FLAG_WEST : tile_emoji_mapping.wall_east_south_west.as_emoji,
        
        BIT_MASK_WALL | BIT_FLAG_NORTH : tile_emoji_mapping.wall_north.as_emoji,
        
        BIT_MASK_FLOOR : tile_emoji_mapping.other_floor.as_emoji,
        BIT_MASK_TARGET_ON_FLOOR : tile_emoji_mapping.other_target_on_floor.as_emoji,
        BIT_MASK_OBSTACLE_DESTROYED : tile_emoji_mapping.other_obstacle_destroyed.as_emoji,
        BIT_MASK_HOLE_FILLED : tile_emoji_mapping.other_hole_filled.as_emoji,
        BIT_MASK_FLOOR | BIT_MASK_BOX : tile_emoji_mapping.other_box_on_floor.as_emoji,
        BIT_MASK_BOX_ON_TARGET : tile_emoji_mapping.other_box_on_target.as_emoji,
        BIT_MASK_BOX_ON_HOLE_FILLED : tile_emoji_mapping.other_box_on_hole_filled.as_emoji,
        BIT_MASK_BOX_ON_OBSTACLE_DESTROYED : tile_emoji_mapping.other_box_on_obstacle_destroyed.as_emoji,
        BIT_MASK_HOLE : tile_emoji_mapping.other_hole.as_emoji,
        BIT_MASK_OBSTACLE : tile_emoji_mapping.other_obstacle.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_FLOOR : tile_emoji_mapping.character_north_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_FLOOR : tile_emoji_mapping.character_east_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_FLOOR : tile_emoji_mapping.character_south_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_FLOOR : tile_emoji_mapping.character_west_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_TARGET_ON_FLOOR : tile_emoji_mapping.character_north_on_target_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_TARGET_ON_FLOOR : tile_emoji_mapping.character_east_on_target_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_TARGET_ON_FLOOR : tile_emoji_mapping.character_south_on_target_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_TARGET_ON_FLOOR : tile_emoji_mapping.character_west_on_target_on_floor.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_HOLE_FILLED : tile_emoji_mapping.character_north_on_hole_filled.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_HOLE_FILLED : tile_emoji_mapping.character_east_on_hole_filled.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_HOLE_FILLED : tile_emoji_mapping.character_south_on_hole_filled.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_HOLE_FILLED : tile_emoji_mapping.character_west_on_hole_filled.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_NORTH | BIT_MASK_OBSTACLE_DESTROYED : tile_emoji_mapping.character_north_on_obstacle_destroyed.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_EAST | BIT_MASK_OBSTACLE_DESTROYED : tile_emoji_mapping.character_east_on_obstacle_destroyed.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_SOUTH | BIT_MASK_OBSTACLE_DESTROYED : tile_emoji_mapping.character_south_on_obstacle_destroyed.as_emoji,
        BIT_MASK_CHARACTER | BIT_FLAG_WEST | BIT_MASK_OBSTACLE_DESTROYED : tile_emoji_mapping.character_west_on_obstacle_destroyed.as_emoji,
    }


class ChapterStyle(RichAttributeErrorBaseType):
    """
    Represents a chapter's style.
    
    Attributes
    ----------
    control_emoji_mapping : ``ControlEmojiMapping``
        Control emojis to use.
    
    emoji : ``Emoji``
        The chapter's character's emoji.
    
    id : `int`
        The chapter's style's identifier.
    
    tile_emoji_mapping : ``TileEmojiMapping``
        The in-game tiles to use.
    
    tile_resolution_table : `dict<int, str>`
        Tile identifier to tile emoji value resolution table.
    """
    __slots__ = ('control_emoji_mapping', 'emoji', 'id', 'tile_emoji_mapping', 'tile_resolution_table')
    
    def __new__(cls, style_id, emoji, control_emoji_mapping, tile_emoji_mapping):
        """
        Parameters
        ----------
        style_id : `int`
            The style's identifier.
        
        emoji : ``Emoji``
            The chapter's character's emoji.
        
        control_emoji_mapping : ``ControlEmojiMapping``
            Control emojis to use.
        
        tile_emoji_mapping : ``TileEmojiMapping``
            The in-game tiles to use.
        """
        self = object.__new__(cls)
        self.control_emoji_mapping = control_emoji_mapping
        self.emoji = emoji
        self.id = style_id
        self.tile_emoji_mapping = tile_emoji_mapping
        self.tile_resolution_table = build_tile_resolution_table(tile_emoji_mapping)
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
