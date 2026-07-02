__all__ = ('EntryStructure', 'Structure',)

from collections import _tuplegetter as TupleGetter

from .constants import FIELD_FLAG_LISTING
from .data_base_field import DataBaseField
from .data_type import DataType
from .data_types import ENTRY_ID


def collect_fields(meta_type, base_types, type_attributes):
    """
    Collects fields.
    
    Parameters
    ----------
    meta_type : `type`
        Meta type for parents which should have fields pulled from.
    
    base_types : `tuple<type>`
        Base types.
    
    type_attributes : `dict<str, object>`
        Attributes to create the types with.
    
    Returns
    -------
    fields : ``tuple<DataBaseField>``
    """
    fields = []
    
    for base_type in base_types:
        if isinstance(base_type, meta_type):
            if fields:
                raise RuntimeError(
                    f'Multiple parents with fields are not supported; second_parent_with_fields = {base_type.__name__}'
                )
            
            fields.extend(base_type.__fields__)
    
    for attribute_name, attribute_value in type_attributes.items():
        if isinstance(attribute_value, DataType):
            fields.append(DataBaseField(attribute_name, attribute_value))
    
    return tuple(fields)


def insert_descriptors(fields, type_attributes, index):
    """
    Inserts descriptors representing the fields into the the type attributes.
    
    Parameters
    ----------
    fields : ``tuple<DataBaseField>``
        Fields to create descriptors for.
    
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    
    index : `int`
        Index to start creating descriptors starting at.
    """
    for field in fields:
        type_attributes[field.name] = TupleGetter(index, None)
        index += 1


def insert_tuple_to_base_types(base_types):
    """
    Inserts tuple to base types if omitted.
    
    Parameters
    ----------
    base_types : `tuple<type>`
        The parent types.
    
    Returns
    -------
    base_types : `tuple<type>`
    """
    do_insert_tuple = True
    for base_type in base_types:
        if issubclass(base_type, tuple):
            do_insert_tuple = False
            break
    
    if do_insert_tuple:
        base_types = (tuple, *base_types)
    
    return base_types


def get_fields_description(fields):
    """
    Describes fields in a serialisable manner.
    
    Parameters
    ----------
    fields : ``tuple<DataBaseField>``
        Fields to describe to.
    
    Returns
    -------
    fields_description : ``tuple<(int, str, int, (None | ...))>``
    """
    fields_description = []
    
    for field in fields:
        flags = 0
        data_type = field.data_type
        type_representation = data_type.type_representation
        if not isinstance(type_representation, Structure):
            sub_description = None
        else:
            sub_description = get_fields_description(type_representation.__fields__)
        
        if data_type.type_representation_wrapped_into_list:
            flags |= FIELD_FLAG_LISTING
        
        fields_description.append((flags, field.name, data_type.id, sub_description))
    
    return tuple(fields_description)


def get_representation_structure(structure):
    """
    Gets the representation of a structure.
    
    Parameters
    ----------
    structure : ``instance<instance<Structure>>``
        Structure to get representation for.
    
    Returns
    -------
    representation : `str`
    """
    repr_parts = ['<', type(structure).__name__]
    field_added = False
    
    for value, field in zip(structure, structure.__fields__):
        if field_added:
            repr_parts.append(', ')
        repr_parts.append(field.name)
        repr_parts.append(' = ')
        repr_parts.append(repr(value))
    
    repr_parts.append('>')
    return ''.join(repr_parts)


def get_representation_entry_structure(entry_structure):
    """
    Gets the representation of a structure.
    
    Parameters
    ----------
    entry_structure : ``instance<instance<EntryStructure>>``
        Entry structure to get representation for.
    
    Returns
    -------
    representation : `str`
    """
    repr_parts = ['<', type(entry_structure).__name__]
    field_added = False
    
    fields = entry_structure.__fields__
    for index in range(len(fields)):
        value = entry_structure[index]
        field = fields[index]
        
        if field_added:
            repr_parts.append(', ')
        repr_parts.append(field.name)
        repr_parts.append(' = ')
        repr_parts.append(repr(value))
    
    repr_parts.append('>')
    return ''.join(repr_parts)


def insert_get_representation_function(base_types, type_attributes, get_representation_function):
    """
    Inserts a get representation function into `type_attributes` if cannot find custom definition.
    
    Parameters
    ----------
    base_types : `tuple<type>`
        Base types.
    
    type_attributes : `dict<str, object>`
        Attributes to create the types with.
    
    get_representation_function : `Function`
        Function to insert if non found.
    """
    if '__repr__' in type_attributes:
        return
    
    for base_type in base_types:
        get_representation = base_type.__repr__
        if (get_representation is not object.__repr__) and (get_representation is not tuple.__repr__):
            return
    
    type_attributes['__repr__'] = get_representation_function


class Structure(type):
    """
    Meta type for structures.
    """
    def __new__(cls, type_name, base_types, type_attributes):
        """
        Creates a new builder type.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        base_types : `tuple<type>`
            The parent types.
        
        type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
        """
        fields = collect_fields(cls, base_types, type_attributes)
        
        for field in fields:
            if field.data_type is ENTRY_ID:
                raise ValueError(f'No fields can be {ENTRY_ID.name}; but {field.name} is.')
        
        type_attributes['__fields__'] = fields
        
        # Create descriptors.
        insert_descriptors(fields, type_attributes, 0)
        # Add `__repr__` function.
        insert_get_representation_function(base_types, type_attributes, get_representation_structure)
        
        # Check whether tuple should be inserted.
        base_types = insert_tuple_to_base_types(base_types)
        
        # Build type.
        return type.__new__(cls, type_name, base_types, type_attributes)


class EntryStructure(type):
    """
    Meta type for entries.
    """
    def __new__(cls, type_name, base_types, type_attributes):
        """
        Creates a new builder type.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        base_types : `tuple<type>`
            The parent types.
        
        type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
        """
        fields = collect_fields(cls, base_types, type_attributes)
        
        field_0 = fields[0]
        if field_0.data_type is not ENTRY_ID:
            raise ValueError(f'Field 0 must be {ENTRY_ID.name}; got {field_0.name}!')
        
        fields = tuple(fields)
        type_attributes['__fields__'] = fields
        
        # Create descriptors.
        insert_descriptors(fields, type_attributes, 2)
        # Add `__repr__` function.
        insert_get_representation_function(base_types, type_attributes, get_representation_entry_structure)
        
        # Check whether tuple should be inserted.
        base_types = insert_tuple_to_base_types(base_types)
        
        # Build type.
        return type.__new__(cls, type_name, base_types, type_attributes)
