from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    OLE_YSIZE_HIMETRIC, Monochrome, OLE_XPOS_HIMETRIC, Color,
    IPictureDisp, BSTR, IDispatch, Default, IFontEventsDisp,
    OLE_YPOS_CONTAINER, FONTSIZE, Checked, COMMETHOD, OLE_CANCELBOOL,
    IFont, DISPPROPERTY, typelib_path, IFontDisp,
    OLE_ENABLEDEFAULTBOOL, OLE_OPTEXCLUSIVE, StdPicture,
    FONTSTRIKETHROUGH, _lcid, OLE_XSIZE_PIXELS, Gray, _check_version,
    FONTNAME, Unchecked, Picture, CoClass, DISPPARAMS,
    OLE_XSIZE_CONTAINER, OLE_YPOS_PIXELS, OLE_XPOS_CONTAINER,
    FONTUNDERSCORE, OLE_YSIZE_CONTAINER, dispid, EXCEPINFO, OLE_COLOR,
    GUID, HRESULT, IEnumVARIANT, FONTITALIC, StdFont,
    OLE_YPOS_HIMETRIC, DISPMETHOD, OLE_XSIZE_HIMETRIC, IUnknown, Font,
    OLE_YSIZE_PIXELS, OLE_HANDLE, FONTBOLD, FontEvents,
    OLE_XPOS_PIXELS, VgaColor, IPicture, Library, VARIANT_BOOL
)


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


__all__ = [
    'OLE_YSIZE_HIMETRIC', 'Monochrome', 'OLE_XPOS_HIMETRIC', 'Color',
    'IPictureDisp', 'Default', 'IFontEventsDisp',
    'OLE_YPOS_CONTAINER', 'FONTSIZE', 'OLE_COLOR', 'Checked',
    'OLE_CANCELBOOL', 'IFont', 'FONTITALIC', 'StdFont',
    'typelib_path', 'OLE_TRISTATE', 'OLE_YPOS_HIMETRIC',
    'OLE_XSIZE_HIMETRIC', 'IFontDisp', 'OLE_ENABLEDEFAULTBOOL',
    'OLE_OPTEXCLUSIVE', 'StdPicture', 'FONTSTRIKETHROUGH', 'Font',
    'OLE_YSIZE_PIXELS', 'LoadPictureConstants', 'OLE_XSIZE_PIXELS',
    'Gray', 'OLE_HANDLE', 'FONTBOLD', 'Unchecked', 'FONTNAME',
    'Picture', 'FontEvents', 'OLE_XPOS_PIXELS', 'VgaColor',
    'OLE_XSIZE_CONTAINER', 'OLE_YPOS_PIXELS', 'OLE_XPOS_CONTAINER',
    'FONTUNDERSCORE', 'IPicture', 'Library', 'OLE_YSIZE_CONTAINER'
]

