__all__ = ('Skill',)

from scarletio import RichAttributeErrorBaseType


class Skill(RichAttributeErrorBaseType):
    """
    Represent a skill.
    
    Attributes
    ----------
    can_activate : `FunctionType`
        Checks whether the chapter's character's skill can be activated.
        
        Accepts the following parameters.
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | game_state    | ``GameState`` |
        +---------------+---------------+
        
        Should returns the following values.
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | can_active    | `bool`        |
        +---------------+---------------+
    
    get_directions : `FunctionType`
        Checks whether the chapter's character's skill can be activated.
        
        Accepts the following parameters.
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | game_state    | ``GameState`` |
        +---------------+---------------+
        
        Should returns the following values.
        
        +-------------------+-----------------------+
        | Name              | Type                  |
        +===================+=======================+
        | move_directions  | ``MoveDirections``     |
        +-------------------+-----------------------+
    
    id : `int`
        The skill's identifier.
    
    use : `FunctionType`
        Uses the skill of the chapter's character.
        
        Accepts the following parameters.
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | game_state    | ``GameState`` |
        +---------------+---------------+
        | step          | `int`         |
        +---------------+---------------+
        | align         | `int`         |
        +---------------+---------------+
        
        Should returns the following values.
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | success       | `bool`        |
        +---------------+---------------+
    """
    __slots__ = ('can_activate', 'get_directions', 'id', 'use')
    
    def __new__(cls, skill_id, can_activate, get_directions, use):
        """
        Creates a new skill.
        
        Parameters
        ----------
        skill_id : `int`
            The skill's identifier.
        
        can_activate : `FunctionType`
            Checks whether the chapter's character's skill can be activated.
        
        get_directions : `FunctionType`
            Checks whether the chapter's character's skill can be activated.
        
        use : `FunctionType`
            Uses the skill of the chapter's character.
        """
        self = object.__new__(cls)
        self.can_activate = can_activate
        self.id = skill_id
        self.get_directions = get_directions
        self.use = use
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
