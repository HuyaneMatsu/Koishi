from types import FunctionType

import vampytest

from ..chat_interaction import ChatInteraction



def function_0(client, message):
    return None


async def function_1(client, message, outcome):
    return None


def _assert_fields_set(chat_interaction):
    """
    Asserts whether every attributes of the welcome style are set.
    
    Parameters
    ----------
    chat_interaction : ``ChatInteraction``
        The welcome style to check.
    """
    vampytest.assert_instance(chat_interaction, ChatInteraction)
    vampytest.assert_instance(chat_interaction.check_can_trigger, FunctionType)
    vampytest.assert_instance(chat_interaction.name, str)
    vampytest.assert_instance(chat_interaction.trigger, FunctionType)


def test__ChatInteraction__new():
    """
    Tests whether ``ChatInteraction.__new__`` works as intended.
    """
    name = 'koishi'
    check_can_trigger = function_0
    trigger = function_1
    
    chat_interaction = ChatInteraction(
        name,
        check_can_trigger,
        trigger,
    )
    _assert_fields_set(chat_interaction)
    
    vampytest.assert_is(chat_interaction.check_can_trigger, check_can_trigger)
    vampytest.assert_eq(chat_interaction.name, name)
    vampytest.assert_is(chat_interaction.trigger, trigger)


def test__ChatInteraction__repr():
    """
    Tests whether ``ChatInteraction.__repr__`` works as intended.
    """
    name = 'koishi'
    check_can_trigger = function_0
    trigger = function_1
    
    chat_interaction = ChatInteraction(
        name,
        check_can_trigger,
        trigger,
    )
    
    vampytest.assert_instance(repr(chat_interaction), str)
