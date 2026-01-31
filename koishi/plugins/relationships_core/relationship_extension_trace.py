__all__ = ('RelationshipExtensionTrace',)

from scarletio import RichAttributeErrorBaseType

from .relationship_types import produce_relationship_type_name_advanced


class RelationshipExtensionTrace(RichAttributeErrorBaseType):
    """
    Represents a relationship extension trace, storing the closest first route to the source.
    
    Attributes
    ----------
    relationship_route : ``tuple<Relationship>``
        The closest first route from the source.
    
    relationship_type : `int`
        The relationship type from the source user.
    
    user_id : `int`
        The represented user's identifier.
    """
    __slots__ = ('relationship_route', 'relationship_type', 'user_id')
    
    def __new__(cls, user_id, relationship_type, relationship_route):
        """
        Creates a new instance.
        
        Parameters
        ----------
        user_id : `int`
            The represented user's identifier.
        
        relationship_type : `int`
            The relationship type from the source user.
        
        relationship_route : ``tuple<Relationship>``
            The closest first route from the source.
        """
        self = object.__new__(cls)
        self.user_id = user_id
        self.relationship_type = relationship_type
        self.relationship_route = relationship_route
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # relationship_type
        repr_parts.append(', relationship_type = ')
        relationship_type = self.relationship_type
        repr_parts.append(repr(relationship_type))
        repr_parts.append(' ~ ')
        repr_parts.extend(produce_relationship_type_name_advanced(relationship_type))
        
        # relationship_route
        repr_parts.append(', relationship_route = ')
        repr_parts.append(repr(self.relationship_route))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        # relationship_type
        if self.relationship_type != other.relationship_type:
            return False
        
        # relationship_route
        if self.relationship_route != other.relationship_route:
            return False
        
        return True
