import vampytest

from ....touhou_core import TouhouCharacter, YAKUMO_RAN, YAKUMO_YUKARI

from ..action import ImageDetailAction


def _assert_fields_set(image_detail_action):
    """
    Asserts whether every fields are set of the given image detail tag.
    
    Parameters
    ----------
    image_detail_action : ``ImageDetailAction``
        Image detail tag to test.
    """
    vampytest.assert_instance(image_detail_action, ImageDetailAction)
    vampytest.assert_instance(image_detail_action.tag, str)
    vampytest.assert_instance(image_detail_action.source, TouhouCharacter, nullable = True)
    vampytest.assert_instance(image_detail_action.target, TouhouCharacter, nullable = True)


def test__ImageDetailAction__new():
    """
    Tests whether ``ImageDetailAction.__new__`` works as intended.
    """
    tag = 'kiss'
    source = YAKUMO_RAN
    target = YAKUMO_YUKARI
    
    image_detail_action = ImageDetailAction(tag, source, target)
    _assert_fields_set(image_detail_action)
    
    vampytest.assert_eq(image_detail_action.tag, tag)
    vampytest.assert_is(image_detail_action.source, source)
    vampytest.assert_is(image_detail_action.target, target)


def test__ImageDetailAction__repr():
    """
    Tests whether ``ImageDetailAction.__repr__`` works as intended.
    """
    tag = 'kiss'
    source = YAKUMO_RAN
    target = YAKUMO_YUKARI
    
    image_detail_action = ImageDetailAction(tag, source, target)
    
    output = repr(image_detail_action)
    vampytest.assert_instance(output, str)


def test__ImageDetailAction__hash():
    """
    Tests whether ``ImageDetailAction.__hash__`` works as intended.
    """
    tag = 'kiss'
    source = YAKUMO_RAN
    target = YAKUMO_YUKARI
    
    image_detail_action = ImageDetailAction(tag, source, target)
    
    output = hash(image_detail_action)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        True,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'lick',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_YUKARI,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_RAN,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': None,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': None,
        },
        False,
    )

@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ImageDetailAction__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageDetailAction.__eq__`` works as intended.
    
    Case: same type.
    
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
    image_detail_action_0 = ImageDetailAction(**keyword_parameters_0)
    image_detail_action_1 = ImageDetailAction(**keyword_parameters_1)
    
    output = image_detail_action_0 == image_detail_action_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__different_type():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()))
def test__ImageDetailAction__eq__different_type(other):
    """
    Tests whether ``ImageDetailAction.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other instance to convert the image detail tag to.
    
    Returns
    -------
    output : `bool`
    """
    tag = 'kiss'
    source = YAKUMO_RAN
    target = YAKUMO_YUKARI
    
    image_detail_action = ImageDetailAction(tag, source, target)
    
    output = image_detail_action == other
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ImageDetailAction__unpack():
    """
    Tests whether ``ImageDetailAction`` unpacking works as intended.
    """
    tag = 'kiss'
    source = YAKUMO_RAN
    target = YAKUMO_YUKARI
    
    image_detail_action = ImageDetailAction(tag, source, target)
    
    output = [*image_detail_action]
    vampytest.assert_eq(len(output), len(image_detail_action))


def _iter_options__iter_characters():
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            YAKUMO_RAN,
            YAKUMO_YUKARI,
        },
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': None,
        },
        {
            YAKUMO_RAN,
        },
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': None,
            'target': YAKUMO_YUKARI,
        },
        {
            YAKUMO_YUKARI,
        },
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': None,
            'target': None,
        },
        set(),
    )


@vampytest._(vampytest.call_from(_iter_options__iter_characters()).returning_last())
def test__ImageDetailAction__iter_characters(keyword_parameters):
    """
    Tests whether ``ImageDetailAction.iter_characters`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `set<TouhouCharacter>`
    """
    image_detail_action = ImageDetailAction(**keyword_parameters)
    
    output = {*image_detail_action.iter_characters()}
    
    for element in output:
        vampytest.assert_instance(element, TouhouCharacter)
    
    return output


def _iter_options__gt__same_type():
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'lick',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'lick',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        True,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_YUKARI,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_YUKARI,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_RAN,
        },
        True,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': None,
            'target': YAKUMO_YUKARI,
        },
        True,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': None,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        False,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': None,
        },
        True,
    )
    
    yield (
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': None,
        },
        {
            'tag': 'kiss',
            'source': YAKUMO_RAN,
            'target': YAKUMO_YUKARI,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__gt__same_type()).returning_last())
def test__ImageDetailAction__gt__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageDetailAction.__gt__`` works as intended.
    
    Case: same type.
    
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
    image_detail_action_0 = ImageDetailAction(**keyword_parameters_0)
    image_detail_action_1 = ImageDetailAction(**keyword_parameters_1)
    
    output = image_detail_action_0 > image_detail_action_1
    vampytest.assert_instance(output, bool)
    return output
