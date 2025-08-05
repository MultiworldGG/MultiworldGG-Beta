from __future__ import annotations
__all__ = ("MarkupTextField", )

import logging
import os

# Configure logger
logger = logging.getLogger('markuptextfield')
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create file handler to save logs to a file
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'markuptextfield_debug.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Silence PIL debug messages
logging.getLogger('PIL').setLevel(logging.INFO)

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (ObjectProperty, 
                             NumericProperty, 
                             VariableListProperty, 
                             ColorProperty, 
                             BooleanProperty,
                             StringProperty,
                             OptionProperty)
from kivy.base import EventLoop
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.core.text.markup import MarkupLabel as Label
from kivy.cache import Cache
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
# import and pass to add it to the new textfield
from kivymd.uix.textfield import (MDTextFieldHelperText,
                                  MDTextFieldTrailingIcon, 
                                  MDTextFieldHintText,
                                  MDTextFieldLeadingIcon,
                                  )
import re
import os

with open(
    os.path.join(os.path.dirname(__file__), "markuptextfield.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())

Cache_register = Cache.register
Cache_append = Cache.append
Cache_get = Cache.get
Cache_remove = Cache.remove
Cache_register('textinput.markup_width', timeout=60.)

#Clipboard = None

if Config:
    _is_desktop = Config.getboolean('kivy', 'desktop')
    # _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    # _scroll_distance = '{}sp'.format(Config.getint('widgets',
    #                                                'scroll_distance'))

class MarkupTextFieldCutCopyPaste(MDDropdownMenu):
    """Internal class used for showing the dropdown menu when
    copy/cut/paste happens. """
    markuptextfield = ObjectProperty(None)
    _textfield_pos_x = NumericProperty(None)
    _textfield_pos_y = NumericProperty(None)
    
    def __init__(self, position, markuptextfield=None, **kwargs):
        super().__init__(**kwargs)
        self.markuptextfield = markuptextfield

        for item in self.items:
            if item['text'] == 'Hint':
                item['on_release'] = self._make_callback(self.markuptextfield.admin, 'hint')
            elif item['text'] == 'Release':
                item['on_release'] = self._make_callback(self.markuptextfield.admin, 'release')
            elif item['text'] == 'Cut':
                item['on_release'] = self._make_callback(self.markuptextfield.cut, self.markuptextfield.selection_text)
            elif item['text'] == 'Copy':
                item['on_release'] = self._make_callback(self.markuptextfield.copy)
            elif item['text'] == 'Paste':
                item['on_release'] = self._make_callback(self.markuptextfield.paste)
            elif item['text'] == 'Select All':
                item['on_release'] = self._make_callback(self.markuptextfield.select_all)
        
        self._textfield_pos_x = int(position[0])
        self._textfield_pos_y = int(position[1])

    def _make_callback(self, func, *args):
        def callback(*_):
            func(*args)
            Clock.schedule_once(lambda dt: self.dismiss(), 0.5)
            return True
        return callback

    def set_menu_pos(self, *args) -> None:
        if self._textfield_pos_y is not None and self._textfield_pos_y > Window.height / 3:
            self.pos = (self._textfield_pos_x, self._textfield_pos_y - (self.height / 2) - dp(28))
        elif self._textfield_pos_y is not None and self._textfield_pos_y <= Window.height / 3:
            self.pos = (self._textfield_pos_x, self._textfield_pos_y + (self.height / 2) + dp(28))
        elif self._textfield_pos_y is not None:
            self.pos = (self._textfield_pos_x, self._textfield_pos_y)
        else:
            super().set_menu_pos(*args)

    def set_menu_properties(self, *args) -> None:
        """Sets the size and position for the menu window.
        Overridden to use the specific mouse cursor position."""

        if self.caller:
            self.menu.data = self._items
            # We need to pick a starting point, see how big we need to be,
            # and where to grow to.
            self._start_coords = self._textfield_pos_x, self._textfield_pos_y

            self.adjust_width()
            self.set_target_height()
            self.check_ver_growth()
            self.check_hor_growth()

    def on_markuptextfield(self, instance, value):
        global Clipboard
        if value and not Clipboard and not _is_desktop:
            value._ensure_clipboard()

class MarkupTextField(TextInput, ThemableBehavior):
    ''' Overridden TextInput class to handle markup text. 
    Added Material Design TextField features. '''

    __events__ = ('on_touch_up',)

    admin_enabled = BooleanProperty(False)
    role = StringProperty("large") #MD
    mode = OptionProperty("outlined", options=["outlined", "filled"]) #MD
    error_color = ColorProperty(None) #MD
    error = BooleanProperty(False) #MD
    use_menu = BooleanProperty(True)
    radius = VariableListProperty([dp(4), dp(4), dp(4), dp(4)]) #MD
    required = BooleanProperty(False) #MD
    line_color_normal = ColorProperty(None) #MD
    line_color_focus = ColorProperty(None) #MD # Remove the invalid truncate parameter
    _helper_text_label = ObjectProperty() #MD
    _hint_text_label = ObjectProperty() #MD
    _leading_icon = ObjectProperty() #MD
    _trailing_icon = ObjectProperty() #MD
    _max_length_label = ObjectProperty() #MD
    _max_length = "0" #MD
    _indicator_height = NumericProperty(dp(1)) #MD
    _outline_height = NumericProperty(dp(1)) #MD
    # The x,y-axis position of the hint text in the text field.
    _hint_x = NumericProperty(0) #MD
    _hint_y = NumericProperty(0) #MD
    # The right/left lines coordinates of the text field in 'outlined' mode.
    _left_x_axis_pos = NumericProperty(dp(32)) #MD
    _right_x_axis_pos = NumericProperty(dp(32)) #MD
    text_default_color = StringProperty("cdcdcd") #MD
    _empty_texture = ObjectProperty(None) #MD
    _saved_markup = StringProperty("[color=FFFFFF]") #MD

    def __init__(self, **kwargs):
        self._label_cached = Label()
        self.selection_previous = None
        self.plaintext = ""
        self.use_markup = True
        self.hint_info = [] # for use in hinting, 2nd item is for host/admin hinting
        self._lines_plaintext = []  # Add a list to store plain text lines
        self._markup_to_plain_map = {}  # Dictionary to map markup positions to plain text positions
        super().__init__(**kwargs)

        self.use_bubble = False
        self.bind(text=self.set_text) #MD
        self._line_options = kw = self._get_line_options()
        self._label_cached = Label(**kw)
        self._empty_texture = self._create_empty_texture()
        
        # Initialize the cut/copy/paste menu
        self._cut_copy_paste_menu = None
        Clock.schedule_once(self._check_text)

    def on_text(self, instance, value):
        # Update the plain text lines list
        self._update_plaintext_lines()
        # Update the markup to plain text mapping
        self._update_markup_to_plain_map()
        
    @property
    def line_count(self) -> int:
        return len(self._lines)

    @property
    def end_cursor(self):
        return len(self._lines[-1]), len(self._lines)

    @staticmethod
    def strip_markup(text):
        # Remove Kivy markup tags for plain text operations
        # First, handle complete markup tags
        text = re.sub(r'\[/?[a-zA-Z0-9_=,#.\-]+\]', '', text)
        # Then remove any partial markup tags (text starting with [)
        text = re.sub(r'\[.*$', '', text)
        return text

    def _update_plaintext_lines(self):
        """Update the _lines_plaintext list with plain text versions of each line"""
        _text = self.text
        _lines = self._lines
        self._lines_plaintext = [self.strip_markup(line) for line in _lines]
        self.plaintext = self.strip_markup(_text)

    def _update_markup_to_plain_map(self):
        """Create a mapping between markup positions and plain text positions"""
        self._markup_to_plain_map = {}
        markup_index = [0]
        plain_index = 1 # Start at 0, increase on found markup characters
        in_markup = False
        text = self.text
        # Work directly with the text string
        for i, char in enumerate(text, 1):
            try:
                if char == '[':
                    # Start of a markup tag
                    if not in_markup:
                        markup_index = [i]
                        in_markup = True
                    else:
                        # If we're already in a markup tag, add this position to the current tag
                        markup_index.append(i)
                elif char == ']' and in_markup:
                    # End of a markup tag...but wait theres more!
                    # Check if we're not at the end of the string before accessing text[i]
                    if i < len(text) and text[i] == '[':
                        markup_index.append(i)
                    # End of a markup tag
                    else:
                        # Map all positions in the markup tag to the same plain text position
                        self._markup_to_plain_map[tuple(markup_index)] = plain_index
                        in_markup = False
                elif not in_markup:
                    # Regular character outside of markup
                    self._markup_to_plain_map[tuple([i])] = plain_index
                    plain_index += 1
                else:
                    # Character inside a markup tag
                    markup_index.append(i)
            except IndexError:
                # If we hit an index error, just continue to the next character
                continue

    def _refresh_text(self, *args):
        """Override to update plain text lines when text is refreshed"""
        super(MarkupTextField, self)._refresh_text(*args)
        self._update_plaintext_lines()
        self._update_markup_to_plain_map()

    def _create_line_label(self, text, hint=False):
        '''Create a label from a text, using line options'''

        # If the text is not in a color tag and has no new lines, we're not using it
        # These are created because kivy can't dectect how much space a line takes up
        # so we increment until we find something that works - we know this doesn't work
        # so just fail it.
        if not self._is_color_tag(text) and text.find(u'\n') == 0:
            return self._empty_texture
        
        ntext = text.replace(u'\n', u'').replace(u'\t', u' ' * self.tab_width)
        
        if self.password and not hint:  # Don't replace hint_text with *
            ntext = self.password_mask * len(ntext)

        kw = self._get_line_options()

        cid = u'{}\0{}\0{}'.format(ntext, self.password, kw)
        texture = Cache_get('textinput.label', cid)
        if texture is None:
            # FIXME right now, we can't render very long line...
            # if we move on "VBO" version as fallback, we won't need to
            # do this. try to find the maximum text we can handle

            # TODO: God this is so fucking stupid, and won't work in some cases.
            #Need to instead find the max character amt in the space
            #That doesn't work with non-monospace fonts but should work here

            label = Label(text=ntext, **kw)
            start_tag = ""
            end_tag = ""
            almost_end_tag = ""
            if len(label.markup) > 0:
                start_tag = label.markup[0]
                end_tag = label.markup[-1]
                if len(label.markup) > 1:
                    almost_end_tag = label.markup[-2]
                    if start_tag == " ":
                        start_tag = label.markup[1]
                    if end_tag == " ":
                        end_tag = label.markup[-2]
                    if almost_end_tag == " " and len(label.markup) > 2:
                        almost_end_tag = label.markup[-3]
            if start_tag == '[b]' and end_tag != '[/b]':
                ntext = u'{}[/b]'.format(ntext)
                label = Label(text=ntext, **kw)
            elif end_tag == '[/b]' and start_tag != '[b]':
                ntext = u'[b]{}'.format(ntext)
                label = Label(text=ntext, **kw)
            elif end_tag != '[/color]':
                self._saved_markup = almost_end_tag
                ntext = u'{}[/color]'.format(ntext)
                label = Label(text=ntext, **kw)
            elif start_tag.count('color') == 0 and end_tag == '[/color]':
                ntext = u'{}{}'.format(self._saved_markup, ntext)
                label = Label(text=ntext, **kw)
            if text.find(u'\n') > 0:
                label.text = u''
            else:
                label.text = ntext
            label.refresh()
            texture = label.texture
            Cache_append('textinput.label', cid, texture)
            label.text = u''
        return texture

    def _get_line_options(self):
        kw = super(MarkupTextField, self)._get_line_options()
        #kw['font_blended'] = False
        kw['markup'] = True
        #kw['valign'] = 'top'
        return kw

    def _get_text_width(self, text, tab_width, _label_cached):
        # Return the width of a text, according to the current line options.
        kw = self._get_line_options()
        
        # Create cache key based on text and options
        if self.use_markup:
            cid = u'{}\0{}\0{}'.format(text, self.password, kw)
            cache_key = 'textinput.markup_width'
        else:
            cid = u'{}\0{}'.format(text, self.password)
            cache_key = 'textinput.width'
            
        # Check cache first
        width = Cache_get(cache_key, cid)
        if width is not None:
            return width
            
        # If not in cache, calculate width
        if self.use_markup:
            # For markup text, we need to handle the width calculation differently
            # First, check if we're in the middle of a markup tag
            if '[' in text and ']' not in text or ']' in text and '[' not in text:
                # If we're in the middle of a markup tag, return 0 width
                return 0
               
            # Get the plain text version
            plain_text = self.strip_markup(text)
            # Create a label with the plain text
            temp_kw = kw.copy()
            temp_kw['markup'] = False
            temp_label = Label(text=plain_text, **temp_kw)
            temp_label.refresh()
            width = temp_label.width
        else:
            if not _label_cached:
                _label_cached = self._label_cached
            text = text.replace('\t', ' ' * tab_width)
            if not self.password:
                width = _label_cached.get_extents(text)[0]
            else:
                width = _label_cached.get_extents(
                    self.password_mask * len(text))[0]
                    
        # Cache the result
        Cache_append(cache_key, cid, width)
        return width

    def _is_color_tag(self, text) -> bool:
        """Check if the text is in a color tag with format [color=XXXXXX]text[/color]
        where XXXXXX is a 6-digit hex color code (0-9A-F), or if it contains just a closing color tag"""
        import re
        # Pattern for complete color tag pair
        complete_pattern = r'.*\[color=[0-9A-Fa-f]{6}\].*\[\/color\].*'
        # Pattern for just a closing color tag - this will flag the markup warning but necessary for
        # word wraps
        closing_pattern = r'.*\[\/color\].*'
        return bool(re.match(complete_pattern, text) or re.match(closing_pattern, text))


    def cursor_offset(self):
        '''Get the cursor x offset on the current line'''
        row = int(self.cursor_row)
        col = int(self.cursor_col) # Subtract 1 because the cursor is 1 character after the text index
        lines = self._lines
        offset = 0

        try:
            # If not multiline, treat the entire text as a single line
            if not self.multiline:
                markup_text = self.text[:col]
                offset = self._get_text_width(markup_text, self.tab_width, self._label_cached)
                return offset

            if col:
                # Get the text up to the cursor position
                markup_text = lines[row][:col]
                
                # Special handling for beginning of line
                if col == len(lines[row]):
                    # If at end of line, use the whole line
                    offset = self._get_text_width(markup_text, self.tab_width, self._label_cached)
                else:
                    # Find the first ] in the line to determine where actual text starts
                    first_bracket_end = lines[row].find(']')
                    if first_bracket_end >= 0 and col <= first_bracket_end:
                        # If cursor is before or at the first ], width should be 0
                        offset = 0
                    else:
                        # Use cached width calculation
                        offset = self._get_text_width(markup_text, self.tab_width, self._label_cached)
          
                return offset
        except Exception as e:
            logger.debug(f"Error calculating cursor offset - {str(e)}")
        finally:
            return offset
        
    def cursor_index(self, cursor=None):
        '''Return the cursor index in the text value.
        '''
        if not cursor:
            cursor = self.cursor
        try:
            # Get the position in the markup text
            position = self._map_cursor_to_markup_position(cursor)
            return position
        except IndexError:
            return 0

    def on_touch_down(self, touch):
        """Override to prevent deselection on right-click"""
        # If right-clicking on a selection, prevent deselection
        # But still allow the event to propagate for menu handling
        if self.disabled:
            return
        
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        touch_pos = touch.pos

        self._touch_count += 1
        if touch.button == 'right' and self.collide_point(*touch.pos):
            return True
        # For all other touches, let the parent handle it
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Override to handle right-click menu"""
        if touch.grab_current is self and touch.button == 'right':
            touch.ungrab(self)
            self._touch_count -= 1
            win = EventLoop.window
            self._show_cut_copy_paste(position=touch.pos, touch=touch, win=win)
            return True
        return super().on_touch_up(touch)
        

    def copy(self, data=''):
        """Override copy to use plain text for selection"""
        if not self.allow_copy:
            return
        if data:
            Clipboard.copy(data)
        elif self.selection_text:
            Clipboard.copy(self.selection_text)
        elif self.selection_previous:
            Clipboard.copy(self.selection_previous)
        else:
            # If no selection, copy the current line in plain text
            row = int(self.cursor_row)
            if row < len(self._lines_plaintext):
                Clipboard.copy(self._lines_plaintext[row])

    def _update_selection(self, finished=False):
        '''Update selection text and order of from/to if finished is True.
        Can be called multiple times until finished is True.
        '''
        # Get the selection range in markup text
        a, b = int(self._selection_from), int(self._selection_to)
        # Store the original direction for later use
        selection_reversed = a > b
        
        # For internal processing, we need a consistent order
        if selection_reversed:
            a, b = b, a
            
        self._selection_finished = finished

        # Map the selection indices to the plaintext
        plain_a = self._get_plain_from_markup_index(a)
        plain_b = self._get_plain_from_markup_index(b)
  
        _selection_text = self.plaintext[plain_a:plain_b]

        self.selection_text = ("" if not self.allow_copy else
                               ((self.password_mask * (plain_b - plain_a)) if
                                self.password else _selection_text))
        
        self.selection_previous = self.selection_text

        if not finished:
            self._selection = True
        else:
            self._selection = bool(len(_selection_text))
            self._selection_touch = None
        if a == 0:
            # update graphics only on new line
            # allows smoother scrolling, noticeably
            # faster when dealing with large text.
            self._update_graphics_selection()

    def _get_plain_from_markup_index(self, position):
        """Map markup text indices to plain text positions using the mapping dictionary"""
        if position > len(self.text):
            logger.debug(f"Selection out of bounds - Position: {position}, Text length: {len(self.text)}")
            return 0

        # Find the position in the mapping dictionary
        for markup_index in self._markup_to_plain_map.keys():
            if position in markup_index:
                #logger.debug(f"Position: {position}, Markup index: {markup_index}, Plain index: {self._markup_to_plain_map[markup_index]}")
                return self._markup_to_plain_map[markup_index]
        # This is to prevent initialization errors
        return 0

    def _map_cursor_to_markup_position(self, cursor):
        """Map cursor position (col, row) to a position in the markup text"""
        lines = self._lines
        lines_flags = self._lines_flags
        col, row = cursor
        #lines_flags 
        if row >= len(lines):
            return len(self.text)
        
        # Calculate the position in the markup text
        position = 0
        for i, line in enumerate(lines[:row]):
            position += len(line) + lines_flags[i]
        
        # Add the column position
        position += col
        full_length = 0 
        for i, line in enumerate(lines):
            full_length += len(line) + lines_flags[i]

        # if full_length == 8472:
        #     logger.debug(f"full_length: {full_length}") # adding the flags, and now they match!
        #     logger.debug(f"len(self.text): {len(self.text)}") # printing 8472
        #     logger.debug(f"len(self.plaintext): {len(self.plaintext)}") # 4030
        # for i in self._markup_to_plain_map.keys():
        #     if full_length in i:
        #         logger.debug(f"last mapped position: {self._markup_to_plain_map[i]}") #4030 please

        # Ensure we don't exceed the text length
        return min(position, len(self.text))
        
    def _select_word(self, delimiters=u' .,:;!?\'"<>(){}'):
        '''Select the tag's contents at the cursor, or 
        the word at the cursor if no tag is selected'''
        cindex = self.cursor_index()
        col = self.cursor_col
        row = self.cursor_row
        line = self._lines[row]
        flag = self._lines_flags[row]
        line_length = len(line)
        enil = str(line[::-1]) #backwards line to find the closest tag
        start = 0
        end = 0

        if col >= line_length:
            col = line_length - 1
        # look for a color markup tag first - if found, select the tag's contents
        for char in enil[-(col):]:
            if char == ']':
                start_tag = re.search(r"\][A-Fa-f0-9]{6}=roloc\[", enil[-(col):]) #search for the start tag...backwards
                #logger.debug(f"start_tag: {start_tag}")
                if start_tag:
                    start = start_tag.end()-flag
                    break
                else:
                    # if we find a tag that isn't a color tag, break
                    if re.search(r"\]", enil[-(col):]):
                        break
        for char in line[col:]:
            if char == '[':
                end_tag = re.search(r"\[/color\]", line[col:]) #search for the end tag
                #logger.debug(f"end_tag: {end_tag}")
                if end_tag:
                    end = end_tag.start()+1
                    break     
                else:
                    # if we find a tag that isn't a color tag, break
                    if re.search(r"\[", line[col:]):
                        break
        
        if start==0 and end==0:
            # if no color markup tag is found, select the word at the cursor
            start = max(0, len(line[:col]) -
                        max(line[:col].rfind(s) for s in delimiters) - 1)
            end = min((line[col:].find(s) if line[col:].find(s) > -1
                    else (len(line) - col)) for s in delimiters)
            
        Clock.schedule_once(lambda dt: self.select_text(cindex - start,
                                                        cindex + end))

    def admin(self, action, *args):
        """Handle admin menu item click"""
        if self.selection_text:
            self.admin_info = [self.selection_text, self._lines_plaintext[int(self.cursor_row)]]
        else:
            # If no selection, use the current line
            row = int(self.cursor_row)
            self.admin_info = ["", self._lines_plaintext[row]]
        if action == "hint":
            logger.debug("Executing hint action on text: {self.admin_info[0]}")
        elif action == "release":
            logger.debug("Executing release action on text: {self.admin_info[0]}")

    def _show_cut_copy_paste(self, position, win, touch=None ,parent_changed=False, mode='', pos_in_window=False, *l):
        """Override to use MarkupTextFieldCutCopyPaste instead of TextInputCutCopyPaste"""
        # Don't touch the menu if it's not enabled or if touch is a tuple
        if not self.use_menu or touch == None:
            return
        if touch.button != 'right':
            return

        # If parent changed, just return
        if parent_changed:
            return
            
        # If we already have a menu, dismiss it
        if self._cut_copy_paste_menu is not None:
            self._cut_copy_paste_menu.dismiss()
            if not self.parent:
                return
        
        menu_items = self._menu_items()
        #logger.debug(f"Menu items: {menu_items}")

        # Create a new menu if needed
        try:
            # Create the menu with the correct parameters
            self._cut_copy_paste_menu = MarkupTextFieldCutCopyPaste(
                markuptextfield=self,
                position=position,
                caller=self,
                items=menu_items
            )
            
            # Set the menu position
            self._cut_copy_paste_menu.set_menu_pos(position)
            
            # Bind to parent changes to handle cleanup
            self.fbind('parent', self._on_parent_changed)
            
            # Bind to focus and cursor position changes to hide menu
            self.bind(
                focus=self._on_focus_change,
                cursor_pos=self._on_cursor_pos_change
            )
            
            # Open the menu immediately
            self._cut_copy_paste_menu.open()
            self._hide_handles(win=win)
            # Clear the menu opening flag after a short delay
            
        except Exception as e:
            logger.error(f"Error showing cut/copy/paste menu: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def _on_parent_changed(self, instance, value):
        """Handle parent changes to clean up menu"""
        if self._cut_copy_paste_menu:
            self._hide_cut_copy_paste()
            
    def _on_focus_change(self, instance, value):
        """Handle focus changes to hide menu"""
        if not value and self._cut_copy_paste_menu:
            self._hide_cut_copy_paste()
            
    def _on_cursor_pos_change(self, instance, value):
        """Handle cursor position changes to hide menu"""
        # Only dismiss the menu if the cursor position changes significantly
        # This prevents the menu from closing immediately when it opens
        if self._cut_copy_paste_menu and hasattr(self, '_last_cursor_pos'):
            # Calculate the distance between the current and last cursor position
            current_pos = value
            last_pos = self._last_cursor_pos
            distance = abs(current_pos[0] - last_pos[0]) + abs(current_pos[1] - last_pos[1])
            
            # Only dismiss if the cursor has moved more than a few pixels
            if distance > 10:  # Adjust this threshold as needed
                self._hide_cut_copy_paste()
        
        # Store the current cursor position
        self._last_cursor_pos = value

    def _hide_cut_copy_paste(self, win=None):
        """Override to use MarkupTextFieldCutCopyPaste instead of TextInputCutCopyPaste"""
        if not self._cut_copy_paste_menu:
            return
            
        try:
            # Dismiss the menu
            self._cut_copy_paste_menu.dismiss()
            
            # Unbind events to prevent memory leaks
            self.unbind(
                focus=self._on_focus_change,
                cursor_pos=self._on_cursor_pos_change
            )
            self.funbind('parent', self._on_parent_changed)
            
            # Clear the reference
            self.selection_previous = None
            self._cut_copy_paste_menu = None
            
        except Exception as e:
            logger.error(f"Error hiding cut/copy/paste menu: {str(e)}")

    def _menu_items(self):
        menu_items = [
            {"text": "Cut", "trailing_icon": "content-cut"},
            {"text": "Copy", "trailing_icon": "content-copy"},
            {"text": "Paste", "trailing_icon": "content-paste"},
            {"text": "Select All", "trailing_icon": "select-all"},
        ]
        # If the text field is admin enabled, add the hint and release options
        if self.admin_enabled:
            menu_items.append({"text": "Hint", "trailing_icon": "magnify-scan"})
            menu_items.append({"text": "Release", "trailing_icon": "lock-open-variant-outline"})
        if self.readonly:
            for item in menu_items:
                if item["text"] == "Cut":
                    menu_items.remove(item)
                if item["text"] == "Paste":
                    menu_items.remove(item) 

        for item in menu_items:
            item['text_color'] = self.theme_cls.onPrimaryContainerColor
            item['trailing_icon_color'] = self.theme_cls.primaryColor
            if item == menu_items[-1]:
                item['divider'] = None
                
        #logger.debug(f"Created menu items: {menu_items}")
        return menu_items

    '''
    Can't inherit from MDTextField, so cut and paste it is, I guess.
    '''

    def add_widget(self, widget, index=0, canvas=None):
        if isinstance(widget, MDTextFieldHelperText):
            self._helper_text_label = widget
        if isinstance(widget, MDTextFieldHintText):
            self._hint_text_label = widget
        if isinstance(widget, MDTextFieldLeadingIcon):
            self._leading_icon = widget
        if isinstance(widget, MDTextFieldTrailingIcon):
            self._trailing_icon = widget
        else:
            return super().add_widget(widget)

    def set_texture_color(
        self, texture, canvas_group, color: list, error: bool = False
    ) -> None:
        """
        Animates the color of the
        leading/trailing icons/hint/helper/max length text.
        """

        def update_hint_text_rectangle(*args):
            hint_text_rectangle = self.canvas.after.get_group(
                "hint-text-rectangle"
            )[0]
            hint_text_rectangle.texture = None
            texture.texture_update()
            hint_text_rectangle.texture = texture.texture

        if texture:
            Animation(rgba=color, d=0).start(canvas_group)
            a = Animation(color=color, d=0)
            if texture is self._hint_text_label:
                a.bind(on_complete=update_hint_text_rectangle)
            a.start(texture)

    def set_pos_hint_text(self, y: float, x: float) -> None:
        """Animates the x-axis width and y-axis height of the hint text."""

        Animation(_hint_y=y, _hint_x=x, d=0.2, t="out_quad").start(self)

    def set_hint_text_font_size(self) -> None:
        """Animates the font size of the hint text."""

        Animation(
            size=self._hint_text_label.texture_size, d=0.2, t="out_quad"
        ).start(self.canvas.after.get_group("hint-text-rectangle")[0])

    def set_space_in_line(
        self, left_width: float | int, right_width: float | int
    ) -> None:
        """
        Animates the length of the right line of the text field for the
        hint text.
        """

        Animation(_left_x_axis_pos=left_width, d=0.2, t="out_quad").start(self)
        Animation(_right_x_axis_pos=right_width, d=0.2, t="out_quad").start(
            self
        )

    def set_max_text_length(self) -> None:
        """
        Fired when text is entered into a text field.
        Set max length text and updated max length texture.
        """

        if self._max_length_label:
            self._max_length_label.text = ""
            self._max_length_label.text = (
                f"{len(self.text)}/{self._max_length_label.max_text_length}"
            )
            self._max_length_label.texture_update()
            max_length_rect = self.canvas.before.get_group("max-length-rect")[0]
            max_length_rect.texture = None
            max_length_rect.texture = self._max_length_label.texture
            max_length_rect.size = self._max_length_label.texture_size
            max_length_rect.pos = (
                (self.x + self.width)
                - (self._max_length_label.texture_size[0] + self.font_size),
                self.y - self.font_size + dp(2),
            )

    def _add_default_color(self, line):
        if line.startswith("[color="):
            return line
        else:
            return "[color={color}]{line}[/color]".format(color=self.text_default_color, line=line)

    def set_text(self, instance, text: str) -> None:
        """Fired when text is entered into a text field."""

        def set_text(*args):
            if self.line_count > 1000:
                self._lines = self._lines[-1000:] #_lines is bound to the text property
            
            # Process the incoming text to add color tags using patterns
            if self.multiline:
                # Simple pattern-based approach:
                # 1. [/color]\n needs a [color= after it
                # 2. \n with no color blocks needs both [color= and [/color]
                # 3. \n[color= needs a [/color] before it
                
                # Add opening color tags after [/color]\n (but only if not already followed by [color=)
                text = re.sub(r'\[/color\]\n(?!\[color=)', f'[/color]\n[color={self.text_default_color}]', text)
                
                # Add closing color tags before \n[color= (but only if not already preceded by [/color])
                text = re.sub(r'(?<!\[/color\])\n\[color=', f'[/color]\n[color=', text)
                
                # Add both tags around \n that don't have color blocks (but only if not already handled)
                text = re.sub(r'(?<!\[/color\])\n(?!\[color=)', f'[/color]\n[color={self.text_default_color}]', text)
                
                self.text = text
            else:
                self.text = re.sub("\n", " ", text)
            self.set_max_text_length()

            if self.text and self._get_has_error() or self._get_has_error():
                self.error = True
            elif self.text and not self._get_has_error():
                self.error = False

            # Start the appropriate texture animations when programmatically
            # pasting text into a text field.
            if len(self.text) != 0 and not self.focus:
                if self._hint_text_label:
                    self._hint_text_label.font_size = self.theme_cls.theme_font_style[
                        self._hint_text_label.font_style
                    ]["small"]["font-size"]
                    self._hint_text_label.texture_update()
                    self.set_hint_text_font_size()

            if (not self.text and not self.focus) or (
                self.text and not self.focus
            ):
                self.on_focus(instance, False)

        set_text()

    def on_focus(self, instance, focus: bool) -> None:
        """Fired when the `focus` value changes."""

        if focus:
            if self.mode == "filled":
                Animation(_indicator_height=dp(1.25), d=0).start(self)
            else:
                Animation(_outline_height=dp(1.25), d=0).start(self)

            if self._trailing_icon:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._trailing_icon,
                        self.canvas.before.get_group("trailing-icons-color")[0],
                        (
                            self.theme_cls.onSurfaceVariantColor
                            if self._trailing_icon.theme_icon_color == "Primary"
                            or not self._trailing_icon.icon_color_focus
                            else self._trailing_icon.icon_color_focus
                        )
                        if not self.error
                        else self._get_error_color(),
                    )
                )
            if self._leading_icon:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._leading_icon,
                        self.canvas.before.get_group("leading-icons-color")[0],
                        self.theme_cls.onSurfaceVariantColor
                        if self._leading_icon.theme_icon_color == "Primary"
                        or not self._leading_icon.icon_color_focus
                        else self._leading_icon.icon_color_focus,
                    )
                )
            if self._max_length_label and not self.error:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._max_length_label,
                        self.canvas.before.get_group("max-length-color")[0],
                        self.theme_cls.onSurfaceVariantColor
                        if not self._max_length_label.text_color_focus
                        else self._max_length_label.text_color_focus,
                    )
                )

            if self._helper_text_label and self._helper_text_label.mode in (
                "on_focus",
                "persistent",
            ):
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._helper_text_label,
                        self.canvas.before.get_group("helper-text-color")[0],
                        (
                            self.theme_cls.onSurfaceVariantColor
                            if not self._helper_text_label.text_color_focus
                            else self._helper_text_label.text_color_focus
                        )
                        if not self.error
                        else self._get_error_color(),
                    )
                )
            if (
                self._helper_text_label
                and self._helper_text_label.mode == "on_error"
                and not self.error
            ):
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._helper_text_label,
                        self.canvas.before.get_group("helper-text-color")[0],
                        self.theme_cls.transparentColor,
                    )
                )
            if self._hint_text_label:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._hint_text_label,
                        self.canvas.after.get_group("hint-text-color")[0],
                        (
                            self.theme_cls.primaryColor
                            if not self._hint_text_label.text_color_focus
                            else self._hint_text_label.text_color_focus
                        )
                        if not self.error
                        else self._get_error_color(),
                    )
                )
                self.set_pos_hint_text(
                    0 if self.mode != "outlined" else dp(-14),
                    (
                        -(
                            (
                                self._leading_icon.texture_size[0]
                                if self._leading_icon
                                else 0
                            )
                            + dp(12)
                        )
                        if self._leading_icon
                        else 0
                    )
                    if self.mode == "outlined"
                    else -(
                        (
                            self._leading_icon.texture_size[0]
                            if self._leading_icon
                            else 0
                        )
                        - dp(24)
                    ),
                )
                self._hint_text_label.font_size = self.theme_cls.theme_font_styles[
                    self._hint_text_label.font_style
                ]["small"]["font-size"]
                self.set_hint_text_font_size()
                if self.mode == "outlined":
                    self.set_space_in_line(
                        dp(14), self._hint_text_label.texture_size[0] + dp(18)
                    )
        else:
            if self.mode == "filled":
                Animation(_indicator_height=dp(1), d=0).start(self)
            else:
                Animation(_outline_height=dp(1), d=0).start(self)

            if self._leading_icon:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._leading_icon,
                        self.canvas.before.get_group("leading-icons-color")[0],
                        self.theme_cls.onSurfaceVariantColor
                        if self._leading_icon.theme_icon_color == "Primary"
                        or not self._leading_icon.icon_color_normal
                        else self._leading_icon.icon_color_normal,
                    )
                )
            if self._trailing_icon:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._trailing_icon,
                        self.canvas.before.get_group("trailing-icons-color")[0],
                        (
                            self.theme_cls.onSurfaceVariantColor
                            if self._trailing_icon.theme_icon_color == "Primary"
                            or not self._trailing_icon.icon_color_normal
                            else self._trailing_icon.icon_color_normal
                        )
                        if not self.error
                        else self._get_error_color(),
                    )
                )
            if self._max_length_label and not self.error:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._max_length_label,
                        self.canvas.before.get_group("max-length-color")[0],
                        self.theme_cls.onSurfaceVariantColor
                        if not self._max_length_label.text_color_normal
                        else self._max_length_label.text_color_normal,
                    )
                )
            if (
                self._helper_text_label
                and self._helper_text_label.mode == "on_focus"
            ):
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._helper_text_label,
                        self.canvas.before.get_group("helper-text-color")[0],
                        self.theme_cls.transparentColor,
                    )
                )
            elif (
                self._helper_text_label
                and self._helper_text_label.mode == "persistent"
            ):
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._helper_text_label,
                        self.canvas.before.get_group("helper-text-color")[0],
                        (
                            self.theme_cls.onSurfaceVariantColor
                            if not self._helper_text_label.text_color_normal
                            else self._helper_text_label.text_color_normal
                        )
                        if not self.error
                        else self._get_error_color(),
                    )
                )

            if not self.text:
                if self._hint_text_label:
                    if self.mode == "outlined":
                        self.set_space_in_line(dp(32), dp(32))
                    self._hint_text_label.font_size = self.theme_cls.theme_font_style[
                        self._hint_text_label.font_style
                    ]["large"]["font-size"]
                    self._hint_text_label.texture_update()
                    self.set_hint_text_font_size()
                    self.set_pos_hint_text(
                        (self.height / 2)
                        - (self._hint_text_label.texture_size[1] / 2),
                        0,
                    )
            else:
                if self._hint_text_label:
                    if self.mode == "outlined":
                        self.set_space_in_line(
                            dp(14),
                            self._hint_text_label.texture_size[0] + dp(18),
                        )
                    self.set_pos_hint_text(
                        0 if self.mode != "outlined" else dp(-14),
                        (
                            -(
                                (
                                    self._leading_icon.texture_size[0]
                                    if self._leading_icon
                                    else 0
                                )
                                + dp(12)
                            )
                            if self._leading_icon
                            else 0
                        )
                        if self.mode == "outlined"
                        else -(
                            (
                                self._leading_icon.texture_size[0]
                                if self._leading_icon
                                else 0
                            )
                            - dp(24)
                        ),
                    )

            if self._hint_text_label:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._hint_text_label,
                        self.canvas.after.get_group("hint-text-color")[0],
                        (
                            self.theme_cls.onSurfaceVariantColor
                            if not self._hint_text_label.text_color_normal
                            else self._hint_text_label.text_color_normal
                        )
                        if not self.error
                        else self._get_error_color(),
                    ),
                )

    def on_disabled(self, instance, disabled: bool) -> None:
        """Fired when the `disabled` value changes."""

        super().on_disabled(instance, disabled)

        def on_disabled(*args):
            if disabled:
                self._set_disabled_colors()
            else:
                self._set_enabled_colors()

        Clock.schedule_once(on_disabled, 0.2)

    def on_error(self, instance, error: bool) -> None:
        """
        Changes the primary colors of the text box to match the `error` value
        (text field is in an error state or not).
        """

        if error:
            if self._max_length_label:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._max_length_label,
                        self.canvas.before.get_group("max-length-color")[0],
                        self._get_error_color(),
                    )
                )
            if self._hint_text_label:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._hint_text_label,
                        self.canvas.after.get_group("hint-text-color")[0],
                        self._get_error_color(),
                    ),
                )
            if self._helper_text_label and self._helper_text_label.mode in (
                "persistent",
                "on_error",
            ):
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._helper_text_label,
                        self.canvas.before.get_group("helper-text-color")[0],
                        self._get_error_color(),
                    )
                )
            if self._trailing_icon:
                Clock.schedule_once(
                    lambda x: self.set_texture_color(
                        self._trailing_icon,
                        self.canvas.before.get_group("trailing-icons-color")[0],
                        self._get_error_color(),
                    )
                )
        else:
            self.on_focus(self, self.focus)


    def _set_enabled_colors(self):
        def schedule_set_texture_color(widget, group_name, color):
            Clock.schedule_once(
                lambda x: self.set_texture_color(widget, group_name, color)
            )

        max_length_label_group = self.canvas.before.get_group(
            "max-length-color"
        )
        helper_text_label_group = self.canvas.before.get_group(
            "helper-text-color"
        )
        hint_text_label_group = self.canvas.after.get_group("hint-text-color")
        leading_icon_group = self.canvas.before.get_group("leading-icons-color")
        trailing_icon_group = self.canvas.before.get_group(
            "trailing-icons-color"
        )

        error_color = self._get_error_color()
        on_surface_variant_color = self.theme_cls.onSurfaceVariantColor

        if self._max_length_label:
            schedule_set_texture_color(
                self._max_length_label,
                max_length_label_group[0],
                self._max_length_label.color[:-1] + [1]
                if not self.error
                else error_color,
            )
        if self._helper_text_label:
            schedule_set_texture_color(
                self._helper_text_label,
                helper_text_label_group[0],
                on_surface_variant_color
                if not self._helper_text_label.text_color_focus
                else self._helper_text_label.text_color_focus
                if not self.error
                else error_color,
            )
        if self._hint_text_label:   
            schedule_set_texture_color(
                self._hint_text_label,
                hint_text_label_group[0],
                on_surface_variant_color
                if not self._hint_text_label.text_color_normal
                else self._hint_text_label.text_color_normal
                if not self.error
                else error_color,
            )
        if self._leading_icon:
            schedule_set_texture_color(
                self._leading_icon,
                leading_icon_group[0],
                on_surface_variant_color
                if self._leading_icon.theme_icon_color == "Primary"
                or not self._leading_icon.icon_color_normal
                else self._leading_icon.icon_color_normal,
            )
        if self._trailing_icon:
            schedule_set_texture_color(
                self._trailing_icon,
                trailing_icon_group[0],
                on_surface_variant_color
                if self._trailing_icon.theme_icon_color == "Primary"
                or not self._trailing_icon.icon_color_normal
                else self._trailing_icon.icon_color_normal
                if not self.error
                else error_color,
            )

    def _set_disabled_colors(self):
        def schedule_set_texture_color(widget, group_name, color, opacity):
            Clock.schedule_once(
                lambda x: self.set_texture_color(
                    widget, group_name, color + [opacity]
                )
            )

        max_length_label_group = self.canvas.before.get_group(
            "max-length-color"
        )
        helper_text_label_group = self.canvas.before.get_group(
            "helper-text-color"
        )
        hint_text_label_group = self.canvas.after.get_group("hint-text-color")
        leading_icon_group = self.canvas.before.get_group("leading-icons-color")
        trailing_icon_group = self.canvas.before.get_group(
            "trailing-icons-color"
        )

        disabled_color = self.theme_cls.disabledTextColor[:-1]

        if self._max_length_label:
            schedule_set_texture_color(
                self._max_length_label,
                max_length_label_group[0],
                disabled_color,
                self.text_field_opacity_value_disabled_max_length_label,
            )
        if self._helper_text_label:
            schedule_set_texture_color(
                self._helper_text_label,
                helper_text_label_group[0],
                disabled_color,
                self.text_field_opacity_value_disabled_helper_text_label,
            )
        if self._hint_text_label:
            schedule_set_texture_color(
                self._hint_text_label,
                hint_text_label_group[0],
                disabled_color,
                self.text_field_opacity_value_disabled_hint_text_label,
            )
        if self._leading_icon:
            schedule_set_texture_color(
                self._leading_icon,
                leading_icon_group[0],
                disabled_color,
                self.text_field_opacity_value_disabled_leading_icon,
            )
        if self._trailing_icon:
            schedule_set_texture_color(
                self._trailing_icon,
                trailing_icon_group[0],
                disabled_color,
                self.text_field_opacity_value_disabled_trailing_icon,
            )

    def _get_has_error(self) -> bool:
        """
        Returns `False` or `True` depending on the state of the text field,
        for example when the allowed character limit has been exceeded or when
        the :attr:`~MDTextField.required` parameter is set to `True`.
        """
        if (
            self._max_length_label
            and len(self.text) > self._max_length_label.max_text_length
        ):
            has_error = True
        else:
            if all((self.required, len(self.text) == 0)):
                has_error = True
            else:
                has_error = False
        return has_error

    def _get_error_color(self):
        return (
            self.theme_cls.errorColor
            if not self.error_color
            else self.error_color
        )

    def _create_empty_texture(self):
        """Creates and returns an empty texture with minimal size.
        I hate this."""
        from kivy.graphics.texture import Texture
        empty_texture = Texture.create(size=(1, 1), colorfmt='rgba')
        empty_texture.blit_buffer(b'\x00\x00\x00\x00', colorfmt='rgba', bufferfmt='ubyte')
        return empty_texture

    def _check_text(self, *args) -> None:
        self.set_text(self, self.text)

    def _refresh_hint_text(self):
        """Method override to avoid duplicate hint text texture."""
    
