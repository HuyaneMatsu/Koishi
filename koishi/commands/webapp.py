__all__ = ()

from hata.main import register


@register
def run_webapp():
    """
    Runs the webapp of Koishi.
    """
    from ..web import WEBAPP
    WEBAPP.run()
