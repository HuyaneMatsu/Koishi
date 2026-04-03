import vampytest
from hata import Activity, ActivityType, Emoji

from ..embed_builder_satori import render_emoji_difference_into


def _iter_options__render_emoji_difference_into():
    emoji_0 = Emoji.precreate(202410140004, name = 'Keine')
    emoji_1 = Emoji.precreate(202410140005, name = 'Mokou')
    
    yield (
        emoji_0,
        Activity(activity_type = ActivityType.custom, emoji = emoji_1),
        f'Emoji: {emoji_0.name} ({emoji_0.id}) -> {emoji_1.name} ({emoji_1.id})\n',
    )
    
    yield (
        emoji_0,
        Activity(activity_type = ActivityType.custom),
        f'Emoji: {emoji_0.name} ({emoji_0.id}) -> null\n',
    )
    yield (
        None,
        Activity(activity_type = ActivityType.custom, emoji = emoji_1),
        f'Emoji: null -> {emoji_1.name} ({emoji_1.id})\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_emoji_difference_into()).returning_last())
def test__render_emoji_difference_into(old_value, activity):
    """
    Tests whether ``render_emoji_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : ``None | Emoji``
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_emoji_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
