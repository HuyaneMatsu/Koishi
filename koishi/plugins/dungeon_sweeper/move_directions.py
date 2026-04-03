__all__ = ()

from scarletio import RichAttributeErrorBaseType


MOVE_DIRECTION_NORTH = 1
MOVE_DIRECTION_EAST = 2
MOVE_DIRECTION_SOUTH = 3
MOVE_DIRECTION_WEST = 4
MOVE_DIRECTION_NORTH_TO_EAST = 5
MOVE_DIRECTION_NORTH_TO_WEST = 6
MOVE_DIRECTION_SOUTH_TO_EAST = 7
MOVE_DIRECTION_SOUTH_TO_WEST = 8
MOVE_DIRECTION_EAST_TO_NORTH = 9
MOVE_DIRECTION_EAST_TO_SOUTH = 10
MOVE_DIRECTION_WEST_TO_NORTH = 11
MOVE_DIRECTION_WEST_TO_SOUTH = 12


DIRECTIONS_MAIN = (
    MOVE_DIRECTION_NORTH,
    MOVE_DIRECTION_EAST,
    MOVE_DIRECTION_SOUTH,
    MOVE_DIRECTION_WEST,
)

DIRECTION_DIAGONAL = (
    (MOVE_DIRECTION_NORTH_TO_EAST, MOVE_DIRECTION_EAST_TO_NORTH),
    (MOVE_DIRECTION_EAST_TO_SOUTH, MOVE_DIRECTION_SOUTH_TO_EAST),
    (MOVE_DIRECTION_SOUTH_TO_WEST, MOVE_DIRECTION_WEST_TO_SOUTH),
    (MOVE_DIRECTION_WEST_TO_NORTH, MOVE_DIRECTION_NORTH_TO_WEST),
)


class MoveDirections(RichAttributeErrorBaseType):
    """
    Container class to store to which positions a character can move or use skill.
    
    Attributes
    ----------
    directions : `set<int>`
        The allowed directions.
    """
    __slots__ = ('directions',)
    
    def __new__(cls):
        """
        Creates a new move direction holder.
        
        It holds to which directions the player can move.
        """
        self = object.__new__(cls)
        self.directions = set()
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # directions
        repr_parts.append(' directions = ')
        repr_parts.append(repr(self.directions))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.directions != other.directions:
            return False
        
        return True
    
    
    def set(self, direction, value):
        """
        Sets the given direction identifier to the given value.
        
        Parameters
        ----------
        direction : `int`
            The direction to set.
        value : `bool`
            Whether to enable the direction.
        """
        if value:
            self.directions.add(direction)
        else:
            self.directions.discard(direction)
    
    
    def get(self, direction):
        """
        Gets whether the given direction is enabled.
        
        Parameters
        ----------
        direction : `int`
            The direction to set.
        
        Returns
        -------
        value : `bool`
        """
        return (direction in self.directions)
