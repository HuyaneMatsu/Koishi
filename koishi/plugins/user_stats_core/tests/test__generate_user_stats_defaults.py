import vampytest

from ..helpers import generate_user_stats_defaults


def test__generate_user_stats_defaults():
    """
    Tests whether ``generate_user_stats_defaults`` works as intended.
    """
    user_id = 909883978717204561
    output = [*generate_user_stats_defaults(user_id)]
    vampytest.assert_eq(output, [3, 9, 3, 4, 9])
