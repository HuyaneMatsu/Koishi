import vampytest

from ..instantiate_inheritance import InstantiateInheritanceMeta


def test__InstantiateInheritanceMeta__new_type():
    """
    Tests whether ``InstantiateInheritanceMeta`` works as intended.
    
    Case: new type.
    """
    class new_type(metaclass = InstantiateInheritanceMeta):
        __slots__ = ('hey', 'mister')
        hey = 12
    
    
    vampytest.assert_instance(new_type, InstantiateInheritanceMeta)
    vampytest.assert_eq(new_type.__slots__, ('hey', 'mister'))
    vampytest.assert_eq(new_type.__attributes__, (('hey', True, 12), ('mister', False, None)))
    vampytest.assert_true(hasattr(new_type.hey, '__get__'))
    vampytest.assert_true(hasattr(new_type.mister, '__get__'))


def test__InstantiateInheritanceMeta__instantiation():
    """
    Tests whether ``InstantiateInheritanceMeta`` works as intended.
    
    Case: new type.
    """
    class new_type(metaclass = InstantiateInheritanceMeta):
        __slots__ = ('hey', 'mister')
        hey = 12
    
    
    class instance(new_type):
        mister = 15
    
    vampytest.assert_instance(instance, new_type)
    vampytest.assert_eq(instance.hey, 12)
    vampytest.assert_eq(instance.mister, 15)
