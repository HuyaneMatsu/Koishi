__all__ = ()

from hata import Attachment, InteractionForm, file_type_filter_create, FileTypeFilterGroup, create_label, create_attachment_input
from hata.ext.slash import P

from ..bots import FEATURE_CLIENTS
from ..bot_utils.constants import GUILD__SUPPORT


TEST_ATTACHMENT_CUSTOM_ID = 'test.attachment.typed.form'


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def test_attachment_typed(
    client,
    interaction_event,
    attachment : P(
        Attachment,
        'mrrr',
        file_type_filter = file_type_filter_create(
            groups = [FileTypeFilterGroup.image],
            individuals = ['mp4'],
        ),
    ),
):
    return repr(attachment)


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT)
async def test_attachment_typed_form(
    client,
    interaction_event,
):
    return InteractionForm(
        'hey', 
        components = [
            create_label(
                'hey ho',
                component = create_attachment_input(
                    file_type_filter = file_type_filter_create(
                        groups = [FileTypeFilterGroup.image],
                        individuals = ['mp4'],
                    ),
                    custom_id = 'attachment',
                ),
            )
        ],
        custom_id = TEST_ATTACHMENT_CUSTOM_ID,
    )


@FEATURE_CLIENTS.interactions(custom_id = TEST_ATTACHMENT_CUSTOM_ID, target = 'form')
async def handle_test_attachment_typed_form(
    client,
    interaction_event,
    *,
    attachment : 'attachment',
):
    return repr(attachment)
