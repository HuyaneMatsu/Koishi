import vampytest
from hata import InteractionEvent, User

from ..rendering import render_hearts_short_description


def _iter_options():
    user_0 = User.precreate(202412030001)
    user_1 = User.precreate(202412030002)
    
    yield (
        InteractionEvent.precreate(
            202412030000,
            user = user_0,
        ),
        user_0,
        10,
        20,
        True,
        'claim your daily',
        'You are on a 20 day streak, and you are ready to claim your daily!',
    )
    
    yield (
        InteractionEvent.precreate(
            202412030003,
            user = user_0,
        ),
        user_0,
        10,
        20,
        False,
        'claim your daily',
        'You are on a 20 day streak, keep up the good work!',
    )
    
    yield (
        InteractionEvent.precreate(
            202412030004,
            user = user_0,
        ),
        user_0,
        10,
        0,
        True,
        'claim your daily',
        None,
    )
    
    yield (
        InteractionEvent.precreate(
            202412030005,
            user = user_0,
        ),
        user_0,
        0,
        20,
        True,
        'claim your daily',
        'You are on a 20 day streak, and you are ready to claim your daily!',
    )
    
    yield (
        InteractionEvent.precreate(
            202412030006,
            user = user_0,
        ),
        user_1,
        10,
        20,
        True,
        'claim your daily',
        'They are on a 20 day streak, hope they will keep up their good work.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_hearts_short_description(
    interaction_event, target_user, total, streak, ready_to_claim, ready_to_claim_string
):
    """
    Tests whether ``render_hearts_short_description`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    total : `int`
        The user's total hearts.
    
    streak : `int`
        The user's streak
    
    ready_to_claim : `bool`
        Whether daily is ready to claim.
    
    ready_to_claim_string : `str`
        String to use when the user is ready to claim its reward.
    
    Returns
    -------
    output : `None | str`
    """
    output = render_hearts_short_description(
        interaction_event, target_user, total, streak, ready_to_claim, ready_to_claim_string
    )
    vampytest.assert_instance(output, str, nullable = True)
    return output
