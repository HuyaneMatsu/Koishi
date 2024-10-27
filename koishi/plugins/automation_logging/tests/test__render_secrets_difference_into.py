import vampytest
from hata import Activity, ActivitySecrets, ActivityType

from ..embed_builder_satori import render_secrets_difference_into


def _iter_options__render_secrets_difference_into():
    yield (
        None,
        Activity(activity_type = ActivityType.playing),
        '',
    )
    
    yield (
        ActivitySecrets(
            join = 'Murasa',
        ),
        Activity(activity_type = ActivityType.playing),
        'Secrets join: \'Murasa\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                join = 'Kogasa',
            ),
        ),
        'Secrets join: null -> \'Kogasa\'\n',
    )
    yield (
        ActivitySecrets(
            join = 'Murasa',
        ),
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                join = 'Kogasa',
            ),
        ),
        'Secrets join: \'Murasa\' -> \'Kogasa\'\n',
    )
    
    yield (
        ActivitySecrets(
            spectate = 'Koishi',
        ),
        Activity(activity_type = ActivityType.playing),
        'Secrets spectate: \'Koishi\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                spectate = 'Satori',
            ),
        ),
        'Secrets spectate: null -> \'Satori\'\n',
    )
    yield (
        ActivitySecrets(
            spectate = 'Koishi',
        ),
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                spectate = 'Satori',
            ),
        ),
        'Secrets spectate: \'Koishi\' -> \'Satori\'\n',
    )
    
    yield (
        ActivitySecrets(
            match = 'Flandre',
        ),
        Activity(activity_type = ActivityType.playing),
        'Secrets match: \'Flandre\' -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                match = 'Remilia',
            ),
        ),
        'Secrets match: null -> \'Remilia\'\n',
    )
    yield (
        ActivitySecrets(
            match = 'Flandre',
        ),
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                match = 'Remilia',
            ),
        ),
        'Secrets match: \'Flandre\' -> \'Remilia\'\n',
    )
    
    yield (
        ActivitySecrets(
            join = 'Murasa',
            spectate = 'Koishi',
            match = 'Flandre',
        ),
        Activity(
            activity_type = ActivityType.playing,
            secrets = ActivitySecrets(
                join = 'Kogasa',
                spectate = 'Satori',
                match = 'Remilia',
            ),
        ),
        (
            'Secrets join: \'Murasa\' -> \'Kogasa\'\n'
            'Secrets spectate: \'Koishi\' -> \'Satori\'\n'
            'Secrets match: \'Flandre\' -> \'Remilia\'\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__render_secrets_difference_into()).returning_last())
def test__render_secrets_difference_into(old_value, activity):
    """
    Tests whether ``render_secrets_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | ActivitySecrets`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_secrets_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
