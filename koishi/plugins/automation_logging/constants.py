__all__ = ()

from hata import Color, Permission


COLOR_ADD = Color.from_rgb(2, 168, 77)
COLOR_UPDATE = Color.from_rgb(237, 206, 28)
COLOR_DELETE = Color.from_rgb(168, 49, 2)

COLOR_SATORI = Color.from_rgb(168, 2, 146)

IMAGE_URL_SATORI = 'https://cdn.discordapp.com/attachments/568837922288173058/1109762751963865200/satori-0015-edit-0000.png'


# We need embed links permission to add thumbnail & image
PERMISSIONS_EMBED_LINKS = Permission().update_by_keys(embed_links = True)

# We need attach files to send files (obviously)
PERMISSIONS_ATTACH_FILES = Permission().update_by_keys(attach_files = True)
