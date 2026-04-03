import vampytest

from ..rendering import _produce_empty_action_tags


def _iter_options():
    yield (
        {'kiss'},
        (
            '.with_action(\n'
            '    ACTION_TAG_KISS, None, None,\n'
            ')'
        ),
    )
    
    yield (
        {'kiss', 'hug'},
        (
            '.with_actions(\n'
            '    (ACTION_TAG_HUG, None, None),\n'
            '    (ACTION_TAG_KISS, None, None),\n'
            ')'
        ),
    )
    
    yield (
        None,
        (
            ''
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_empty_action_tags(action_tags):
    """
    Tests whether ``_produce_empty_action_tags`` works as intended.
    
    Parameters
    ----------
    action_tags : `None | set<str>`
        Action tags to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_empty_action_tags(action_tags)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
