from __future__ import annotations
__all__ = ("MarkupTextField", )

import os
import logging
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (ObjectProperty, 
                             NumericProperty, 
                             VariableListProperty, 
                             ColorProperty, 
                             BooleanProperty,
                             StringProperty,
                             OptionProperty,
                             DictProperty,
                             ListProperty)
from kivy.base import EventLoop
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.config import Config
from kivy.effects.scroll import ScrollEffect
from kivy.uix.textinput import TextInput, FL_IS_NEWLINE
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
from kivymd.uix.button import MDFabButton
import re
from re import Pattern, compile
import os

logger = logging.getLogger("Client")

def unescape_markup(text):
    '''
    Inverse of escape_markup. Converts Kivy markup entities back to normal characters.
    Used when copying text to clipboard to restore original brackets.
    '''
    return text.replace('&bl;', '[').replace('&br;', ']').replace('&amp;', '&')

HINT_PATTERN = compile(r'(\[Hint\])|(\[[\'"][^\'"]*[\'"](?:,[\s]*[\'"][^\'"]*[\'"])*\])')

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
    _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    _scroll_distance = '{}sp'.format(Config.getint('widgets', 'scroll_distance'))

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
            Clock.schedule_once(lambda dt: self.dismiss(), 1)
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

    plaintext = StringProperty("", cache=True)
    markup_to_plain_map = DictProperty({}, cache=True)
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
    effect_cls = ObjectProperty(ScrollEffect, allow_none=True)
    bottom_scroll_button = ObjectProperty(None)
    current_color_tag = None
    all_patterns = {"color": re.compile(r'\[color=[0-9A-Fa-f]{6}\]'), "bold": re.compile(r'\[b\]'), "italic": re.compile(r'\[i\]'), "underline": re.compile(r'\[u\]')}
    # Pattern to match any valid Kivy markup tag (opening or closing)
    # Matches: [tag], [/tag], [tag=value], [tag=value,value2], etc.
    # Pattern: [ or [/ followed by tag name (letters/numbers/underscores), optionally =value, then ]
    _markup_tag_pattern = re.compile(r'\[/?[a-zA-Z][a-zA-Z0-9_]*(?:[=][^\]]*)?\]')
    
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
    _saved_markup = {"color": "", "bold": "", "italic": "", "underline": ""}
    _lines_plaintext = ListProperty([], cache=True)
    effect_y = ObjectProperty(None)
    _effect_y_start_height = None
    _effect_y_start_scroll = None
    _unclamped_scroll_y = None  # Track unclamped scroll position for velocity calculation
    scroll_velocity = NumericProperty(0.5)  # Scale factor to slow down scrolling
    _manually_scrolled = BooleanProperty(False)
    _markup_to_plain_map = DictProperty({}, cache=True)

    def __init__(self, bottom_scroll_button=None, ignore_patterns: Pattern = None, **kwargs):
        self.bottom_scroll_button = bottom_scroll_button
        self._label_cached = Label()
        self.selection_previous = None
        self.use_markup = True
        self.hint_info = [] # for use in hinting, 2nd item is for host/admin hinting
        self.ignore_patterns = ignore_patterns or None # Patterns to ignore when stripping markup
        super().__init__(**kwargs)

        self.scroll_from_swipe = True
        self.use_bubble = False
        self.bind(text=self.set_text) #MD
        self._line_options = kw = self._get_line_options()
        self._label_cached = Label(**kw)
        self._empty_texture = self._create_empty_texture()
        
        # Initialize the cut/copy/paste menu
        self._cut_copy_paste_menu = None

        Clock.schedule_once(self._check_text)

        effect_cls = self.effect_cls
        if self.effect_y is None and effect_cls is not None:
            self.effect_y = effect_cls(target_widget=self)
            self.effect_y.bind(scroll=self._update_effect_y)
        self.fbind('height', self._update_effect_y_bounds)
        self.bottom_scroll_button.bind(on_release=self.scroll_to_bottom)

    def set_texts(self, text, plaintext):
         # Set texts in a function to pass everything through
         self.plaintext = self.plaintext + u"\n" + plaintext if self.plaintext else plaintext
         self.text = self.text + u"\n" + text if self.text else text
         self._update_plaintext_lines()
        
    @property
    def line_count(self) -> int:
        return len(self._lines)

    @property
    def end_cursor(self):
        return len(self._lines[-1]), len(self._lines)

    @staticmethod
    def strip_markup(text, ignore_patterns: Pattern = None):
        # Remove Kivy markup tags for plain text operations
        # First, handle complete markup tags
        if ignore_patterns:
            # Split by the pattern and rejoin with placeholders, then strip markup, then restore
            parts = ignore_patterns.split(text)
            stripped_parts = [re.sub(r'\[/?[a-zA-Z0-9_=,#.\-]+\]', '', part) for part in parts]
            stripped_parts = [re.sub(r'\[.*$', '', part) for part in parts]
            stripped_parts = [re.sub(r'\^.*]', '', part) for part in parts]
            return ignore_patterns.sub(lambda m: m.group(0), ''.join(stripped_parts))
        # Remove Kivy markup tags for plain text operations, but preserve specified patterns
        text = re.sub(r'\[/?[a-zA-Z0-9_=,#.\-]+\]', '', text)
        # Then remove any partial markup tags (text starting with [)
        text = re.sub(r'\[.*$', '', text)
        text = re.sub(r'\^.*]', '', text)
        return text

    def _update_plaintext_lines(self) -> None:
        """Update the _lines_plaintext list with plain text versions of each line"""
        _text = self.text
        _lines = self._lines
        self._lines_plaintext = [self.strip_markup(line, ignore_patterns=self.ignore_patterns) for line in _lines]
        self._update_markup_to_plain_map()

    def _update_markup_to_plain_map(self):
        """Create a mapping between markup positions and plain text positions.
        Uses stored plaintext from tuples where available for more accurate mapping."""


        markup_index = [0]
        def _plain_index():
            return len(self._markup_to_plain_map) | 0

        plain_index = _plain_index()

        #plain_index = 0 # #1 Start at 0, increase on found markup characters
        in_markup = False
        idx = 0 # #1 Start enum at 1
        text = self.text
        plaintext = self.plaintext
        and_char = None
        # Start at current position in the text and plaintext, and work from there.
        if self._markup_to_plain_map:
            k = list(self._markup_to_plain_map.keys())[-1]
            idx = k[-1] + 1
            #plain_index = v
        for i, char in enumerate(text[idx:], idx):
            try:
                if char == '&':
                # If we're in an escaped character, skip the first 3 characters and only count the last. Catch index errors rather than checking everything.
                    and_char = text[i:i+3]
                    if and_char == '&br;' or and_char == '&bl;':
                        continue
                elif and_char is not None and char != ';':
                    continue
                elif and_char is not None and char == ';':
                    and_char = None              

                if char == '[' and plaintext[_plain_index()] != '[':
                    # Check if it's a '[' in the plaintext to see if it's markup or not.
                    if not in_markup:
                        markup_index = [i]
                        in_markup = True
                    else:
                        # If we're already in a markup tag, add this position to the current tag
                        markup_index.append(i)
                elif char == ']' and in_markup and plaintext[_plain_index()] != ']':
                    # End of a markup tag...but wait theres more!
                    # Check if we're not at the end of the string before accessing text[i]
                    if i < len(text) and text[i] == '[':
                        markup_index.append(i)
                    # End of a markup tag
                    else:
                        # Map all positions in the markup tag to the same plain text position
                        markup_index.append(i)
                        self._markup_to_plain_map[tuple(markup_index)] = _plain_index()
                        in_markup = False
                elif not in_markup:
                    # Regular character outside of markup
                    self._markup_to_plain_map[tuple([i])] = _plain_index()
                else:
                    # Character inside a markup tag
                    markup_index.append(i)
            except IndexError:
                # If we hit an index error, just continue to the next character
                continue

    def _refresh_text(self, text, *largs):
        """Override to update plain text lines when text is refreshed"""
        # Check if our tokenizer made the lines empty.
        if text == '':
            return
        # For non-empty text call parent normally
        super(MarkupTextField, self)._refresh_text(text, *largs)
        #self._update_plaintext_lines()
        # Check if we should reset manual scroll flag after text refresh
        self._check_and_reset_manual_scroll()

    def _check_and_reset_manual_scroll(self):
        """Check if cursor is at/near the bottom and reset _manually_scrolled flag if so.
        
        This allows the viewport to follow the cursor again when the user scrolls
        back to the bottom or when the cursor is already at the bottom.
        """
        if not self._lines or not self._manually_scrolled:
            return
        
        # Calculate the visible viewport range
        dy = self.line_height + self.line_spacing
        if dy <= 0:
            return
            
        padding_top = self.padding[1]
        padding_bottom = self.padding[3]
        viewport_height = self.height - padding_top - padding_bottom - dy
        
        # Calculate max scroll position
        max_scroll_y = max(0, self.minimum_height - self.height)
        
        # Check if we're scrolled to the bottom (within a small buffer)
        # Buffer is 2 lines worth of scroll distance
        buffer = dy * 2
        is_at_bottom = self.scroll_y >= max_scroll_y - buffer
        
        # Check if cursor is at the end
        total_rows = len(self._lines)
        cr = self.cursor_row
        is_cursor_at_end = cr >= total_rows - 1
        
        # If scrolled to bottom and cursor is at end, reset the flag
        if is_at_bottom and is_cursor_at_end:
            self._manually_scrolled = False

    def on_cursor(self, instance, value):
        """Override to check and reset manual scroll flag when cursor moves."""
        super().on_cursor(instance, value)
        # Check if we should reset manual scroll flag after cursor movement
        self._check_and_reset_manual_scroll()

    def scroll_to_bottom(self, *args):
        """Scroll the viewport to the bottom and reset the manual scroll flag.
        
        This method can be called by a FAB button to return to following new text.
        """
        max_scroll_y = max(0, self.minimum_height - self.height)
        self.scroll_y = max_scroll_y
        self._manually_scrolled = False
        self._trigger_update_graphics()

    def _adjust_viewport(self, cc, cr):
        """Override to prevent viewport from following cursor when text is added programmatically.
        
        When text is added at the end (programmatically), the cursor moves there automatically.
        This prevents the viewport from scrolling to follow the cursor if the user has manually
        scrolled away from the bottom.
        """
        if not self._lines:
            return
        
        # Check if we should reset the manual scroll flag
        self._check_and_reset_manual_scroll()
        
        # If user hasn't manually scrolled, use normal viewport adjustment
        if not self._manually_scrolled:
            super()._adjust_viewport(cc, cr)
            return
        
        # User has manually scrolled - only adjust viewport if cursor is in visible area
        # Calculate the visible viewport range
        dy = self.line_height + self.line_spacing
        if dy <= 0:
            # Fallback to parent if line height is invalid
            super()._adjust_viewport(cc, cr)
            return
            
        padding_top = self.padding[1]
        padding_bottom = self.padding[3]
        viewport_height = self.height - padding_top - padding_bottom - dy
        
        # Calculate what row would be at the bottom of the visible viewport
        visible_bottom_row = int((self.scroll_y + viewport_height) / dy) if dy > 0 else 0
        visible_top_row = int(self.scroll_y / dy) if dy > 0 else 0
        
        # Only adjust viewport if cursor is within or near the visible area
        # This allows normal cursor following when user is actively editing
        if visible_top_row - 1 <= cr <= visible_bottom_row + 1:
            super()._adjust_viewport(cc, cr)
        # Otherwise, don't scroll - user is viewing elsewhere

    def _create_line_label(self, text, hint=False):
        '''Create a label from a text, using line options'''

        # increment until we find something that works - we know this doesn't work
        # so just fail it.
        if not self._is_color_tag(text) and text.find(u'\n') == 0:
            return super()._create_line_label(text, hint)
        
        ntext = text.replace(u'\n', u'').replace(u'\t', u' ' * self.tab_width)
        
        if self.password and not hint:  # Don't replace hint_text with *
            ntext = self.password_mask * len(ntext)

        ntext = self._get_bbcode(ntext)

        kw = self._get_line_options()

        cid = u'{}\0{}\0{}'.format(ntext, self.password, kw)
        texture = Cache_get('textinput.label', cid)
        if texture is None:
            # FIXME right now, we can't render very long line...
            # if we move on "VBO" version as fallback, we won't need to
            # do this. try to find the maximum text we can handle

            # TODO: God this is so fucking stupid, and won't work in some cases.
            # We're making a label and if it's too big we're trying again. Need to iterate
            # through markup tags and correctly match them up. Doing this fast is hard, but it does cache the label.
            # Make tuples of the patterns and a string for their end tag, match the pattern, get the end tag.

            label = Label(text=ntext, **kw)
            color_pattern = (re.compile(r'\[color=[0-9A-Fa-f]{6}\]'), r"[/color]")
            bold_pattern = (re.compile(r'\[b\]'), r"[/b]")
            italic_pattern = (re.compile(r'\[i\]'), r"[/i]")
            underline_pattern = (re.compile(r'\[u\]'), r"[/u]")
            end_pattern = re.compile(r'\[/.*\]')
            all_patterns = {"color": color_pattern, "bold": bold_pattern, "italic": italic_pattern, "underline": underline_pattern}
            start_tag = {"color": {}, "bold": {}, "italic": {}, "underline": {}}
            end_tag = {"color": {}, "bold": {}, "italic": {}, "underline": {}}
            markup_tags = label.markup
            if markup_tags:
                for i, tag in enumerate(markup_tags):
                    for mktype, pattern in all_patterns.items():
                        if re.match(pattern[0], tag):
                            start_tag[mktype][i] = (tag, pattern[1]) # Start tag at i index. Store the end in case we need it.
                            break
                        elif re.match(end_pattern, tag):
                            end_tag[mktype][i] = tag
                            break
                for mktype in all_patterns.keys():
                    if len(start_tag[mktype]) > len(end_tag[mktype]):
                        # more start tags than end tags, so we need to add the end tag from the last 
                        # start tag of this kind, and store the start tag for the next line
                        last_key = max(start_tag[mktype].keys())
                        ntext = u'{}{}'.format(ntext, start_tag[mktype][last_key][1])
                        self._saved_markup[mktype] = start_tag[mktype][last_key][0]
                    elif len(end_tag[mktype]) > len(start_tag[mktype]):
                        # more end tags than start tags, so we need to add the start tag we stored
                        ntext = u'{}{}'.format(self._saved_markup[mktype], ntext)
                        self._saved_markup[mktype] = ""
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
        # TODO: The mouse position vs cursor position is slightly off when selecting text.
        # Your mouse position is correct for where you want to start the selection, but the
        # graphics (viewable selection) isn't quite right.
        # python shenanigans here with typing...
        plain_text = ''
        if isinstance(text, tuple):
            markup_text, plain_text = text
            text = markup_text
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
            # Get the plaintext version
            if not plain_text:
                plain_text = self.strip_markup(text, ignore_patterns=self.ignore_patterns)
            # Create a label with the plaintext
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
        # Pattern for complete color tag pair
        color_pattern = re.compile(r'\[color=[0-9A-Fa-f]{6}\]')
        closing_pattern = re.compile(r'\[\/color\]')
        other_pattern = re.compile(r'\[/?(?:b|i|u)\]')
        all_patterns = [color_pattern, closing_pattern, other_pattern]
        return bool(any(re.search(pattern, text) for pattern in all_patterns))

    def _get_bbcode(self, ntext):
        # get bbcoded text for python
        # I think I may be doing this twice now...
        try:
            ntext[0]
            # replace brackets with special chars that aren't highlighted
            # by pygment. can't use &bl; ... cause & is highlighted
            #ntext = ntext.replace(u'[', u'\x01').replace(u']', u'\x02')
            #ntext = highlight(ntext, self.lexer, self.formatter)
            #ntext = ntext.replace(u'\x01', u'&bl;').replace(u'\x02', u'&br;')
            # replace special chars with &bl; and &br;
            color_pattern = re.compile(r'\[color=[0-9A-Fa-f]{6}\]')
            color_tag = self.current_color_tag if self.current_color_tag else f"[color={self.text_default_color}]"
            end_color_tag = '[/color]'
            if not re.match(color_pattern, ntext):
                if ntext.endswith(end_color_tag):
                    ntext = u''.join((color_tag, ntext))
                    self.current_color_tag = None
                else:
                    ntext = u''.join((color_tag, ntext, end_color_tag))
                    self.current_color_tag = None
            else:
                if not ntext.endswith(end_color_tag):
                    ntext = u''.join((ntext, end_color_tag))
                    self.current_color_tag = re.findall(color_pattern, ntext)
                    if self.current_color_tag:
                        try:
                            self.current_color_tag = self.current_color_tag[-1]
                        except IndexError:
                            self.current_color_tag = None
            #ntext = ntext.replace(u'\n', u'')
            # remove possible extra highlight options
            ntext = ntext.replace(u'[u]', '').replace(u'[/u]', '')
            return ntext
        except IndexError:
            return ''

    def _tokenize(self, text):
        """Override _tokenize to handle markup tags as single tokens.
        
        Markup tags like [color=FFFFFF] or [b] should be treated as single tokens
        and not split on brackets. This prevents word wrapping from breaking
        markup tags or splitting text that uses brackets like [Hint].
        """
        if text is None:
            return
        
        # For empty text, yield empty string to match parent behavior
        if not text:
            yield ''
            return
        
        delimiters = self._tokenize_delimiters
        
        # Find all markup tag positions in the text
        markup_ranges = []
        for match in self._markup_tag_pattern.finditer(text):
            markup_ranges.append((match.start(), match.end()))
        
        # If no markup tags, use parent's tokenization
        if not markup_ranges:
            for token in super()._tokenize(text):
                yield token
            return
        
        # Tokenize text, treating markup tags as single tokens
        old_index = 0
        prev_char = ''
        
        for markup_start, markup_end in markup_ranges:
            # Tokenize text before this markup tag using parent logic
            if old_index < markup_start:
                segment = text[old_index:markup_start]
                for token in self._tokenize_segment(segment, delimiters, prev_char):
                    yield token
                if segment:
                    prev_char = segment[-1]
            
            # Yield the entire markup tag as a single token
            yield text[markup_start:markup_end]
            old_index = markup_end
            prev_char = text[markup_end - 1] if markup_end > 0 else ''
        
        # Tokenize any remaining text after the last markup tag
        if old_index < len(text):
            segment = text[old_index:]
            for token in self._tokenize_segment(segment, delimiters, prev_char):
                yield token
    
    def _tokenize_segment(self, text_segment, delimiters, prev_char):
        """Helper method to tokenize a text segment using parent class logic."""
        if not text_segment:
            return
        
        old_index = 0
        for index, char in enumerate(text_segment):
            if char not in delimiters:
                if char != u'\n':
                    if index > 0 and (prev_char in delimiters):
                        if old_index < index:
                            yield text_segment[old_index:index]
                        old_index = index
                else:
                    if old_index < index:
                        yield text_segment[old_index:index]
                    yield text_segment[index:index + 1]
                    old_index = index + 1
            prev_char = char
        if old_index < len(text_segment):
            yield text_segment[old_index:]

    def cursor_offset(self):
        '''Get the cursor x offset on the current line'''
        row = int(self.cursor_row)
        col = int(self.cursor_col)
        lines = self._lines
        plaintext_lines = self._lines_plaintext
        offset = 0

        try:
            if col:
                # Get the text up to the cursor position
                markup_text = lines[row][:col]
                plain_text = plaintext_lines[row][:col]
                
                # Special handling for beginning of line
                if col == len(lines[row]):
                    # If at end of line, use the whole line
                    offset = self._get_text_width(text=(markup_text, plain_text), tab_width=self.tab_width, _label_cached=self._label_cached)
                else:
                    # Find the first ] in the line to determine where actual text starts
                    for pattern in self.all_patterns.values():
                        first_bracket_end = re.match(pattern, lines[row]).end()
                        break
                    if first_bracket_end >= 0 and col <= first_bracket_end:
                        # If cursor is before or at the first ], width should be 0
                        offset = 0
                    else:
                        # Use cached width calculation
                        offset = self._get_text_width(text=(markup_text, plain_text), tab_width=self.tab_width, _label_cached=self._label_cached)
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
        
        # For right-click, handle specially to prevent selection cancellation
        if touch.button == 'right' and self.collide_point(*touch.pos):
            touch.grab(self)
            self._touch_count += 1
            # Store selection state to preserve it
            self._right_click_selection_state = {
                'from': self._selection_from,
                'to': self._selection_to,
                'touch': self._selection_touch,
                'text': self.selection_text
            }
            return True

        if 'button' in touch.profile and touch.button.startswith('scroll'):
            if self.minimum_height - self.height < 0:
                return super().on_touch_down(touch)
            self._manually_scrolled = True
        # If the touch is a scroll button while the effect is running. Halt the effect.
            if self.effect_y.velocity > 0:
                self.effect_y.cancel() # this is .halt in the master branch of kivy

        # For all other touches, let the parent handle it
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Override to handle right-click menu"""
        if touch.grab_current is self and touch.button == 'right':
            touch.ungrab(self)
            self._touch_count -= 1
            win = EventLoop.window
            self._show_cut_copy_paste(position=touch.pos, touch=touch, win=win)
            # Restore selection state that was saved during on_touch_down
            if hasattr(self, '_right_click_selection_state'):
                state = self._right_click_selection_state
                self._selection_from = state['from']
                self._selection_to = state['to']
                self._selection_touch = state['touch']
                self._selection = (self._selection_from != self._selection_to)
                self._trigger_update_graphics()
                delattr(self, '_right_click_selection_state')
            return True
        # For right-click touches, don't call parent to prevent deselection
        if touch.button == 'right':
            return True
        if self.effect_y and self.effect_y.is_manual:
            # Stop tracking - pass unclamped scroll position for velocity calculation
            # The effect's history contains the scroll positions, so it can calculate velocity
            # Use unclamped position (which may be beyond bounds for momentum)
            final_scroll = self._unclamped_scroll_y if self._unclamped_scroll_y is not None else self.effect_y.value
            self.effect_y.stop(final_scroll)
            self._unclamped_scroll_y = None  # Reset for next scroll
        return super().on_touch_up(touch)

    def copy(self, data=''):
        """Override copy to use plain text for selection"""
        if not self.allow_copy:
            return
        if data:
            Clipboard.copy(unescape_markup(data))
        elif self.selection_text:
            Clipboard.copy(unescape_markup(self.selection_text))
        elif self.selection_previous:
            Clipboard.copy(unescape_markup(self.selection_previous))
        else:
            # If no selection, copy the current line in plain text
            row = int(self.cursor_row)
            if row < len(self._lines_plaintext):
                Clipboard.copy(unescape_markup(self._lines_plaintext[row]))

    def _update_selection(self, finished=False):
        '''Update selection text and order of from/to if finished is True.
        Can be called multiple times until finished is True.
        '''
        # Get the selection range in markup text
        a, b = int(self._selection_from), int(self._selection_to)
        # Store the original direction
        selection_reversed = a > b
        # reorder the selection if it's reversed
        if selection_reversed:
            a, b = b, a
            
        self._selection_finished = finished

        # Map the selection indices to the plaintext
        plain_a = self._get_plain_from_markup_index(a) + 1
        plain_b = self._get_plain_from_markup_index(b) + 1
  
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
        for i, line in enumerate(lines[:row], 1):
            if lines_flags[i] & FL_IS_NEWLINE:
                position += len(line) + 1
            else:
                position += len(line)
        
        # Add the column position
        position += col
        
        # Ensure we don't exceed the text length
        return min(position, len(self.text))
        
    def _select_word(self, delimiters=u' .,:;!?\'"<>(){}\n'):
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
        roloc_tluafed = self.text_default_color[::-1]
        no_color = False
        end = 0

        if col >= line_length:
            col = line_length - 1
        # look for a color markup tag first - if found, select the tag's contents
        for char in enil[-(col):]:
            if char == ']':
                start_tag = re.search(r"\][A-Fa-f0-9]{6}=roloc\[", enil[-(col):]) #search for the start tag...backwards
                #logger.debug(f"start_tag: {start_tag}")
                if start_tag and not start_tag.group(0) == (f']{roloc_tluafed}=roloc['):
                    start = start_tag.end()-flag
                    break
                else:
                    # if we find a tag that isn't a color tag, break
                    if re.search(r"\]", enil[-(col):]):
                        no_color=True
                        break
        if not no_color:
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
        
        if start==0 or end==0:
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
            if distance > 100:  # Adjust this threshold as needed
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

    def set_text(self, instance, text: str) -> None:
        """Fired when text is entered into a text field."""

        def set_text(*args):
            ntext = text.split('\n', 1)[1] if self.line_count > 1000 else text
            self.text = re.sub("\n", " ", ntext) if not self.multiline else ntext
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

    def scroll_text_from_swipe(self, touch):
        _scroll_timeout = (touch.time_update - touch.time_start) * 1000
        self._scroll_distance_x += abs(touch.dx)
        self._scroll_distance_y += abs(touch.dy)
        if not self._have_scrolled:
            # To be considered a scroll, touch should travel more than
            # scroll_distance in less than the scroll_timeout since touch_down
            if not (
                _scroll_timeout <= self.scroll_timeout
                and (
                    (self._scroll_distance_x >= self.scroll_distance)
                    or (self._scroll_distance_y >= self.scroll_distance)
                )
            ):
                # Distance isn't enough (yet) to consider it as a scroll
                if _scroll_timeout <= self.scroll_timeout:
                    # Timeout is not reached, scroll is still enabled.
                    return False
                else:
                    self._enable_scroll = False
                    self._cancel_update_selection(self._touch_down)
                    return False
            # We have a scroll!
            self._have_scrolled = True

        self.cancel_long_touch_event()

        if self.multiline:
            # Vertical scrolling
            if self.minimum_height - self.height < 0:
                return True

            if self.effect_y and not self.effect_y.is_manual:
                self._manually_scrolled = True
                # Starting a new scroll - initialize effect for velocity tracking
                self._update_effect_y_bounds()
                # Track unclamped scroll position for velocity calculation
                self._unclamped_scroll_y = self.scroll_y
                # Effect history tracks scroll position values for velocity calculation
                self.effect_y.value = self.scroll_y
                self.effect_y.start(self.scroll_y)
            
            # During manual scrolling, update scroll_y directly to follow the mouse
            # Also update effect history so it can calculate velocity when touch ends
            if self.effect_y and self.effect_y.is_manual:
                # Calculate scroll delta with speed factor
                scroll_delta = touch.dy * self.scroll_velocity
                max_scroll_y = max(0, self.minimum_height - self.height)
                
                # Update unclamped scroll position (for velocity calculation)
                if self._unclamped_scroll_y is None:
                    self._unclamped_scroll_y = self.scroll_y
                self._unclamped_scroll_y += scroll_delta
                
                # Update scroll_y directly - clamp to bounds so it follows mouse within limits
                # touch.dy is positive when dragging down, scroll_y increases when dragging down
                self.scroll_y = min(
                    max(0, self._unclamped_scroll_y),
                    max_scroll_y
                )
                
                # Update effect history with unclamped scroll position for velocity calculation
                # This allows proper velocity calculation even when mouse goes beyond widget bounds
                self.effect_y.value = self._unclamped_scroll_y
                self.effect_y.update(self._unclamped_scroll_y)
        else:
            max_scroll_x = self.get_max_scroll_x()
            self.scroll_x = min(
                max(0, self.scroll_x - touch.dx),
                max_scroll_x
            )

        self._trigger_update_graphics()
        self._position_handles()
        return True

    def _update_effect_y_bounds(self, *args):
        if not self.effect_y:
            return
        # Both scroll_y and effect_y use pixel-based coordinates
        # Direct assignment since coordinate systems match
        self.effect_y.min = 0
        max_scroll = max(0, self.minimum_height - self.height)
        self.effect_y.max = max_scroll
        # Set current value to current scroll position
        self.effect_y.value = self.scroll_y

    def _update_effect_y(self, *args):
        if not self.effect_y:
            return
        if not self.effect_y.is_manual:
            # During momentum scrolling (after touch ends)
            # effect_y.scroll is the computed scroll position (pixel-based)
            # Clamp to bounds and apply directly
            max_scroll = max(0, self.minimum_height - self.height)
            self.scroll_y = max(0, min(self.effect_y.scroll, max_scroll))
        # During manual scrolling, scroll_y is updated directly in scroll_text_from_swipe
        self._trigger_update_graphics()
        self._position_handles()
