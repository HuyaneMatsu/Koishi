__all__ = ()

from decimal import Decimal

BET_MIN = 10

MULTIPLIERS = (*(Decimal(value) / 100 for value in (170, 240, 120, 50, 30, 10, 20, 150,)),)

ARROW_BLOCKS = tuple(
    (
        f'```\n'
        f'「{MULTIPLIERS[(7 + push) % 8]:.01f}」    「{MULTIPLIERS[(0 + push) % 8]:.01f}」    「{MULTIPLIERS[(1 + push) % 8]:.01f}」\n'
        f'\n'
        f'　　       　/|\\\n'
        f'「{MULTIPLIERS[(6 + push) % 8]:.01f}」   　/ | \\　   「{MULTIPLIERS[(2 + push) % 8]:.01f}」\n'
        f'　　        　|\n'
        f'\n'
        f'「{MULTIPLIERS[(5 + push) % 8]:.01f}」    「{MULTIPLIERS[(4 + push) % 8]:.01f}」    「{MULTIPLIERS[(3 + push) % 8]:.01f}」\n'
        f'```'
    ) for push in range(8)
)
