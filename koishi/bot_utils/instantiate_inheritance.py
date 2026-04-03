__all__ = ()

from scarletio import RichAttributeErrorBaseType


def check_parameter_omitted(attributes, type_attributes):
    """
    Checks whether any attributes were omitted.
    
    Parameters
    ----------
    attributes : `tuple<(str, bool, object)>`
        Attributes to check with.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Raises
    ------
    TypeError
    """
    for attribute_name, attribute_has_default, attribute_default in attributes:
        if attribute_has_default:
            continue
        
        if attribute_name not in type_attributes:
            raise TypeError(f'It is required to define an {attribute_name!r} attribute.')


def instantiate(direct_parent, attributes, type_attributes):
    """
    Instantiates the given type.
    
    Parameters
    ----------
    direct_parent : `type`
        Type to instantiate.
    
    attributes : `tuple<(str, bool, object)>`
        Attributes to assign.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Returns
    -------
    instance : instance<direct_parent>`
    """
    instance = object.__new__(direct_parent)
    
    for attribute_name, attribute_has_default, attribute_default in attributes:
        try:
            attribute_value = type_attributes[attribute_name]
        except KeyError:
            attribute_value = attribute_default
        
        setattr(instance, attribute_name, attribute_value)
    
    return instance


def create_attributes(slots, type_attributes):
    """
    Creates the `__attributes__` field.
    
    Parameters
    ----------
    slots : `tuple<str>`
        Slots defining the attribute listing.
    
    type_attributes : `dict<str, object>`
        The assigned variables in the type's body.
    
    Returns
    -------
    attributes : `tuple<(str, bool, object)>`
    """
    attributes = []
    
    for attribute_name in slots:
        try:
            attribute_default = type_attributes.pop(attribute_name)
        except KeyError:
            attribute_default = None
            attribute_has_default = False
        else:
            attribute_has_default = True
        
        attributes.append((attribute_name, attribute_has_default, attribute_default))
    
    attributes.sort()
    return tuple(attributes)


class InstantiateInheritanceMeta(type):
    """
    Meta type that intercepts inheritance with instantiation.
    """
    def __new__(cls, type_name, type_parents, type_attributes):
        """
        Creates a new bitwise flag type.
        
        Parameters
        ----------
        type_name : `str`
            The created class's name.
        
        type_parents : `tuple<type>`
            The parent types of the type to create.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        
        Returns
        -------
        type : `instance<cls> | instance<instance<cls>>`
        
        Raises
        ------
        TypeError
            When any requirements are not satisfied.
        """
        if not type_parents:
            direct_parent = None
        else:
            direct_parent = type_parents[0]
        
        if (direct_parent is not None) and isinstance(direct_parent, cls):
            create_instance = True
        else:
            create_instance = False
        
        if create_instance:
            # Check for missing attributes.
            attributes = direct_parent.__attributes__
            check_parameter_omitted(attributes, type_attributes)
            return instantiate(direct_parent, attributes, type_attributes)
        
        try:
            slots = type_attributes['__slots__']
        except KeyError as exception:
            raise TypeError(f'Missing slots in {type_name!r}.') from exception
        
        type_attributes['__attributes__'] = create_attributes(slots, type_attributes)
        
        return type.__new__(cls, type_name, type_parents, type_attributes)
