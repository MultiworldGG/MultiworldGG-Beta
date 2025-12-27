"""
Titlebar class - creates the root widget that will be added to
the titlebar.  Additionally creates helper functions to bind
to the mouse and window events to display the appropriate icon

There is a drop shadow effect applied, which is why the positions
of the labels are at .45 and .47 - it is currently centered and hardcoded.
WINDOWS ONLY
"""
from __future__ import annotations
__all__ = (
    "Titlebar",
    "TitleBarButton",
)
from kivy.core.window import Window

from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import HorizontalBlurEffect, VerticalBlurEffect
from kivymd.uix.button import MDIconButton 
from kivy.lang import Builder

archipelago_name = "multiworld.gg"    ## need to fix in the future

KV = '''
#:import os os
<TitleBarButton>:
    style: "standard"
    adaptive_size: True
    pos_hint: {"y": 0, "x": 0}
    draggable: False
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.primaryContainerColor \
                    if app.theme_cls.theme_style == "Light" \
                    else app.theme_cls.onPrimaryColor
    theme_text_color: "Custom"
    text_color: app.theme_cls.onPrimaryContainerColor


<Titlebar>:
    adaptive_height: True
    width: root.width
    orientation: 'horizontal'
    padding: [0,0,0,0]
    spacing: 0
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.primaryContainerColor \
                    if app.theme_cls.theme_style == "Light" \
                    else app.theme_cls.onPrimaryColor
    tblabel: tblabel
    
    Image:
        halign: "left"
        valign: "top"
        source: os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "titlebards.png")
        size: self.texture_size
        size_hint: None,None

    MDFloatLayout:
        id: tblabel
        size_hint: 1, 1
        pos_hint: {"center_x": .5, "center_y": .5}

        TitleBlur:
            id: titleblur
            pos_hint: {"center_x": .5, "center_y": .45}
            size_hint: 1, 1
            opacity: .5
            MDLabel:
                pos_hint: {"center_x": .5, "center_y": .45}
                id: tblabel_title
                text: app.base_title
                font_style: "TitleBar"
                role: "small"
                text_size: self.width, None
                outline_width: 2
                outline_color: app.theme_cls.shadowColor
                theme_text_color: "Custom"
                text_color: app.theme_cls.shadowColor
                opacity: .5

        MDLabel:
            pos_hint: {"center_x": .499, "center_y": .47}
            size_hint: 1, 1
            id: tblabeltext
            text: app.base_title
            font_style: "TitleBar"
            text_size: self.width, None
            role: "small"
            outline_width: 1
            outline_color: app.theme_cls.inverseOnSurfaceColor

'''

class TitleBlur(EffectWidget):
    effects = [VerticalBlurEffect(size=3), HorizontalBlurEffect(size=3)]

class TitleBarButton(MDIconButton):
    pass

class Titlebar(MDBoxLayout):
    ''' 
    Titlebar class, creates functions to bind to window events
    Windows only
    '''
    titleblur = ObjectProperty(None)
    tbmin: TitleBarButton
    tbmax: TitleBarButton
    tbrestore: TitleBarButton
    tbclose: TitleBarButton

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_buttons()

    def create_buttons(self):
        self.tbmin = TitleBarButton(
            icon = "window-minimize"
        )
        self.tbmin.bind(on_release=self.tb_min)
        self.add_widget(self.tbmin)
        self.tbrestore = TitleBarButton(
            icon = "window-restore"
        )
        self.tbrestore.bind(on_release=self.tb_res)
        self.tbmax = TitleBarButton(
            icon = "window-maximize"
        )
        self.tbmax.bind(on_release=self.tb_max)
        self.add_widget(self.tbmax)
        self.tbclose = TitleBarButton(
            icon = "close"
        )
        self.tbclose.bind(on_release=lambda x: MDApp.get_running_app().stop(x))
        self.add_widget(self.tbclose)

    def tb_max(self, instance):
        Window.maximize()

    def tb_onmax(self, instance):
        try:
            assert self.tbmax in self.children
            self.remove_widget(self.tbmax)
            self.add_widget(self.tbrestore)
            self.remove_widget(self.tbclose)
            self.add_widget(self.tbclose)
        except:
            return

    def tb_res(self, instance):
        Window.restore()

    def tb_onres(self, instance):
        try:
            assert self.tbrestore in self.children
            self.remove_widget(self.tbrestore)
            self.add_widget(self.tbmax)
            self.remove_widget(self.tbclose)
            self.add_widget(self.tbclose)
        except:
            return
        
    def tb_min(self, instance):
        Window.minimize()

Builder.load_string(KV)