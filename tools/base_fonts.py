from __future__ import annotations
__all__ = ("RegisterFonts",)

import os
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.metrics import sp


def RegisterFonts(app: MDApp, monospace_font: str = 'Argon'):
    LabelBase.register('Inter',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Bold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-BoldItalic.ttf"))
    LabelBase.register('Neon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Argon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Xenon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Radon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Krypton',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-ExtraBoldItalic.ttf"))
    LabelBase.register('GothicA1',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","GothicA1-Regular.ttf"),
                        None,
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","GothicA1-Bold.ttf"),
                        None)
    LabelBase.register('Mincho',
                       os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Mincho-Regular.ttf"),
                       )
    LabelBase.register('LibreFranklin',
                       os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","LibreFranklin-ExtraBold.ttf"),
                       )
    LabelBase.register('Icons',
                       fn_regular=os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","materialdesignicons-fa-webfont.ttf"),
                       )
    app.theme_cls.font_styles = {
        "Icon": {
            "large": {
                "line-height": 1,
                "font-name": "Icons",
                "font-size": sp(24),
            },
        },
        "Display": {
            "large": {
                "line-height": 1.64,
                "font-name": "GothicA1",
                "font-size": sp(57),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "GothicA1",
                "font-size": sp(45),
            },
            "small": {
                "line-height": 1.40,
                "font-name": "GothicA1",
                "font-size": sp(36),
            },
        },
        "Headline": {
            "large": {
                "line-height": 1.40,
                "font-name": "GothicA1",
                "font-size": sp(32),
            },
            "medium": {
                "line-height": 1.36,
                "font-name": "GothicA1",
                "font-size": sp(28),
            },
            "small": {
                "line-height": 1.32,
                "font-name": "GothicA1",
                "font-size": sp(24),
            },
        },
        "Title": {
            "large": {
                "line-height": 1.28,
                "font-name": "GothicA1",
                "font-size": sp(22),
            },
            "medium": {
                "line-height": 1.24,
                "font-name": "GothicA1",
                "font-size": sp(16),
            },
            "small": {
                "line-height": 1.20,
                "font-name": "GothicA1",
                "font-size": sp(14),
            },
        },
        "Body": {
            "large": {
                "line-height": 1.24,
                "font-name": "Inter",
                "font-size": sp(16),
            },
            "medium": {
                "line-height": 1.20,
                "font-name": "Inter",
                "font-size": sp(14),
            },
            "small": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(12),
            },
        },
        "Label": {
            "large": {
                "line-height": 1.20,
                "font-name": "Inter",
                "font-size": sp(14),
            },
            "medium": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(12),
            },
            "small": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(11),
            },
        },
        "TitleBar": {
            "large": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(20),
            },
            "medium": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(19),
            },
            "small": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(18),
            },
        },
        "Monospace": {
            "large": {
                "line-height": 2.4,
                "font-name": f"{monospace_font}",
                "font-size": sp(20),
            },
            "medium": {
                "line-height": 2.2,
                "font-name": f"{monospace_font}",
                "font-size": sp(16),
            },
            "small": {
                "line-height": 1.8,
                "font-name": f"{monospace_font}",
                "font-size": sp(12),
            },
        },
        "Monospace-SM": {
            "large": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(12),
            },
            "medium": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(10),
            },
            "small": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(8),
            },
        },
    }
