__all__ = ()

from re import compile as re_compile


CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_BUILDER = lambda user_id: f'user.burn_divorce_papers.{user_id:x}'

CUSTOM_ID_BURN_DIVORCE_PAPERS_CONFIRMATION_RP = re_compile('user\\.burn_divorce_papers\\.([0-9a-f]+)')
