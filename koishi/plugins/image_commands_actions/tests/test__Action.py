import vampytest

from ...image_handling_core import ImageHandlerBase

from ..action import Action
from ..asset_listings.constants import ACTION_TAG_POCKY_KISS, ACTION_TAG_POCKY_KISS_SELF
from ..image_handlers import IMAGE_HANDLER_POCKY_KISS, IMAGE_HANDLER_POCKY_KISS_SELF 


def _assert_fields_set(action):
    """
    Asserts whether every fields of the given `action` are set.
    
    Parameters
    ----------
    action : ``Action``
    """
    vampytest.assert_instance(action, Action)
    vampytest.assert_instance(action.aliases, tuple, nullable = True)
    vampytest.assert_instance(action.description, str)
    vampytest.assert_instance(action.handler, ImageHandlerBase)
    vampytest.assert_instance(action.handler_self, ImageHandlerBase, nullable = True)
    vampytest.assert_instance(action.name, str)
    vampytest.assert_instance(action.starter_text, str, nullable = True)
    vampytest.assert_instance(action.verb, str)


def test__Action__new__min():
    """
    Tests whether ``Action.__new__`` works as intended.
    
    Case: Minimal amount of fields given.
    """
    name = 'hug'
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    
    action = Action(
        name,
        description,
        handler,
        verb,
    )
    _assert_fields_set(action)
    
    vampytest.assert_eq(action.aliases, None)
    vampytest.assert_eq(action.description, description)
    vampytest.assert_is(action.handler, handler)
    vampytest.assert_is(action.handler_self, None)
    vampytest.assert_eq(action.name, name)
    vampytest.assert_eq(action.verb, verb)


def test__Action__new__max():
    """
    Tests whether ``Action.__new__`` works as intended.
    
    Case: Maximal amount of fields given.
    """
    name = 'hug'
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    aliases = ('kiss', 'smooch')
    handler_self = IMAGE_HANDLER_POCKY_KISS_SELF
    starter_text = 'so true bestie'
    
    action = Action(
        name,
        description,
        handler,
        verb,
        aliases = aliases,
        handler_self = handler_self,
        starter_text = starter_text,
    )
    _assert_fields_set(action)
    
    vampytest.assert_eq(action.aliases, aliases)
    vampytest.assert_eq(action.description, description)
    vampytest.assert_is(action.handler, handler)
    vampytest.assert_is(action.handler_self, handler_self)
    vampytest.assert_eq(action.name, name)
    vampytest.assert_eq(action.starter_text, starter_text)
    vampytest.assert_eq(action.verb, verb)


def test__Action__repr():
    """
    Tests whether ``Action.__repr__`` works as intended.
    """
    name = 'hug'
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    aliases = ('kiss', 'smooch')
    handler_self = IMAGE_HANDLER_POCKY_KISS_SELF
    starter_text = 'so true bestie'
    
    action = Action(
        name,
        description,
        handler,
        verb,
        aliases = aliases,
        handler_self = handler_self,
        starter_text = starter_text,
    )
    
    output = repr(action)
    vampytest.assert_instance(output, str)


def _iter_options__iter_names():
    yield 'pudding', None, ['pudding']
    yield 'pudding', ('lord', ), ['pudding', 'lord']
    yield 'pudding', ('lord', 'sister'), ['pudding', 'lord', 'sister']


@vampytest._(vampytest.call_from(_iter_options__iter_names()).returning_last())
def test__Action__iter_names(name, aliases):
    """
    Tests whether ``Action.iter_names`` works as intended.
    
    Parameters
    ----------
    name : `str`
        Name of the action.
    aliases : `None | tuple<str>`
        Name aliases.
    
    Returns
    -------
    output : `list<str>`
    """
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    
    action = Action(
        name,
        description,
        handler,
        verb,
        aliases = aliases,
    )
    
    return [*action.iter_names()]


def test__Action__get_action_tag():
    """
    Tests whether ``Action.get_action_tag`` works as intended.
    """
    name = 'hug'
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    handler_self = IMAGE_HANDLER_POCKY_KISS_SELF
    
    action = Action(
        name,
        description,
        handler,
        verb,
        handler_self = handler_self,
    )
    
    output = action.get_action_tag()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, ACTION_TAG_POCKY_KISS)


def test__Action__get_action_tag_self():
    """
    Tests whether ``Action.get_action_tag_self`` works as intended.
    """
    name = 'hug'
    description = 'Huggu!!'
    handler = IMAGE_HANDLER_POCKY_KISS
    verb = 'hugs'
    handler_self = IMAGE_HANDLER_POCKY_KISS_SELF
    
    action = Action(
        name,
        description,
        handler,
        verb,
        handler_self = handler_self,
    )
    
    output = action.get_action_tag_self()
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_eq(output, ACTION_TAG_POCKY_KISS_SELF)
