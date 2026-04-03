from .error_message_getter import *


__all__ = (
    *error_message_getter.__all__,
)


from ...bots import FEATURE_CLIENTS

from .error_message_getter import okuu_error_message_getter

# Set random error message getter
for client in FEATURE_CLIENTS:
    client.slasher.random_error_message_getter = okuu_error_message_getter
