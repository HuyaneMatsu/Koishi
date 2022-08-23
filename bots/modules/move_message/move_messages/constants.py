__all__ = ()

from hata import Emoji


MESSAGE_MOVER_CONTEXT_TIMEOUT = 600.0

MESSAGE_MOVER_CONTEXTS = {}


CUSTOM_ID_MESSAGE_MOVER_SUBMIT = 'message_mover.submit'
CUSTOM_ID_MESSAGE_MOVER_CANCEL = 'message_mover.cancel'
CUSTOM_ID_MESSAGE_MOVER_CLOSE = 'message_mover.close'
CUSTOM_ID_MESSAGE_MOVER_ADD_BY_ID = 'message_mover.add_by_id'


MESSAGE_MOVER_SUBMITTING_EMOJI = Emoji.precreate(704393708467912875)
