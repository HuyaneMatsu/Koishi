import vampytest
from hata import Attachment

from ..attachment_builders import _build_attachment_truncated_attachments


def test__build_attachment_truncated_attachments():
    """
    Tests whether ``_build_attachment_truncated_attachments`` works as intended.
    """
    attachment_0 = Attachment.precreate(202503060012_000000, name = 'sister.txt', size = 12)
    attachment_1 = Attachment.precreate(202503060013_000000, name = 'mister.txt', size = 13, title = 'miau')
    attachment_2 = Attachment.precreate(202503060014_000000, name = 'kisser.txt', size = 14)
    output = _build_attachment_truncated_attachments((attachment_0, attachment_1, attachment_2), 1)
    
    vampytest.assert_eq(
        output,
        (
            'attachments_truncated.txt',
            (
                'Attachments truncated from zip due to lack of upload limit:\n'
                '- miau.txt | size = 13 bytes\n'
                '- kisser.txt | size = 14 bytes'
            ),
        )
    )
