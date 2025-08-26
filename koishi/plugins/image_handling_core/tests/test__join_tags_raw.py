import vampytest

from ..helpers import join_tags_raw


def _iter_options():
    tags_required = frozenset((
        'touhou',
        'solo',
    ))
    
    tags_banned = frozenset((
        'smoking',
        'bikini',
    ))
    
    tags_requested = {
        (True, 'komeiji_koishi'),
        (False, 'komeiji_satori'),
    }
    
    yield (
        tags_required,
        tags_banned,
        tags_requested,
        '-komeiji_satori komeiji_koishi',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__join_tags_raw(tags_required, tags_banned, tags_requested):
    """
    Tests whether ``join_tags_raw`` works as intended.
    
    Parameters
    ----------
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    tags_requested : `set<(bool, str)>`
        The requested tags.
    
    Returns
    -------
    output : `str`
    """
    output = join_tags_raw(tags_required, tags_banned, tags_requested)
    vampytest.assert_instance(output, str)
    return output
