from kivy.base import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
from kivymd.uix.tooltip import MDTooltip, MDTooltipPlain
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, DictProperty, ColorProperty
from kivy.metrics import dp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

from .TrackerKivy import ImageLoader

from Gui import apname, UT_VERSION, __version__

from Generate import main as GMain, mystery_argparse

from collections import Counter, defaultdict

def get_ut_color(color: str)->str:
    from typing import ClassVar
    class UTTextColor(Widget):
        in_logic: ClassVar[str] = StringProperty("")
        glitched: ClassVar[str] = StringProperty("") 
        out_of_logic: ClassVar[str] = StringProperty("") 
        collected: ClassVar[str] = StringProperty("") 
        in_logic_glitched: ClassVar[str] = StringProperty("") 
        out_of_logic_glitched: ClassVar[str] = StringProperty("") 
        mixed_logic: ClassVar[str] = StringProperty("") 
        collected_light: ClassVar[str] = StringProperty("") 
        hinted: ClassVar[str] = StringProperty("") 
        hinted_in_logic: ClassVar[str] = StringProperty("") 
        hinted_out_of_logic: ClassVar[str] = StringProperty("") 
        hinted_glitched: ClassVar[str] = StringProperty("") 
        excluded: ClassVar[str] = StringProperty("")
        unconnected: ClassVar[str] = StringProperty("") 
    if not hasattr(get_ut_color,"utTextColor"):
        get_ut_color.utTextColor = UTTextColor()
    return str(getattr(get_ut_color.utTextColor,color,"DD00FF"))
    
class TrackerScreen(MDScreen):
    pass

class TrackerLayout(BoxLayout):
    pass

class TrackerTooltip(MDTooltipPlain):
    pass

class TrackerView(MDRecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.data.append({"text": f"Tracker {UT_VERSION} Initializing for {apname} version {__version__}"})

    def resetData(self):
        self.data.clear()

    def addLine(self, line: str, sort: bool = False):
        self.data.append({"text": line})
        if sort:
            self.data.sort(key=lambda e: e["text"])

class ApLocationIcon(FitImage):
    pass

class ApLocation(Widget, MDTooltip):
    locationDict = DictProperty()
    app: MDApp

    def __init__(self, sections, parent, **kwargs):
        self.app = MDApp.get_running_app()
        for location_id in sections:
            self.locationDict[location_id] = "none"
            self.tracker_page = parent
        self.bind(locationDict=self.update_color)
        super().__init__(**kwargs)
        self._tooltip = TrackerTooltip(text="Test")
        self._tooltip.markup = True
    
    def on_enter(self):
        self._tooltip.text = self.get_text()
        self.display_tooltip()

    def on_leave(self):
        self.animation_tooltip_dismiss()
    
    def transform_to_pop_coords(self,x,y):
        x2 = (x)
        y2 = (self.tracker_page.height - y)
        x3 = x2 - (self.tracker_page.x + (self.tracker_page.width - self.tracker_page.norm_image_size[0])/2)
        y3 = y2 + (self.tracker_page.y - (self.tracker_page.height - self.tracker_page.norm_image_size[1])/2)
        x4 = x3 / ((self.tracker_page.norm_image_size[0] / self.tracker_page.texture_size[0]) if self.tracker_page.texture_size[0] > 0 else 1)
        y4 = y3 / ((self.tracker_page.norm_image_size[1] / self.tracker_page.texture_size[1]) if self.tracker_page.texture_size[0] > 0 else 1)
        x5 = x4 + self.width/2
        y5 = y4 + self.width/2
        return (x5,y5)
    
    def on_mouse_pos(self, window, pos): #this does nothing, but it's kept here to make adding debug prints easier
        return super().on_mouse_pos(window, pos)

    def to_window(self, x, y):
        if self.border_point:
            return self.border_point
        else:
            return self.tracker_page.to_window(x,y)
    
    def to_widget(self, x, y):
        return self.transform_to_pop_coords(*self.tracker_page.to_widget(x,y))

    def update_status(self, location, status):
        if location in self.locationDict:
            if self.locationDict[location] != status:
                self.locationDict[location] = status
    
    def get_text(self):
        ctx = self.app.ctx
        
        location_id_to_name = ctx.location_names[ctx.game]
        sReturn = []
        for loc,status in self.locationDict.items():
            color = get_ut_color("collected_light")
            if status in ["in_logic","out_of_logic","glitched","hinted_in_logic","hinted_out_of_logic","hinted_glitched"]:
                color = get_ut_color(status)
            sReturn.append(f"{location_id_to_name[loc]} : [color={color}]{status}[/color]") 
        return "\n".join(sReturn)

    def update_color(self, locationDict):
        return
    
class ApLocationDeferred(ApLocation):
    color = ColorProperty("#"+get_ut_color("error"))
    app: MDApp
    def __init__(self, sections, parent, entrance, **kwargs):
        super().__init__(sections, parent, **kwargs)
        self.entrance = entrance
        self.app = MDApp.get_running_app()

    @staticmethod
    def update_color(self, entranceDict):
        passable = any(status == "passable" for status in entranceDict.values())
        impassable = any(status == "impassable" for status in entranceDict.values())
        if passable:
            self.color = "#"+get_ut_color("in_logic")
        elif impassable:
            self.color = "#"+get_ut_color("out_of_logic")
        else:
            self.color = "#"+get_ut_color("collected")
    
    def get_text(self):
        ctx = self.app.ctx
        host_world = ctx.tracker_core.get_current_world()
        sReturn = []
        for entrance, status in self.locationDict.items():
            color = get_ut_color("out_of_logic")
            if status == "passed":
                color = get_ut_color("collected_light")
            elif status == "passable":
                color = get_ut_color("in_logic")
            poptracker_entrance_mapping: dict[str, str] | None = ctx.tracker_world.poptracker_entrance_mapping
            if poptracker_entrance_mapping:
                try:
                    entrance_name = next(key for key in poptracker_entrance_mapping if poptracker_entrance_mapping[key] == entrance)
                except StopIteration:
                    entrance_name = entrance
            else:
                entrance_name = entrance
            sReturn.append(f"{entrance_name} : [color={color}]{status}[/color]")
            if host_world:
                if self.entrance:
                    real_entrance = host_world.get_entrance(entrance)
                    if real_entrance.connected_region:
                        sReturn.append(f" - connects to ({real_entrance.connected_region.name})")
        return "\n".join(sReturn)
   
class APLocationMixed(ApLocation):
    color = ColorProperty("#"+get_ut_color("error"))

    def __init__(self, sections, parent, **kwargs):
        super().__init__(sections, parent, **kwargs)

    @staticmethod
    def update_color(self, locationDict):
        glitches = any(status.endswith("glitched") for status in locationDict.values())
        in_logic = any(status.endswith("in_logic") for status in locationDict.values())
        out_of_logic = any(status.endswith("out_of_logic") for status in locationDict.values())
        hinted = any(status.startswith("hinted") for status in locationDict.values())

        if in_logic and (out_of_logic or (glitches and hinted)):
            self.color = "#"+get_ut_color("mixed_logic")
        elif glitches and hinted:
            self.color = "#"+get_ut_color("hinted_glitched")
        elif hinted and out_of_logic:
            self.color = "#"+get_ut_color("hinted_out_of_logic")
        elif hinted:
            self.color = "#"+get_ut_color("hinted")
        elif glitches and in_logic:
            self.color = "#"+get_ut_color("in_logic_glitched")
        elif glitches and out_of_logic:
            self.color = "#"+get_ut_color("out_of_logic_glitched")
        elif in_logic:
            self.color = "#"+get_ut_color("in_logic")
        elif out_of_logic:
            self.color = "#"+get_ut_color("out_of_logic")
        elif glitches:
            self.color = "#"+get_ut_color("glitched")
        else:
            self.color = "#"+get_ut_color("collected")

class APLocationSplit(ApLocation):
    color_1 = ColorProperty("#"+get_ut_color("error"))
    color_2 = ColorProperty("#"+get_ut_color("error"))
    color_3 = ColorProperty("#"+get_ut_color("error"))
    color_4 = ColorProperty("#"+get_ut_color("error"))
    def __init__(self, sections, parent, **kwargs):
        super().__init__(sections, parent, **kwargs)

    @staticmethod
    def update_color(self, locationDict):
        #glitches = any(status.endswith("glitched") for status in locationDict.values())

        color_list = Counter()
        def sort_status(pair) -> float:
            if pair[0] == "out_of_logic": return 0
            if pair[0] == "in_logic": return 999999999
            if pair[0] == "hinted_in_logic": return 8888888
            return pair[1] + (ord(pair[0][0])/10)

        for status in locationDict.values():
            if status == "collected": #ignore collected
                continue
            color_list[status] += 1

        color_list = [k for k,v in sorted(color_list.items(),key=sort_status,reverse=True)]
        if color_list:
            color_list = (color_list * max(2, (4 // len(color_list))))[:4]
            self.color_1="#"+get_ut_color(color_list[0])
            self.color_2="#"+get_ut_color(color_list[1])
            self.color_3="#"+get_ut_color(color_list[2])
            self.color_4="#"+get_ut_color(color_list[3])
        else:
            self.color_1="#"+get_ut_color("collected")
            self.color_2="#"+get_ut_color("collected")
            self.color_3="#"+get_ut_color("collected")
            self.color_4="#"+get_ut_color("collected")

class VisualTracker(BoxLayout):
    location_icon: ApLocationIcon
    def load_coords(self,  coords: dict[tuple,list[int]], defered_coords: dict[tuple, list[str]],
                        ldefered_coords: dict[tuple, list[str]], use_split) -> tuple[dict[int,list], dict[str,list], dict[str,list]]:
        self.ids.location_canvas.clear_widgets()
        returnDict: dict[int,list] = defaultdict(list)
        deferredDict: dict[str,list] = defaultdict(list)
        ldeferredDict: dict[str,list] = defaultdict(list)
        for coord, sections in coords.items():
            # https://discord.com/channels/731205301247803413/1170094879142051912/1272327822630977727
            ap_location_class = APLocationSplit if use_split else APLocationMixed
            temp_loc = ap_location_class(sections, self.ids.tracker_map, pos=(coord))
            self.ids.location_canvas.add_widget(temp_loc)
            for location_id in sections:
                returnDict[location_id].append(temp_loc)
        for coord, sections in defered_coords.items():
            temp_loc = ApLocationDeferred(sections, self.ids.tracker_map, True, pos=(coord))
            self.ids.location_canvas.add_widget(temp_loc)
            for entrance_name in sections:
                deferredDict[entrance_name].append(temp_loc)
        for coord, sections in ldefered_coords.items():
            temp_loc = ApLocationDeferred(sections, self.ids.tracker_map, False, pos=(coord))
            self.ids.location_canvas.add_widget(temp_loc)
            for event_name in sections:
                ldeferredDict[event_name].append(temp_loc)
        self.ids.location_canvas.add_widget(self.location_icon)
        return returnDict, deferredDict, ldeferredDict
'''
This is adding an additional hint label to the hints tab for 'in logic'

Will add this via mwgg_gui.overrides.expansionlist.py
'''
# class TrackerHintLabel():
#     logic_text = StringProperty("")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.app = MDApp.get_running_app()
#         logic = TrackerTooltip(
#             sort_key="finding",  # is lying to computer and player but fixing it will need core changes
#             text="", halign='center', valign='center', pos_hint={"center_y": 0.5},
#             )
#         self.add_widget(logic)

#         def set_text(_, value):
#             logic.text = value
#         self.bind(logic_text=set_text)

#     def refresh_view_attrs(self, rv, index, data):
#         super().refresh_view_attrs(rv, index, data)
#         if data["item"]["text"] == rv.header["item"]["text"]:
#             self.logic_text = "[u]In Logic[/u]"
#             return
#         ctx = self.app.ctx
#         if "status" in data:
#             loc = data["status"]["hint"]["location"]
#             from NetUtils import HintStatus
#             found = data["status"]["hint"]["status"] == HintStatus.HINT_FOUND
#         else:
#             prefix = len("[color=00FF7F]")
#             suffix = len("[/color]")
#             loc_name = data["location"]["text"][prefix:-1*suffix]
#             loc = ctx.location_names[ctx.game].get(loc_name)
#             found = "Not Found" not in data["found"]["text"]

#         in_logic = loc in ctx.tracker_core.locations_available
#         self.logic_text = rv.parser.handle_node({
#             "type": "color", "color": "green" if found else
#             "orange" if in_logic else "red",
#             "text": "Found" if found else "In Logic" if in_logic
#             else "Not Found"})

#     def kv_post(self, base_widget):
#         self.viewclass = TrackerHintLabel
#     .on_kv_post = kv_post

class TrackerScreen(MDScreen):
    tracker: TrackerLayout
    tracker_page: TrackerView
    source: StringProperty("")
    loc_size: NumericProperty(20)
    loc_icon_size: NumericProperty(20)
    loc_border: NumericProperty(5)
    enable_map: BooleanProperty(False)
    iconSource: StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

        self.tracker = TrackerLayout(orientation="vertical")
        tracker_view = TrackerView()

        # Creates a header
        tracker_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(36))
        tracker_divider = MDDivider(size_hint_y=None, height=dp(1))
        self.tracker_total_locs_label = MDLabel(text="Locations: 0/0", halign="center")
        self.tracker_logic_locs_label = MDLabel(text="In Logic: 0", halign="center")
        self.tracker_glitched_locs_label = MDLabel(text=f"Glitched: [color={get_ut_color('glitched')}]0[/color]",  halign="center")
        self.tracker_hinted_locs_label = MDLabel(text=f"Hinted: [color={get_ut_color('hinted_in_logic')}]0[/color]", halign="center")
        self.tracker_glitched_locs_label.markup = True
        self.tracker_hinted_locs_label.markup = True
        tracker_header.add_widget(self.tracker_total_locs_label)
        tracker_header.add_widget(self.tracker_logic_locs_label)
        tracker_header.add_widget(self.tracker_glitched_locs_label)
        tracker_header.add_widget(self.tracker_hinted_locs_label)

        # Adds the tracker list at the bottom
        self.tracker.add_widget(tracker_header)
        self.tracker.add_widget(tracker_divider)
        self.tracker.add_widget(tracker_view)

        self.tracker_page = tracker_view
        self.location_icon = ApLocationIcon()

        self.app.map_content = VisualTracker()
        self.app.map_content.location_icon = self.location_icon
        self.app.map_page_coords_func = self.app.map_content.load_coords
        if self.gen_error is not None:
            for line in self.gen_error.split("\n"):
                self.log_to_tab(line, False)

        @staticmethod
        def set_map_tab(value, *args, map_content=self.app.map_content, test=[]):
            if value:
                if not test:
                    test.append(self.app.create_custom_screen("Map", map_content))
            else:
                if test:
                    map_tab = test.pop()
                    map_tab.content.parent = None
                    self.app.screen_manager.remove_widget(map_tab)

        self.app.apply_property(show_map=BooleanProperty(True))
        self.app.fbind("show_map",set_map_tab)
        self.app.show_map = False

Builder.load_file("Tracker.kv")