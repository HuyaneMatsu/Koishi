import vampytest

from ....touhou_core import CHEN, TouhouCharacter, YAKUMO_RAN, YAKUMO_YUKARI

from ...image_detail import ImageDetailAction, ImageDetailStatic

from ..custom import ImageDetailMatcherCustom


def _assert_fields_set(image_detail_matcher):
    """
    Asserts whether every fields are set of the given image detail matcher.
    
    Parameters
    ----------
    image_detail_matcher : ``ImageDetailMatcherCustom``
        The image detail matcher to assert.
    """
    vampytest.assert_instance(image_detail_matcher, ImageDetailMatcherCustom)
    vampytest.assert_instance(image_detail_matcher.action_tag, str, nullable = True)
    vampytest.assert_instance(image_detail_matcher.source, TouhouCharacter, nullable = True)
    vampytest.assert_instance(image_detail_matcher.name, str, nullable = True)
    vampytest.assert_instance(image_detail_matcher.target, TouhouCharacter, nullable = True)


def test__ImageDetailMatcherCustom__new():
    """
    Tests whether ``ImageDetailMatcherCustom.__new__`` works as intended.
    """
    action_tag = 'fluff'
    source = CHEN
    name = 'chen-ran'
    target = YAKUMO_RAN
    
    image_detail_matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    _assert_fields_set(image_detail_matcher)
    
    vampytest.assert_eq(image_detail_matcher.action_tag, action_tag)
    vampytest.assert_is(image_detail_matcher.source, source)
    vampytest.assert_eq(image_detail_matcher.name, name)
    vampytest.assert_is(image_detail_matcher.target, target)


def test__ImageDetailMatcherCustom__repr():
    """
    Tests whether ``ImageDetailMatcherCustom.__repr__`` works as intended.
    """
    action_tag = 'fluff'
    source = CHEN
    name = 'chen-ran'
    target = YAKUMO_RAN
    
    image_detail_matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    
    output = repr(image_detail_matcher)
    vampytest.assert_instance(output, str)


def test__ImageDetailMatcherCustom__hash():
    """
    Tests whether ``ImageDetailMatcherCustom.__hash__`` works as intended.
    """
    action_tag = 'fluff'
    source = CHEN
    name = 'chen-ran'
    target = YAKUMO_RAN
    
    image_detail_matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    
    output = hash(image_detail_matcher)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    action_tag = 'fluff'
    source = CHEN
    name = 'chen-ran'
    target = YAKUMO_RAN
    
    yield (
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        True,
    )
    
    yield (
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        {
            'action_tag': None,
            'source': source,
            'name': name,
            'target': target,
        },
        False,
    )
    
    yield (
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        {
            'action_tag': action_tag,
            'source': None,
            'name': name,
            'target': target,
        },
        False,
    )
    
    yield (
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        {
            'action_tag': action_tag,
            'source': source,
            'name': None,
            'target': target,
        },
        False,
    )
    
    yield (
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': target,
        },
        {
            'action_tag': action_tag,
            'source': source,
            'name': name,
            'target': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ImageDetailMatcherCustom__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageDetailMatcherCustom.__eq__`` works as intended.
    
    Case: Same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<object, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    image_detail_matcher_0 = ImageDetailMatcherCustom(**keyword_parameters_0)
    image_detail_matcher_1 = ImageDetailMatcherCustom(**keyword_parameters_1)
    
    output = image_detail_matcher_0 == image_detail_matcher_1
    vampytest.assert_instance(output, bool)
    return output


def test__ImageDetailMatcherCustom__eq__different_type():
    """
    Tests whether ``ImageDetailMatcherCustom`` works as intended.
    
    Case: Different type.
    """
    action_tag = 'fluff'
    source = CHEN
    name = 'chen-ran'
    target = YAKUMO_RAN
    
    image_detail_matcher = ImageDetailMatcherCustom(action_tag, source, target, name)
    
    output = image_detail_matcher == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def _iter_options__get_match_rate():
    image_detail = ImageDetailStatic('https://www.orindance.party/chen-ran-yukari-kick-lick-0000.png')
    image_detail.with_actions(
        ImageDetailAction('kiss', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    yield (
        {
            'action_tag': None,
            'source': None,
            'name': None,
            'target': None,
            
        },
        image_detail,
        1,
    )
    
    yield (
        {
            'action_tag': 'fluff',
            'source': None,
            'name': None,
            'target': None,
            
        },
        image_detail,
        0,
    )
    
    yield (
        {
            'action_tag': 'kiss',
            'source': YAKUMO_RAN,
            'name': 'chen-ran',
            'target': YAKUMO_YUKARI,
            
        },
        image_detail,
        1,
    )
    
    yield (
        {
            'action_tag': 'kiss',
            'source': YAKUMO_RAN,
            'name': None,
            'target': YAKUMO_YUKARI,
            
        },
        image_detail,
        1,
    )
    
    yield (
        {
            'action_tag': 'kiss',
            'source': YAKUMO_RAN,
            'name': 'chen-ran',
            'target': YAKUMO_YUKARI,
            
        },
        image_detail,
        1,
    )
    
    yield (
        {
            'action_tag': 'kiss',
            'source': YAKUMO_RAN,
            'name': 'miau',
            'target': YAKUMO_YUKARI,
            
        },
        image_detail,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate()).returning_last())
def test__ImageDetailMatcherCustom__get_match_rate(keyword_parameters, image_detail):
    """
    Tests whether ``ImageDetailMatcherCustom.get_match_rate`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    image_detail : ``ImageDetailCustom``
        The image detail to match.
    
    Returns
    -------
    output : `int`
    """
    image_detail_matcher = ImageDetailMatcherCustom(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate(image_detail)
    vampytest.assert_instance(output, int)
    return output



def _iter_options__get_match_rate_action():
    image_detail_action_0 = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    yield (
        {
            'action_tag': None,
            'source': None,
            'name': None,
            'target': None,
            
        },
        image_detail_action_0,
        1,
    )
    
    yield (
        {
            'action_tag': 'kiss',
            'source': None,
            'name': None,
            'target': None,
            
        },
        image_detail_action_0,
        1,
    )
    
    yield (
        {
            'action_tag': 'lick',
            'source': None,
            'name': None,
            'target': None,
            
        },
        image_detail_action_0,
        0,
    )
    
    yield (
        {
            'action_tag': None,
            'source': YAKUMO_RAN,
            'name': None,
            'target': None,
            
        },
        image_detail_action_0,
        1,
    )
    
    yield (
        {
            'action_tag': None,
            'source': CHEN,
            'name': None,
            'target': None,
            
        },
        image_detail_action_0,
        0,
    )
    
    yield (
        {
            'action_tag': None,
            'source': None,
            'name': None,
            'target': YAKUMO_YUKARI,
            
        },
        image_detail_action_0,
        1,
    )
    
    yield (
        {
            'action_tag': None,
            'source': None,
            'name': None,
            'target': CHEN,
            
        },
        image_detail_action_0,
        0,
    )
    
    # Name does not affects this function.
    yield (
        {
            'action_tag': None,
            'source': None,
            'name': 'hey-mister',
            'target': None,
            
        },
        image_detail_action_0,
        1,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate_action()).returning_last())
def test__ImageDetailMatcherCustom__get_match_rate_action(keyword_parameters, image_detail_action):
    """
    Tests whether ``ImageDetailMatcherCustom.get_match_rate_action`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    image_detail_action : ``ImageDetailAction``
        The image detail action to match.
    
    Returns
    -------
    output : `int`
    """
    image_detail_matcher = ImageDetailMatcherCustom(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate_action(image_detail_action)
    vampytest.assert_instance(output, int)
    return output
