__all__ = ()

import re


DATE_CONNECTOR = ' - '
NAME_WITH_DATE_RP = re.compile(
    f'.*?{re.escape(DATE_CONNECTOR)}\\d{{4}}\\-\\d{{2}}\\-\\d{{2}} \\d{{2}}\\:\\d{{2}}\\:\\d{{2}}'
)
NAME_LENGTH_MAX = 80 - (19 + len(DATE_CONNECTOR))
