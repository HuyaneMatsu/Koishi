import vampytest

from ..sub_type_bases import QuestSubTypeSerialisable


def _assert_fields_set(quest_sub_type_serialisable):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_sub_type_serialisable : ``QuestSubTypeSerialisable``
        The instance to check.
    """
    vampytest.assert_instance(quest_sub_type_serialisable, QuestSubTypeSerialisable)
    vampytest.assert_eq(quest_sub_type_serialisable.TYPE, 0)


def test__QuestSubTypeSerialisable__new():
    """
    Tests whether ``QuestSubTypeSerialisable.__new__`` works as intended.
    """
    quest_sub_type_serialisable = QuestSubTypeSerialisable()
    _assert_fields_set(quest_sub_type_serialisable)


def test__QuestSubTypeSerialisable__repr():
    """
    Tests whether ``QuestSubTypeSerialisable.__repr__`` works as intended.
    """
    quest_sub_type_serialisable = QuestSubTypeSerialisable()
    
    output = repr(quest_sub_type_serialisable)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestSubTypeSerialisable__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestSubTypeSerialisable.__eq__`` works as intended.
    
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
    quest_sub_type_serialisable_0 = QuestSubTypeSerialisable(*position_parameters_0)
    quest_sub_type_serialisable_1 = QuestSubTypeSerialisable(*position_parameters_1)
    
    output = quest_sub_type_serialisable_0 == quest_sub_type_serialisable_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestSubTypeSerialisable__deserialise():
    """
    Tests whether ``QuestSubTypeSerialisable.deserialise`` works as as intended.
    """
    data = b''
    start_index = 0
    
    quest_sub_type_serialisable, end_index = QuestSubTypeSerialisable.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_sub_type_serialisable)
    vampytest.assert_eq(end_index, 0)


def test__QuestSubTypeSerialisable__serialise():
    """
    Tests whether ``QuestSubTypeSerialisable.serialise`` works as intended.
    """
    quest_sub_type_serialisable = QuestSubTypeSerialisable()
    
    output = [*quest_sub_type_serialisable.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b'',
    )
