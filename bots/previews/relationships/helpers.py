__all__ = ()

def get_multiplier(user_id_1, user_id_2):
    return 2.1 - (((user_id_1 & 0x1111111111111111111111) + (user_id_2 & 0x1111111111111111111111)) % 101 * 0.01)
