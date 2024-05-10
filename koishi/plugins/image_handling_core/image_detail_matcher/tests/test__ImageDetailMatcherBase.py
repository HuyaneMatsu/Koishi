import vampytest

from ....touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ...image_detail import ImageDetailAction, ImageDetailStatic

from ..base import ImageDetailMatcherBase


def _assert_fields_set(image_detail_matcher):
    """
    Asserts whether every fields are set of teh given image detail matcher.
    
    Parameters
    ----------
    image_detail_matcher : ``ImageDetailMatcherBase``
        The image detail matcher to assert.
    """
    vampytest.assert_instance(image_detail_matcher, ImageDetailMatcherBase)


def test__ImageDetailMatcherBase__new():
    """
    Tests whether ``ImageDetailMatcherBase.__new__`` works as intended.
    """
    image_detail_matcher = ImageDetailMatcherBase()
    _assert_fields_set(image_detail_matcher)


def test__ImageDetailMatcherBase__repr():
    """
    Tests whether ``ImageDetailMatcherBase.__repr__`` works as intended.
    """
    image_detail_matcher = ImageDetailMatcherBase()
    
    output = repr(image_detail_matcher)
    vampytest.assert_instance(output, str)


def test__ImageDetailMatcherBase__hash():
    """
    Tests whether ``ImageDetailMatcherBase.__hash__`` works as intended.
    """
    image_detail_matcher = ImageDetailMatcherBase()
    
    output = hash(image_detail_matcher)
    vampytest.assert_instance(output, int)



def _iter_options__eq__same_type():
    yield (
        {},
        {},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ImageDetailMatcherBase__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageDetailMatcherBase.__eq__`` works as intended.
    
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
    image_detail_matcher_0 = ImageDetailMatcherBase(**keyword_parameters_0)
    image_detail_matcher_1 = ImageDetailMatcherBase(**keyword_parameters_1)
    
    output = image_detail_matcher_0 == image_detail_matcher_1
    vampytest.assert_instance(output, bool)
    return output


def test__ImageDetailMatcherBase__eq__different_type():
    """
    Tests whether ``ImageDetailMatcherBase`` works as intended.
    
    Case: Different type.
    """
    image_detail_matcher = ImageDetailMatcherBase()
    
    output = image_detail_matcher == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def _iter_options__get_match_rate():
    image_detail = ImageDetailStatic('https://www.orindance.party/')
    image_detail.with_actions(
        ImageDetailAction('kiss', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    yield (
        {},
        image_detail,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate()).returning_last())
def test__ImageDetailMatcherBase__get_match_rate(keyword_parameters, image_detail):
    """
    Tests whether ``ImageDetailMatcherBase.get_match_rate`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    image_detail : ``ImageDetailBase``
        The image detail to match.
    
    Returns
    -------
    output : `bool`
    """
    image_detail_matcher = ImageDetailMatcherBase(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate(image_detail)
    vampytest.assert_instance(output, int)
    return output



def _iter_options__get_match_rate_action():
    image_detail_action = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    yield (
        {},
        image_detail_action,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate_action()).returning_last())
def test__ImageDetailMatcherBase__get_match_rate_action(keyword_parameters, image_detail_action):
    """
    Tests whether ``ImageDetailMatcherBase.get_match_rate_action`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    image_detail_action : ``ImageDetailAction``
        The image detail action to match.
    
    Returns
    -------
    output : `bool`
    """
    image_detail_matcher = ImageDetailMatcherBase(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate_action(image_detail_action)
    vampytest.assert_instance(output, int)
    return output
