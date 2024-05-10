import vampytest

from ....touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ...image_detail import ImageDetailAction, ImageDetailStatic

from ..constants import WEIGHT_DIRECT_MATCH, WEIGHT_NONE_MATCH
from ..context_sensitive import ImageDetailMatcherContextSensitive


def _assert_fields_set(image_detail_matcher):
    """
    Asserts whether every fields are set of teh given image detail matcher.
    
    Parameters
    ----------
    image_detail_matcher : ``ImageDetailMatcherContextSensitive``
        The image detail matcher to assert.
    """
    vampytest.assert_instance(image_detail_matcher, ImageDetailMatcherContextSensitive)
    vampytest.assert_instance(image_detail_matcher.sources, set, nullable = True)
    vampytest.assert_instance(image_detail_matcher.targets, set, nullable = True)


def test__ImageDetailMatcherContextSensitive__new():
    """
    Tests whether ``ImageDetailMatcherContextSensitive.__new__`` works as intended.
    """
    sources = {CHEN.system_name}
    targets = {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name}
    
    image_detail_matcher = ImageDetailMatcherContextSensitive(sources, targets)
    _assert_fields_set(image_detail_matcher)
    
    vampytest.assert_eq(image_detail_matcher.sources, sources)
    vampytest.assert_eq(image_detail_matcher.targets, targets)


def test__ImageDetailMatcherContextSensitive__repr():
    """
    Tests whether ``ImageDetailMatcherContextSensitive.__repr__`` works as intended.
    """
    sources = {CHEN.system_name}
    targets = {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name}
    
    image_detail_matcher = ImageDetailMatcherContextSensitive(sources, targets)
    
    output = repr(image_detail_matcher)
    vampytest.assert_instance(output, str)


def test__ImageDetailMatcherContextSensitive__hash():
    """
    Tests whether ``ImageDetailMatcherContextSensitive.__hash__`` works as intended.
    """
    sources = {CHEN.system_name}
    targets = {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name}
    
    image_detail_matcher = ImageDetailMatcherContextSensitive(sources, targets)
    
    output = hash(image_detail_matcher)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    sources = {CHEN.system_name}
    targets = {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name}
    
    yield (
        {
            'sources': sources,
            'targets': targets,
        },
        {
            'sources': sources,
            'targets': targets,
        },
        True,
    )
    
    yield (
        {
            'sources': sources,
            'targets': targets,
        },
        {
            'sources': None,
            'targets': targets,
        },
        False,
    )
    
    yield (
        {
            'sources': sources,
            'targets': targets,
        },
        {
            'sources': sources,
            'targets': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ImageDetailMatcherContextSensitive__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ImageDetailMatcherContextSensitive.__eq__`` works as intended.
    
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
    image_detail_matcher_0 = ImageDetailMatcherContextSensitive(**keyword_parameters_0)
    image_detail_matcher_1 = ImageDetailMatcherContextSensitive(**keyword_parameters_1)
    
    output = image_detail_matcher_0 == image_detail_matcher_1
    vampytest.assert_instance(output, bool)
    return output


def test__ImageDetailMatcherContextSensitive__eq__different_type():
    """
    Tests whether ``ImageDetailMatcherContextSensitive`` works as intended.
    
    Case: Different type.
    """
    sources = {CHEN.system_name}
    targets = {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name}
    
    image_detail_matcher = ImageDetailMatcherContextSensitive(sources, targets)
    
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
        {
            'sources': {CHEN.system_name},
            'targets': {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name},
        },
        image_detail,
        WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH,
    )
    
    yield (
        {
            'sources': {CHEN.system_name},
            'targets': {YAKUMO_RAN.system_name},
        },
        image_detail,
        WEIGHT_DIRECT_MATCH + 0,
    )
    
    yield (
        {
            'sources': {YAKUMO_YUKARI.system_name},
            'targets': {CHEN.system_name},
        },
        image_detail,
        0 + 0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate()).returning_last())
def test__ImageDetailMatcherContextSensitive__get_match_rate(keyword_parameters, image_detail):
    """
    Tests whether ``ImageDetailMatcherContextSensitive.get_match_rate`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    image_detail : ``ImageDetailContextSensitive``
        The image detail to match.
    
    Returns
    -------
    output : `bool`
    """
    image_detail_matcher = ImageDetailMatcherContextSensitive(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate(image_detail)
    vampytest.assert_instance(output, int)
    return output



def _iter_options__get_match_rate_action():
    image_detail_action_0 = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    image_detail_action_1 = ImageDetailAction('kiss', YAKUMO_RAN, None)
    
    yield (
        {
            'sources': {CHEN.system_name},
            'targets': {YAKUMO_RAN.system_name, YAKUMO_YUKARI.system_name},
        },
        image_detail_action_0,
        0 + WEIGHT_DIRECT_MATCH,
    )
    
    yield (
        {
            'sources': {YAKUMO_RAN.system_name},
            'targets': {YAKUMO_YUKARI.system_name},
        },
        image_detail_action_0,
        WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH,
    )
    
    yield (
        {
            'sources': None,
            'targets': None,
        },
        image_detail_action_0,
        0 + 0,
    )
    
    yield (
        {
            'sources': None,
            'targets': None,
        },
        image_detail_action_1,
        0 + WEIGHT_NONE_MATCH,
    )
    
    yield (
        {
            'sources': {YAKUMO_RAN.system_name},
            'targets': None,
        },
        image_detail_action_1,
        WEIGHT_DIRECT_MATCH + WEIGHT_NONE_MATCH,
    )


@vampytest._(vampytest.call_from(_iter_options__get_match_rate_action()).returning_last())
def test__ImageDetailMatcherContextSensitive__get_match_rate_action(keyword_parameters, image_detail_action):
    """
    Tests whether ``ImageDetailMatcherContextSensitive.get_match_rate_action`` works as intended.
    
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
    image_detail_matcher = ImageDetailMatcherContextSensitive(**keyword_parameters)
    
    output = image_detail_matcher.get_match_rate_action(image_detail_action)
    vampytest.assert_instance(output, int)
    return output
