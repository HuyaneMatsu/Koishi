import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_url_difference_into


def _iter_options__render_url_difference_into():
    url_0 = 'https://orindance.party/party'
    url_1 = 'https://orindance.party/dance'
    
    yield (
        url_0,
        Activity(activity_type = ActivityType.playing, url = url_1),
        f'Url: {url_0!r} -> {url_1!r}\n',
    )
    
    yield (
        url_0,
        Activity(activity_type = ActivityType.playing),
        f'Url: {url_0!r} -> null\n',
    )
    yield (
        None,
        Activity(activity_type = ActivityType.playing, url = url_1),
        f'Url: null -> {url_1!r}\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_url_difference_into()).returning_last())
def test__render_url_difference_into(old_value, activity):
    """
    Tests whether ``render_url_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | str`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_url_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
