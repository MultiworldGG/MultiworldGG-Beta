import os

application = os.environ.get("MACOS_APP", "MultiworldGG.app")

files = ['build/' + application]

symlinks = {'Applications': '/Applications'}

format = 'UDZO'
size = '750m'

icon = 'data/macos/MultiworldGG.icns'

window_rect = ((100, 100), (640, 320))
icon_locations = {
    application: (140, 140),
    'Applications': (500, 140)
}

# Generated together with the app icon by tools/build_macos_assets.swift.
background = 'data/macos/dmg-background.tiff'
default_view = 'icon-view'
include_icon_view_settings = True
arrange_by = None
grid_spacing = 80
scroll_position = (0, 0)
icon_size = 128
text_size = 16
label_pos = 'bottom'
show_icon_preview = False
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
