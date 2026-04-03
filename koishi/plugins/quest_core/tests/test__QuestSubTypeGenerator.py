from random import Random

import vampytest

from ..sub_type_bases import QuestSubTypeGenerator, QuestSubTypeInstantiable


def _assert_fields_set(quest_sub_type_generator):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_sub_type_generator : ``QuestSubTypeGenerator``
        The instance to check.
    """
    vampytest.assert_instance(quest_sub_type_generator, QuestSubTypeGenerator)
    vampytest.assert_eq(quest_sub_type_generator.TYPE, 0)


def test__QuestSubTypeGenerator__new():
    """
    Tests whether ``QuestSubTypeGenerator.__new__`` works as intended.
    """
    quest_sub_type_generator = QuestSubTypeGenerator()
    _assert_fields_set(quest_sub_type_generator)


def test__QuestSubTypeGenerator__repr():
    """
    Tests whether ``QuestSubTypeGenerator.__repr__`` works as intended.
    """
    quest_sub_type_generator = QuestSubTypeGenerator()
    
    output = repr(quest_sub_type_generator)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestSubTypeGenerator__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestSubTypeGenerator.__eq__`` works as intended.
    
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
    quest_sub_type_generator_0 = QuestSubTypeGenerator(*position_parameters_0)
    quest_sub_type_generator_1 = QuestSubTypeGenerator(*position_parameters_1)
    
    output = quest_sub_type_generator_0 == quest_sub_type_generator_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestSubTypeGenerator__generate():
    """
    Tests whether ``QuestSubTypeGenerator.generate`` works as intended.
    """
    quest_sub_type_generator = QuestSubTypeGenerator()
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_sub_type_generator.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestSubTypeInstantiable(),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )


def test__QuestSubTypeGenerator__generate_with_diversion():
    """
    Tests whether ``QuestSubTypeGenerator.generate`` works as intended.
    """
    quest_sub_type_generator = QuestSubTypeGenerator()
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_sub_type_generator.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestSubTypeInstantiable(),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
