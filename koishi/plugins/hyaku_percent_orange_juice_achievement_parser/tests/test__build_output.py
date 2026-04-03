import vampytest

from ..constants import ACHIEVEMENTS
from ..logic import build_output


def _iter_options():
    user_owned_achievements = {
        'Pudding Chaser',
        'Hyper',
        'A Little Aviator',
    }
    
    yes_indexes = (*(ACHIEVEMENTS.index(achievement_name) for achievement_name in user_owned_achievements),)
    
    yield (
        user_owned_achievements,
        '\n'.join(('Yes' if index in yes_indexes else 'No') for index in range(len(ACHIEVEMENTS))),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_output(user_owned_achievements):
    """
    Builds output file content.
    
    Parameters
    ----------
    user_owned_achievements : `set<str>`
        The achievements owned by the user.
    
    Returns
    -------
    output : `str`
    """
    output = build_output(user_owned_achievements)
    vampytest.assert_instance(output, str)
    return output
