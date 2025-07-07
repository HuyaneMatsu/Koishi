import vampytest
from hata import Emoji, SoundboardSound, Sticker

from ..choice import Choice
from ..choice_type import ChoiceTypeBase, ChoiceTypeEmoji, ChoiceTypeSticker


def _assert_fields_set(choice):
    """
    Asserts whether the choice has all of its fields set.
    
    Parameters
    ----------
    choice : ``Choice``
    """
    vampytest.assert_instance(choice, Choice)
    vampytest.assert_instance(choice.entity, Emoji, SoundboardSound, Sticker)
    vampytest.assert_subtype(choice.type, ChoiceTypeBase)


def test__Choice__new():
    """
    Tests whether ``Choice.__new__`` works as intended.
    """
    entity = Emoji.precreate(202506200100)
    choice_type = ChoiceTypeEmoji
    
    choice = Choice(entity, choice_type)
    _assert_fields_set(choice)
    vampytest.assert_is(choice.entity, entity)
    vampytest.assert_is(choice.type, choice_type)


def test__Choice__repr():
    """
    Tests whether ``Choice.__repr__`` works as intended.
    """
    entity = Emoji.precreate(202506200101)
    choice_type = ChoiceTypeEmoji
    
    choice = Choice(entity, choice_type)
    
    output = repr(choice)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    entity = Emoji.precreate(202506200102)
    choice_type = ChoiceTypeEmoji
    
    keyword_parameters = {
        'entity': entity,
        'choice_type' : choice_type,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'entity' : Emoji.precreate(202506200103)
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            'entity' : Sticker.precreate(202506200104),
            'choice_type': ChoiceTypeSticker,
        },
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Choice__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Choice.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    choice_0 = Choice(**keyword_parameters_0)
    choice_1 = Choice(**keyword_parameters_1)
    
    output = choice_0 == choice_1
    vampytest.assert_instance(output, bool)
    return output


def test__Choice__unpack():
    """
    Tests whether ``Choice`` unpacking works as intended.
    """
    entity = Emoji.precreate(202506200105)
    choice_type = ChoiceTypeEmoji
    
    choice = Choice(entity, choice_type)
    
    unpacked = [*choice]
    vampytest.assert_eq(len(unpacked), len(choice))
