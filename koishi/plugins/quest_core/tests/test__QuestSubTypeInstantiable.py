import vampytest

from ..sub_type_bases import QuestSubTypeInstantiable, QuestSubTypeSerialisable


def _assert_fields_set(quest_sub_type_instantiable):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_sub_type_instantiable : ``QuestSubTypeInstantiable``
        The instance to check.
    """
    vampytest.assert_instance(quest_sub_type_instantiable, QuestSubTypeInstantiable)
    vampytest.assert_eq(quest_sub_type_instantiable.TYPE, 0)


def test__QuestSubTypeInstantiable__new():
    """
    Tests whether ``QuestSubTypeInstantiable.__new__`` works as intended.
    """
    quest_sub_type_instantiable = QuestSubTypeInstantiable()
    _assert_fields_set(quest_sub_type_instantiable)


def test__QuestSubTypeInstantiable__repr():
    """
    Tests whether ``QuestSubTypeInstantiable.__repr__`` works as intended.
    """
    quest_sub_type_instantiable = QuestSubTypeInstantiable()
    
    output = repr(quest_sub_type_instantiable)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestSubTypeInstantiable__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestSubTypeInstantiable.__eq__`` works as intended.
    
    Parameters
    ----------
    position_parameters_0 : `tuple<object>`
        Positional parameters to create instance form.
    
    position_parameters_1 : `tuple<object>`
        Positional parameters to create instance form.
    
    Returns
    -------
    output : `bool`
    """
    quest_sub_type_instantiable_0 = QuestSubTypeInstantiable(*position_parameters_0)
    quest_sub_type_instantiable_1 = QuestSubTypeInstantiable(*position_parameters_1)
    
    output = quest_sub_type_instantiable_0 == quest_sub_type_instantiable_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestSubTypeInstantiable__instantiate():
    """
    Tests whether ``QuestSubTypeInstantiable.instantiate`` works as intended.
    """
    quest_sub_type_instantiable = QuestSubTypeInstantiable()
    
    output = quest_sub_type_instantiable.instantiate()
    
    vampytest.assert_eq(
        output,
        QuestSubTypeSerialisable(),
    )
