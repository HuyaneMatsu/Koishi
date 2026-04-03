import vampytest
from hata import Activity, ActivityAssets, ActivityType

from ..embed_builder_satori import render_assets_difference_into


def _iter_options__render_assets_difference_into():
    yield (
        None,
        Activity(activity_type = ActivityType.playing),
        '',
    )
    
    yield (
        ActivityAssets(
            image_large = 'Murasa',
        ),
        Activity(activity_type = ActivityType.playing),
        'Assets image large: \'Murasa\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                image_large = 'Kogasa',
            ),
        ),
        'Assets image large: null -> \'Kogasa\'\n',
    )
    yield (
        ActivityAssets(
            image_large = 'Murasa',
        ),
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                image_large = 'Kogasa',
            ),
        ),
        'Assets image large: \'Murasa\' -> \'Kogasa\'\n',
    )
    
    yield (
        ActivityAssets(
            text_large = 'Koishi',
        ),
        Activity(activity_type = ActivityType.playing),
        'Assets text large: \'Koishi\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                text_large = 'Satori',
            ),
        ),
        'Assets text large: null -> \'Satori\'\n',
    )
    yield (
        ActivityAssets(
            text_large = 'Koishi',
        ),
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                text_large = 'Satori',
            ),
        ),
        'Assets text large: \'Koishi\' -> \'Satori\'\n',
    )
    
    yield (
        ActivityAssets(
            image_small = 'Flandre',
        ),
        Activity(activity_type = ActivityType.playing),
        'Assets image small: \'Flandre\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                image_small = 'Remilia',
            ),
        ),
        'Assets image small: null -> \'Remilia\'\n',
    )
    yield (
        ActivityAssets(
            image_small = 'Flandre',
        ),
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                image_small = 'Remilia',
            ),
        ),
        'Assets image small: \'Flandre\' -> \'Remilia\'\n',
    )
    
    yield (
        ActivityAssets(
            text_small = 'Orin',
        ),
        Activity(activity_type = ActivityType.playing),
        'Assets text small: \'Orin\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                text_small = 'Okuu',
            ),
        ),
        'Assets text small: null -> \'Okuu\'\n',
    )
    yield (
        ActivityAssets(
            text_small = 'Orin',
        ),
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                text_small = 'Okuu',
            ),
        ),
        'Assets text small: \'Orin\' -> \'Okuu\'\n',
    )
    
    yield (
        ActivityAssets(
            image_large = 'Murasa',
            text_large = 'Koishi',
            image_small = 'Flandre',
            text_small = 'Orin',
        ),
        Activity(
            activity_type = ActivityType.playing,
            assets = ActivityAssets(
                image_large = 'Kogasa',
                text_large = 'Satori',
                image_small = 'Remilia',
                text_small = 'Okuu',
            ),
        ),
        (
            'Assets image large: \'Murasa\' -> \'Kogasa\'\n'
            'Assets text large: \'Koishi\' -> \'Satori\'\n'
            'Assets image small: \'Flandre\' -> \'Remilia\'\n'
            'Assets text small: \'Orin\' -> \'Okuu\'\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__render_assets_difference_into()).returning_last())
def test__render_assets_difference_into(old_value, activity):
    """
    Tests whether ``render_assets_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | ActivityAssets`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_assets_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
