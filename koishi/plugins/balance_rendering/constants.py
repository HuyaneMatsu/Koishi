from hata import AnsiForegroundColor, create_ansi_format_code

COLOR_CODE_RED = create_ansi_format_code(foreground_color = AnsiForegroundColor.red)
COLOR_CODE_GREEN = create_ansi_format_code(foreground_color = AnsiForegroundColor.green)
COLOR_CODE_RESET = create_ansi_format_code()
