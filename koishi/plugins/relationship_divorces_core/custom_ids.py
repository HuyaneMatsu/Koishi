__all__ = ('CUSTOM_ID_BURN_DIVORCE_PAPERS_INVOKE_RP',)

from re import compile as re_compile


# invoke
CUSTOM_ID_BURN_DIVORCE_PAPERS_BUILDER = (
    lambda user_id: f'user.burn_divorce_papers.invoke.{user_id:x}'
)
CUSTOM_ID_BURN_DIVORCE_PAPERS_INVOKE_RP = re_compile(
    f'user\\.burn_divorce_papers\\.invoke\\.([0-9a-f]+)'
)
