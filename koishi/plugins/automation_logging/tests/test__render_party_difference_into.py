import vampytest
from hata import Activity, ActivityParty, ActivityType

from ..embed_builder_satori import render_party_difference_into


def _iter_options__render_party_difference_into():
    yield (
        None,
        Activity(activity_type = ActivityType.playing),
        '',
    )
    
    yield (
        ActivityParty(
            party_id = 'Murasa',
        ),
        Activity(activity_type = ActivityType.playing),
        'Party id: \'Murasa\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                party_id = 'Kogasa',
            ),
        ),
        'Party id: null -> \'Kogasa\'\n',
    )
    yield (
        ActivityParty(
            party_id = 'Murasa',
        ),
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                party_id = 'Kogasa',
            ),
        ),
        'Party id: \'Murasa\' -> \'Kogasa\'\n',
    )
    
    yield (
        ActivityParty(
            size = 1,
        ),
        Activity(activity_type = ActivityType.playing),
        'Party size: 1 -> 0\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                size = 2,
            ),
        ),
        'Party size: 0 -> 2\n',
    )
    yield (
        ActivityParty(
            size = 1,
        ),
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                size = 2,
            ),
        ),
        'Party size: 1 -> 2\n',
    )
    
    yield (
        ActivityParty(
            max_ = 3,
        ),
        Activity(activity_type = ActivityType.playing),
        'Party max: 3 -> 0\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                max_ = 4,
            ),
        ),
        'Party max: 0 -> 4\n',
    )
    yield (
        ActivityParty(
            max_ = 3,
        ),
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                max_ = 4,
            ),
        ),
        'Party max: 3 -> 4\n',
    )
    
    yield (
        ActivityParty(
            party_id = 'Murasa',
            size = 1,
            max_ = 3,
        ),
        Activity(
            activity_type = ActivityType.playing,
            party = ActivityParty(
                party_id = 'Kogasa',
                size = 2,
                max_ = 4,
            ),
        ),
        (
            'Party id: \'Murasa\' -> \'Kogasa\'\n'
            'Party size: 1 -> 2\n'
            'Party max: 3 -> 4\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__render_party_difference_into()).returning_last())
def test__render_party_difference_into(old_value, activity):
    """
    Tests whether ``render_party_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | ActivityParty`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_party_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
