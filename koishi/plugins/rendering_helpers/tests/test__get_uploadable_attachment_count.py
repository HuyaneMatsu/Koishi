import vampytest
from hata import Attachment, Guild

from ..attachment_builders import _get_uploadable_attachment_count


def _iter_options():
    yield (
        None,
        (
            Attachment.precreate(202503060000, size = 7 * (1 << 20)),
        ),
        1,
    )
    
    yield (
        None,
        (
            Attachment.precreate(202503060001, size = 8 * (1 << 20)),
        ),
        0,
    )
    
    yield (
        None,
        (
            Attachment.precreate(202503060002, size = 3 * (1 << 20)),
            Attachment.precreate(202503060003, size = 3 * (1 << 20)),
            Attachment.precreate(202503060004, size = 3 * (1 << 20)),
        ),
        2,
    )
    
    yield (
        Guild.precreate(202503060005, boost_level = 0),
        (
            Attachment.precreate(202503060006, size = 8 * (1 << 20)),
        ),
        0,
    )
    
    yield (
        Guild.precreate(202503060007, boost_level = 1),
        (
            Attachment.precreate(202503060008, size = 8 * (1 << 20)),
        ),
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_uploadable_attachment_count(guild, attachments):
    """
    Tests whether ``_get_uploadable_attachment_count`` works as intended.
    
    Parameters
    ----------
    guild : `None | Guild`
        The respective guild where the message will be sent.
    
    attachments : `tuple<Attachment>`
        Attachments to determine count from.
    
    Returns
    -------
    output : `int`
    """
    output = _get_uploadable_attachment_count(guild, attachments)
    vampytest.assert_instance(output, int)
    return output
