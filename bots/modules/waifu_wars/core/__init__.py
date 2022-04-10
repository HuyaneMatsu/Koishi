from hata.ext.extension_loader import import_extension

constants = import_extension('.constants')
waifu_type = import_extension('.waifu_type')


from hata import bind,  ClientUserBase


bind(ClientUserBase, waifu_type.WaifuType, 'waifu_stats')
