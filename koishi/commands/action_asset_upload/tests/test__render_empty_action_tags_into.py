import vampytest

from ..rendering import _render_empty_action_tags_into


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
def test__render_empty_action_tags_into(action_tags):
    """
    Tests whether ``_render_empty_action_tags_into`` works as intended.
    
    Parameters
    ----------
    action_tags : `None | set<str>`
        Action tags to render.
    
    Returns
    -------
    output : `str`
    """
    into = _render_empty_action_tags_into([], action_tags)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
