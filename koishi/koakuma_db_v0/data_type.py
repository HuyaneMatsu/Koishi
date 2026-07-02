__all__ = ()

from scarletio import RichAttributeErrorBaseType


class DataType(RichAttributeErrorBaseType):
    """
    Represents a data type.
    
    Attributes
    ----------
    get_length : `FunctionType`
        Length getter.
    
    id : `int`
        The data type's identifier.
    
    name : `str`
        The data type's name.
    
    producer : `FunctionType`
        Serialiser function.
    
    reader : `FunctionType`
        Reader function.
    
    type_representation : `type`
        What type does this data type represents.
    
    type_representation_nullable : `bool`
        Whether ``.type_representation`` is nullable.
    
    type_representation_wrapped_into_list : `bool`
        Whether the represented type is wrapped into a list.
    """
    __slots__ = (
        'get_length', 'id', 'name', 'producer', 'reader', 'type_representation', 'type_representation_nullable',
        'type_representation_wrapped_into_list',
    )
    
    def __new__(
        cls,
        data_type_id,
        name,
        type_representation,
        type_representation_nullable,
        type_representation_wrapped_into_list,
        reader,
        producer,
        get_length,
    ):
        """
        Creates a new data type.
        
        Parameters
        ----------
        data_type_id : `int`
            The data type's identifier.
        
        name : `str`
            The data type's name.
        
        type_representation : `type`
            What type does this data type represents.
        
        type_representation_nullable : `bool`
            Whether ``.type_representation`` is nullable.
        
        type_representation_wrapped_into_list : `bool`
            Whether the represented type is wrapped into a list.
        
        reader : `FunctionType`
            Reader function.
        
        producer : `FunctionType`
            Serialiser function.
        
        get_length : `FunctionType`
            Length getter.
        """
        self = object.__new__(cls)
        self.id = data_type_id
        self.get_length = get_length
        self.name = name
        self.producer = producer
        self.reader = reader
        self.type_representation = type_representation
        self.type_representation_nullable = type_representation_nullable
        self.type_representation_wrapped_into_list = type_representation_wrapped_into_list
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
