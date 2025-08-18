from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    Checked, FONTNAME, VARIANT_BOOL, OLE_XPOS_CONTAINER, DISPMETHOD,
    DISPPROPERTY, Gray, CoClass, FONTSTRIKETHROUGH, _check_version,
    IPicture, IFontEventsDisp, IDispatch, FONTUNDERSCORE, FONTITALIC,
    IFontDisp, OLE_XSIZE_CONTAINER, OLE_XPOS_PIXELS, Picture, IFont,
    Monochrome, VgaColor, Unchecked, IPictureDisp, OLE_YSIZE_HIMETRIC,
    OLE_XPOS_HIMETRIC, Font, typelib_path, COMMETHOD, Default,
    HRESULT, OLE_HANDLE, FontEvents, FONTSIZE, IUnknown, OLE_COLOR,
    IEnumVARIANT, dispid, OLE_ENABLEDEFAULTBOOL, DISPPARAMS, _lcid,
    StdPicture, OLE_YPOS_PIXELS, OLE_YPOS_CONTAINER,
    OLE_YPOS_HIMETRIC, BSTR, StdFont, OLE_OPTEXCLUSIVE, GUID,
    OLE_XSIZE_PIXELS, OLE_CANCELBOOL, FONTBOLD, Library, Color,
    OLE_YSIZE_PIXELS, OLE_XSIZE_HIMETRIC, OLE_YSIZE_CONTAINER,
    EXCEPINFO
)


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


__all__ = [
    'FontEvents', 'Checked', 'FONTNAME', 'FONTSIZE', 'OLE_COLOR',
    'OLE_XPOS_CONTAINER', 'OLE_ENABLEDEFAULTBOOL', 'Gray',
    'FONTSTRIKETHROUGH', 'StdPicture', 'OLE_YPOS_PIXELS',
    'OLE_YPOS_CONTAINER', 'IPicture', 'IFontEventsDisp',
    'OLE_YPOS_HIMETRIC', 'FONTUNDERSCORE', 'FONTITALIC', 'StdFont',
    'OLE_OPTEXCLUSIVE', 'OLE_XSIZE_PIXELS', 'IFontDisp',
    'OLE_CANCELBOOL', 'FONTBOLD', 'OLE_XSIZE_CONTAINER',
    'OLE_XPOS_PIXELS', 'Picture', 'OLE_TRISTATE', 'IFont', 'Library',
    'Monochrome', 'VgaColor', 'Unchecked', 'Color', 'IPictureDisp',
    'OLE_YSIZE_HIMETRIC', 'OLE_XPOS_HIMETRIC', 'Font',
    'OLE_YSIZE_PIXELS', 'typelib_path', 'OLE_XSIZE_HIMETRIC',
    'LoadPictureConstants', 'OLE_YSIZE_CONTAINER', 'Default',
    'OLE_HANDLE'
]

