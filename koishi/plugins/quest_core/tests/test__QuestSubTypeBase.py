import vampytest

from ..sub_type_bases import QuestSubTypeBase


def _assert_fields_set(quest_sub_type_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_sub_type_base : ``QuestSubTypeBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_sub_type_base, QuestSubTypeBase)
    vampytest.assert_eq(quest_sub_type_base.TYPE, 0)


def test__QuestSubTypeBase__new():
    """
    Tests whether ``QuestSubTypeBase.__new__`` works as intended.
    """
    quest_sub_type_base = QuestSubTypeBase()
    _assert_fields_set(quest_sub_type_base)


def test__QuestSubTypeBase__repr():
    """
    Tests whether ``QuestSubTypeBase.__repr__`` works as intended.
    """
    quest_sub_type_base = QuestSubTypeBase()
    
    output = repr(quest_sub_type_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestSubTypeBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestSubTypeBase.__eq__`` works as intended.
    
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
    quest_sub_type_base_0 = QuestSubTypeBase(*position_parameters_0)
    quest_sub_type_base_1 = QuestSubTypeBase(*position_parameters_1)
    
    output = quest_sub_type_base_0 == quest_sub_type_base_1
    vampytest.assert_instance(output, bool)
    return output
