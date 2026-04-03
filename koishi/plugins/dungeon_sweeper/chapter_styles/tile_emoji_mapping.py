__all__ = ()

from scarletio import RichAttributeErrorBaseType


class TileEmojiMapping(RichAttributeErrorBaseType):
    """
    Represents the tile emojis a chapter.
    
    Attributes
    ----------
    character_east_on_floor : ``Emoji``
        Character looking east-wards on a floor.
    
    character_east_on_hole_filled : ``Emoji``
        Character looking east-wards on a filled hole.
    
    character_east_on_obstacle_destroyed : ``Emoji``
        Character looking east-wards on a destroyed obstacle.
    
    character_east_on_target_on_floor : ``Emoji``
        Character looking east-wards on a target floor.
    
    character_north_on_floor : ``Emoji``
        Character looking north-wards on a floor.
    
    character_north_on_hole_filled : ``Emoji``
        Character looking north-wards on a filled hole.
    
    character_north_on_obstacle_destroyed : ``Emoji``
        Character looking north-wards on a destroyed obstacle.
    
    character_north_on_target_on_floor : ``Emoji``
        Character looking north-wards on a target floor.
    
    character_south_on_floor : ``Emoji``
        Character looking south-wards on a floor.
    
    character_south_on_hole_filled : ``Emoji``
        Character looking south-wards on a filled hole.
    
    character_south_on_obstacle_destroyed : ``Emoji``
        Character looking south-wards on a destroyed obstacle.
    
    character_south_on_target_on_floor : ``Emoji``
        Character looking south-wards on a target floor.
    
    character_west_on_floor : ``Emoji``
        Character looking west-wards on a floor.
    
    character_west_on_hole_filled : ``Emoji``
        Character looking west-wards on a filled hole.
    
    character_west_on_obstacle_destroyed : ``Emoji``
        Character looking west-wards on a destroyed obstacle.
    
    character_west_on_target_on_floor : ``Emoji``
        Character looking west-wards on a target floor.
    
    other_box_on_floor : ``Emoji``
        Box on a floor.
    
    other_box_on_hole_filled : ``Emoji``
        Box on a filled hole.
    
    other_box_on_obstacle_destroyed : ``Emoji``
        Box on a destroyed obstacle.
    
    other_box_on_target : ``Emoji``
        Box on a target floor.
    
    other_floor : ``Emoji``
        Floor.
    
    other_hole : ``Emoji``
        Hole.
    
    other_hole_filled : ``Emoji``
        Filled hole.
    
    other_obstacle : ``Emoji``
        Obstacle.
    
    other_obstacle_destroyed : ``Emoji``
        Destroyed obstacle.
    
    other_target_on_floor : ``Emoji``
        Target on a floor.
    
    wall : ``Emoji``
        Empty wall tile used where wall has no direction.
    
    wall_east : ``Emoji``
        East side wall.
    
    wall_east_south : ``Emoji``
        East and south side wall.
    
    wall_east_south_west : ``Emoji``
        East, south and west side wall.
    
    wall_east_west : ``Emoji``
        East and west side wall.
    
    wall_north : ``Emoji``
        North side wall. This tile is visible so not like other walls, has an actual chapter specific asset.
    
    wall_north_east : ``Emoji``
        North and east side wall.
    
    wall_north_east_south : ``Emoji``
        North, east  and south side wall.
        
    wall_north_east_south_west : ``Emoji``
        North, east, south as west side wall.
    
    wall_north_east_west : ``Emoji``
        North, east and west side wall.
    
    wall_north_south : ``Emoji``
        North and south side wall.
    
    wall_north_south_west : ``Emoji``
        North, south and west side wall.
    
    wall_north_west : ``Emoji``
        North and west side wall.
    
    wall_south : ``Emoji``
        South side wall.
    
    wall_south_west : ``Emoji``
        South and west side wall.
    
    wall_west : ``Emoji``
        West side wall.
    """
    __slots__ = (
        'character_east_on_floor', 'character_east_on_hole_filled', 'character_east_on_obstacle_destroyed',
        'character_east_on_target_on_floor', 'character_north_on_floor', 'character_north_on_hole_filled',
        'character_north_on_obstacle_destroyed', 'character_north_on_target_on_floor', 'character_south_on_floor',
        'character_south_on_hole_filled', 'character_south_on_obstacle_destroyed',
        'character_south_on_target_on_floor', 'character_west_on_floor', 'character_west_on_hole_filled',
        'character_west_on_obstacle_destroyed', 'character_west_on_target_on_floor', 
        
        'other_box_on_floor', 'other_box_on_hole_filled', 'other_box_on_obstacle_destroyed', 'other_box_on_target',
        'other_floor', 'other_hole', 'other_hole_filled', 'other_obstacle', 'other_obstacle_destroyed',
        'other_target_on_floor',
        
        'wall', 'wall_east', 'wall_east_south', 'wall_east_south_west', 'wall_east_west', 'wall_north',
        'wall_north_east', 'wall_north_east_south', 'wall_north_east_south_west', 'wall_north_east_west',
        'wall_north_south', 'wall_north_south_west', 'wall_north_west', 'wall_south', 'wall_south_west',
        'wall_west', 
    )
    
    def __new__(
        cls,
        
        character_east_on_floor,
        character_east_on_hole_filled,
        character_east_on_obstacle_destroyed,
        character_east_on_target_on_floor,
        character_north_on_floor,
        character_north_on_hole_filled,
        character_north_on_obstacle_destroyed,
        character_north_on_target_on_floor,
        character_south_on_floor,
        character_south_on_hole_filled,
        character_south_on_obstacle_destroyed,
        character_south_on_target_on_floor,
        character_west_on_floor,
        character_west_on_hole_filled,
        character_west_on_obstacle_destroyed,
        character_west_on_target_on_floor,
        
        other_box_on_floor,
        other_box_on_hole_filled,
        other_box_on_obstacle_destroyed,
        other_box_on_target,
        other_floor,
        other_hole,
        other_hole_filled,
        other_obstacle,
        other_obstacle_destroyed,
        other_target_on_floor,
        
        wall,
        wall_east,
        wall_east_south,
        wall_east_south_west,
        wall_east_west,
        wall_north,
        wall_north_east,
        wall_north_east_south,
        wall_north_east_south_west,
        wall_north_east_west,
        wall_north_south,
        wall_north_south_west,
        wall_north_west,
        wall_south,
        wall_south_west,
        wall_west,
    ):
        """
        Creates a new tile emoji mapping.
        
        Attributes
        ----------
        character_east_on_floor : ``Emoji``
            Character looking east-wards on a floor.
        
        character_east_on_hole_filled : ``Emoji``
            Character looking east-wards on a filled hole.
        
        character_east_on_obstacle_destroyed : ``Emoji``
            Character looking east-wards on a destroyed obstacle.
        
        character_east_on_target_on_floor : ``Emoji``
            Character looking east-wards on a target floor.
        
        character_north_on_floor : ``Emoji``
            Character looking north-wards on a floor.
        
        character_north_on_hole_filled : ``Emoji``
            Character looking north-wards on a filled hole.
        
        character_north_on_obstacle_destroyed : ``Emoji``
            Character looking north-wards on a destroyed obstacle.
        
        character_north_on_target_on_floor : ``Emoji``
            Character looking north-wards on a target floor.
        
        character_south_on_floor : ``Emoji``
            Character looking south-wards on a floor.
        
        character_south_on_hole_filled : ``Emoji``
            Character looking south-wards on a filled hole.
        
        character_south_on_obstacle_destroyed : ``Emoji``
            Character looking south-wards on a destroyed obstacle.
        
        character_south_on_target_on_floor : ``Emoji``
            Character looking south-wards on a target floor.
        
        character_west_on_floor : ``Emoji``
            Character looking west-wards on a floor.
        
        character_west_on_hole_filled : ``Emoji``
            Character looking west-wards on a filled hole.
        
        character_west_on_obstacle_destroyed : ``Emoji``
            Character looking west-wards on a destroyed obstacle.
        
        character_west_on_target_on_floor : ``Emoji``
            Character looking west-wards on a target floor.
        
        other_box_on_floor : ``Emoji``
            Box on a floor.
        
        other_box_on_hole_filled : ``Emoji``
            Box on a filled hole.
        
        other_box_on_obstacle_destroyed : ``Emoji``
            Box on a destroyed obstacle.
        
        other_box_on_target : ``Emoji``
            Box on a target floor.
        
        other_floor : ``Emoji``
            Floor.
        
        other_hole : ``Emoji``
            Hole.
        
        other_hole_filled : ``Emoji``
            Filled hole.
        
        other_obstacle : ``Emoji``
            Obstacle.
        
        other_obstacle_destroyed : ``Emoji``
            Destroyed obstacle.
        
        other_target_on_floor : ``Emoji``
            Target on a floor.
        
        wall : ``Emoji``
            Empty wall tile used where wall has no direction.
        
        wall_east : ``Emoji``
            East side wall.
        
        wall_east_south : ``Emoji``
            East and south side wall.
        
        wall_east_south_west : ``Emoji``
            East, south and west side wall.
        
        wall_east_west : ``Emoji``
            East and west side wall.
        
        wall_north : ``Emoji``
            North side wall. This tile is visible so not like other walls, has an actual chapter specific asset.
        
        wall_north_east : ``Emoji``
            North and east side wall.
        
        wall_north_east_south : ``Emoji``
            North, east  and south side wall.
            
        wall_north_east_south_west : ``Emoji``
            North, east, south as west side wall.
        
        wall_north_east_west : ``Emoji``
            North, east and west side wall.
        
        wall_north_south : ``Emoji``
            North and south side wall.
        
        wall_north_south_west : ``Emoji``
            North, south and west side wall.
        
        wall_north_west : ``Emoji``
            North and west side wall.
        
        wall_south : ``Emoji``
            South side wall.
        
        wall_south_west : ``Emoji``
            South and west side wall.
        
        wall_west : ``Emoji``
            West side wall.
        """
        self = object.__new__(cls)
        
        self.character_east_on_floor = character_east_on_floor
        self.character_east_on_hole_filled = character_east_on_hole_filled
        self.character_east_on_obstacle_destroyed = character_east_on_obstacle_destroyed
        self.character_east_on_target_on_floor = character_east_on_target_on_floor
        self.character_north_on_floor = character_north_on_floor
        self.character_north_on_hole_filled = character_north_on_hole_filled
        self.character_north_on_obstacle_destroyed = character_north_on_obstacle_destroyed
        self.character_north_on_target_on_floor = character_north_on_target_on_floor
        self.character_south_on_floor = character_south_on_floor
        self.character_south_on_hole_filled = character_south_on_hole_filled
        self.character_south_on_obstacle_destroyed = character_south_on_obstacle_destroyed
        self.character_south_on_target_on_floor = character_south_on_target_on_floor
        self.character_west_on_floor = character_west_on_floor
        self.character_west_on_hole_filled = character_west_on_hole_filled
        self.character_west_on_obstacle_destroyed = character_west_on_obstacle_destroyed
        self.character_west_on_target_on_floor = character_west_on_target_on_floor
        
        self.other_box_on_floor = other_box_on_floor
        self.other_box_on_hole_filled = other_box_on_hole_filled
        self.other_box_on_obstacle_destroyed = other_box_on_obstacle_destroyed
        self.other_box_on_target = other_box_on_target
        self.other_floor = other_floor
        self.other_hole = other_hole
        self.other_hole_filled = other_hole_filled
        self.other_obstacle = other_obstacle
        self.other_obstacle_destroyed = other_obstacle_destroyed
        self.other_target_on_floor = other_target_on_floor
        
        self.wall = wall
        self.wall_east = wall_east
        self.wall_east_south = wall_east_south
        self.wall_east_south_west = wall_east_south_west
        self.wall_east_west = wall_east_west
        self.wall_north = wall_north
        self.wall_north_east = wall_north_east
        self.wall_north_east_south = wall_north_east_south
        self.wall_north_east_south_west = wall_north_east_south_west
        self.wall_north_east_west = wall_north_east_west
        self.wall_north_south = wall_north_south
        self.wall_north_south_west = wall_north_south_west
        self.wall_north_west = wall_north_west
        self.wall_south = wall_south
        self.wall_south_west = wall_south_west
        self.wall_west = wall_west
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # Nothing here.
        
        repr_parts.append('>')
        return ''.join(repr_parts)
