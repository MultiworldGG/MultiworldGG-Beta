# -*- coding: mbcs -*-

from ctypes import *
from comtypes import (
    _check_version, BSTR, CoClass, COMMETHOD, dispid, GUID, wireHWND
)
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes.automation import IDispatch, VARIANT
from ctypes import HRESULT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comtypes import hints


_lcid = 0  # change this if required
typelib_path = 'C:\\Windows\\System32\\oleacc.dll'
WSTRING = c_wchar_p

# values for enumeration 'AnnoScope'
ANNO_THIS = 0
ANNO_CONTAINER = 1
AnnoScope = c_int  # enum



class CAccPropServices(CoClass):
    _reg_clsid_ = GUID('{B5F8350B-0548-48B1-A6EE-88BD00B4A5E7}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{1EA4DBF0-3C3B-11CF-810C-00AA00389B71}', 1, 1)


class IAccPropServices(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6E26E776-04F0-495D-80E4-3330352E3169}')
    _idlflags_ = []

    if TYPE_CHECKING:  # commembers
        def SetPropValue(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete, idProp: hints.Incomplete, var: hints.Incomplete) -> hints.Hresult: ...
        def SetPropServer(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete, pServer: hints.Incomplete, AnnoScope: hints.Incomplete) -> hints.Hresult: ...
        def ClearProps(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete) -> hints.Hresult: ...
        def SetHwndProp(self, hwnd: hints.Incomplete, idObject: hints.Incomplete, idChild: hints.Incomplete, idProp: hints.Incomplete, var: hints.Incomplete) -> hints.Hresult: ...
        def SetHwndPropStr(self, hwnd: hints.Incomplete, idObject: hints.Incomplete, idChild: hints.Incomplete, idProp: hints.Incomplete, str: hints.Incomplete) -> hints.Hresult: ...
        def SetHwndPropServer(self, hwnd: hints.Incomplete, idObject: hints.Incomplete, idChild: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete, pServer: hints.Incomplete, AnnoScope: hints.Incomplete) -> hints.Hresult: ...
        def ClearHwndProps(self, hwnd: hints.Incomplete, idObject: hints.Incomplete, idChild: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete) -> hints.Hresult: ...
        def ComposeHwndIdentityString(self, hwnd: hints.Incomplete, idObject: hints.Incomplete, idChild: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...
        def DecomposeHwndIdentityString(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete, hints.Incomplete]: ...
        def SetHmenuProp(self, hmenu: hints.Incomplete, idChild: hints.Incomplete, idProp: hints.Incomplete, var: hints.Incomplete) -> hints.Hresult: ...
        def SetHmenuPropStr(self, hmenu: hints.Incomplete, idChild: hints.Incomplete, idProp: hints.Incomplete, str: hints.Incomplete) -> hints.Hresult: ...
        def SetHmenuPropServer(self, hmenu: hints.Incomplete, idChild: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete, pServer: hints.Incomplete, AnnoScope: hints.Incomplete) -> hints.Hresult: ...
        def ClearHmenuProps(self, hmenu: hints.Incomplete, idChild: hints.Incomplete, paProps: hints.Incomplete, cProps: hints.Incomplete) -> hints.Hresult: ...
        def ComposeHmenuIdentityString(self, hmenu: hints.Incomplete, idChild: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...
        def DecomposeHmenuIdentityString(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...


CAccPropServices._com_interfaces_ = [IAccPropServices]


class IAccessible(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{618736E0-3C3D-11CF-810C-00AA00389B71}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_accParent(self) -> hints.Incomplete: ...
        accParent = hints.normal_property(_get_accParent)
        def _get_accChildCount(self) -> hints.Incomplete: ...
        accChildCount = hints.normal_property(_get_accChildCount)
        def _get_accChild(self, varChild: hints.Incomplete) -> hints.Incomplete: ...
        accChild = hints.named_property('accChild', _get_accChild)
        def _get_accName(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        def _set_accName(self, varChild: hints.Incomplete = ..., **kwargs: hints.Any) -> hints.Hresult: ...
        accName = hints.named_property('accName', _get_accName, _set_accName)
        def _get_accValue(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        def _set_accValue(self, varChild: hints.Incomplete = ..., **kwargs: hints.Any) -> hints.Hresult: ...
        accValue = hints.named_property('accValue', _get_accValue, _set_accValue)
        def _get_accDescription(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accDescription = hints.named_property('accDescription', _get_accDescription)
        def _get_accRole(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accRole = hints.named_property('accRole', _get_accRole)
        def _get_accState(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accState = hints.named_property('accState', _get_accState)
        def _get_accHelp(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accHelp = hints.named_property('accHelp', _get_accHelp)
        def _get_accHelpTopic(self, varChild: hints.Incomplete = ...) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...
        accHelpTopic = hints.named_property('accHelpTopic', _get_accHelpTopic)
        def _get_accKeyboardShortcut(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accKeyboardShortcut = hints.named_property('accKeyboardShortcut', _get_accKeyboardShortcut)
        def _get_accFocus(self) -> hints.Incomplete: ...
        accFocus = hints.normal_property(_get_accFocus)
        def _get_accSelection(self) -> hints.Incomplete: ...
        accSelection = hints.normal_property(_get_accSelection)
        def _get_accDefaultAction(self, varChild: hints.Incomplete = ...) -> hints.Incomplete: ...
        accDefaultAction = hints.named_property('accDefaultAction', _get_accDefaultAction)
        def accSelect(self, flagsSelect: hints.Incomplete, varChild: hints.Incomplete = ...) -> hints.Hresult: ...
        def accLocation(self, varChild: hints.Incomplete = ...) -> hints.Tuple[hints.Incomplete, hints.Incomplete, hints.Incomplete, hints.Incomplete]: ...
        def accNavigate(self, navDir: hints.Incomplete, varStart: hints.Incomplete = ...) -> hints.Incomplete: ...
        def accHitTest(self, xLeft: hints.Incomplete, yTop: hints.Incomplete) -> hints.Incomplete: ...
        def accDoDefaultAction(self, varChild: hints.Incomplete = ...) -> hints.Hresult: ...


IAccessible._methods_ = [
    COMMETHOD(
        [dispid(-5000), 'hidden', 'propget'],
        HRESULT,
        'accParent',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppdispParent')
    ),
    COMMETHOD(
        [dispid(-5001), 'hidden', 'propget'],
        HRESULT,
        'accChildCount',
        (['out', 'retval'], POINTER(c_int), 'pcountChildren')
    ),
    COMMETHOD(
        [dispid(-5002), 'hidden', 'propget'],
        HRESULT,
        'accChild',
        (['in'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppdispChild')
    ),
    COMMETHOD(
        [dispid(-5003), 'hidden', 'propget'],
        HRESULT,
        'accName',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszName')
    ),
    COMMETHOD(
        [dispid(-5004), 'hidden', 'propget'],
        HRESULT,
        'accValue',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszValue')
    ),
    COMMETHOD(
        [dispid(-5005), 'hidden', 'propget'],
        HRESULT,
        'accDescription',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszDescription')
    ),
    COMMETHOD(
        [dispid(-5006), 'hidden', 'propget'],
        HRESULT,
        'accRole',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarRole')
    ),
    COMMETHOD(
        [dispid(-5007), 'hidden', 'propget'],
        HRESULT,
        'accState',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarState')
    ),
    COMMETHOD(
        [dispid(-5008), 'hidden', 'propget'],
        HRESULT,
        'accHelp',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszHelp')
    ),
    COMMETHOD(
        [dispid(-5009), 'hidden', 'propget'],
        HRESULT,
        'accHelpTopic',
        (['out'], POINTER(BSTR), 'pszHelpFile'),
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(c_int), 'pidTopic')
    ),
    COMMETHOD(
        [dispid(-5010), 'hidden', 'propget'],
        HRESULT,
        'accKeyboardShortcut',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszKeyboardShortcut')
    ),
    COMMETHOD(
        [dispid(-5011), 'hidden', 'propget'],
        HRESULT,
        'accFocus',
        (['out', 'retval'], POINTER(VARIANT), 'pvarChild')
    ),
    COMMETHOD(
        [dispid(-5012), 'hidden', 'propget'],
        HRESULT,
        'accSelection',
        (['out', 'retval'], POINTER(VARIANT), 'pvarChildren')
    ),
    COMMETHOD(
        [dispid(-5013), 'hidden', 'propget'],
        HRESULT,
        'accDefaultAction',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['out', 'retval'], POINTER(BSTR), 'pszDefaultAction')
    ),
    COMMETHOD(
        [dispid(-5014), 'hidden'],
        HRESULT,
        'accSelect',
        (['in'], c_int, 'flagsSelect'),
        (['in', 'optional'], VARIANT, 'varChild')
    ),
    COMMETHOD(
        [dispid(-5015), 'hidden'],
        HRESULT,
        'accLocation',
        (['out'], POINTER(c_int), 'pxLeft'),
        (['out'], POINTER(c_int), 'pyTop'),
        (['out'], POINTER(c_int), 'pcxWidth'),
        (['out'], POINTER(c_int), 'pcyHeight'),
        (['in', 'optional'], VARIANT, 'varChild')
    ),
    COMMETHOD(
        [dispid(-5016), 'hidden'],
        HRESULT,
        'accNavigate',
        (['in'], c_int, 'navDir'),
        (['in', 'optional'], VARIANT, 'varStart'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarEndUpAt')
    ),
    COMMETHOD(
        [dispid(-5017), 'hidden'],
        HRESULT,
        'accHitTest',
        (['in'], c_int, 'xLeft'),
        (['in'], c_int, 'yTop'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarChild')
    ),
    COMMETHOD(
        [dispid(-5018), 'hidden'],
        HRESULT,
        'accDoDefaultAction',
        (['in', 'optional'], VARIANT, 'varChild')
    ),
    COMMETHOD(
        [dispid(-5003), 'hidden', 'propput'],
        HRESULT,
        'accName',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['in'], BSTR, 'pszName')
    ),
    COMMETHOD(
        [dispid(-5004), 'hidden', 'propput'],
        HRESULT,
        'accValue',
        (['in', 'optional'], VARIANT, 'varChild'),
        (['in'], BSTR, 'pszValue')
    ),
]

################################################################
# code template for IAccessible implementation
# class IAccessible_Impl(object):
#     @property
#     def accParent(self):
#         '-no docstring-'
#         #return ppdispParent
#
#     @property
#     def accChildCount(self):
#         '-no docstring-'
#         #return pcountChildren
#
#     @property
#     def accChild(self, varChild):
#         '-no docstring-'
#         #return ppdispChild
#
#     def _get(self, varChild):
#         '-no docstring-'
#         #return pszName
#     def _set(self, varChild, pszName):
#         '-no docstring-'
#     accName = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self, varChild):
#         '-no docstring-'
#         #return pszValue
#     def _set(self, varChild, pszValue):
#         '-no docstring-'
#     accValue = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def accDescription(self, varChild):
#         '-no docstring-'
#         #return pszDescription
#
#     @property
#     def accRole(self, varChild):
#         '-no docstring-'
#         #return pvarRole
#
#     @property
#     def accState(self, varChild):
#         '-no docstring-'
#         #return pvarState
#
#     @property
#     def accHelp(self, varChild):
#         '-no docstring-'
#         #return pszHelp
#
#     @property
#     def accHelpTopic(self, varChild):
#         '-no docstring-'
#         #return pszHelpFile, pidTopic
#
#     @property
#     def accKeyboardShortcut(self, varChild):
#         '-no docstring-'
#         #return pszKeyboardShortcut
#
#     @property
#     def accFocus(self):
#         '-no docstring-'
#         #return pvarChild
#
#     @property
#     def accSelection(self):
#         '-no docstring-'
#         #return pvarChildren
#
#     @property
#     def accDefaultAction(self, varChild):
#         '-no docstring-'
#         #return pszDefaultAction
#
#     def accSelect(self, flagsSelect, varChild):
#         '-no docstring-'
#         #return 
#
#     def accLocation(self, varChild):
#         '-no docstring-'
#         #return pxLeft, pyTop, pcxWidth, pcyHeight
#
#     def accNavigate(self, navDir, varStart):
#         '-no docstring-'
#         #return pvarEndUpAt
#
#     def accHitTest(self, xLeft, yTop):
#         '-no docstring-'
#         #return pvarChild
#
#     def accDoDefaultAction(self, varChild):
#         '-no docstring-'
#         #return 
#


class _RemotableHandle(Structure):
    pass


wireHMENU = POINTER(_RemotableHandle)


class Library(object):
    name = 'Accessibility'
    _reg_typelib_ = ('{1EA4DBF0-3C3B-11CF-810C-00AA00389B71}', 1, 1)


class IAccPropServer(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{76C0DBBB-15E0-4E7B-B61B-20EEEA2001E0}')
    _idlflags_ = []

    if TYPE_CHECKING:  # commembers
        def GetPropValue(self, pIDString: hints.Incomplete, dwIDStringLen: hints.Incomplete, idProp: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...


IAccPropServer._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'GetPropValue',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['out'], POINTER(VARIANT), 'pvarValue'),
        (['out'], POINTER(c_int), 'pfHasProp')
    ),
]

################################################################
# code template for IAccPropServer implementation
# class IAccPropServer_Impl(object):
#     def GetPropValue(self, pIDString, dwIDStringLen, idProp):
#         '-no docstring-'
#         #return pvarValue, pfHasProp
#


class __MIDL_IWinTypes_0009(Union):
    pass


__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]

assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)

_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]

assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)

IAccPropServices._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'SetPropValue',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['in'], VARIANT, 'var')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetPropServer',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps'),
        (['in'], POINTER(IAccPropServer), 'pServer'),
        (['in'], AnnoScope, 'AnnoScope')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ClearProps',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHwndProp',
        (['in'], wireHWND, 'hwnd'),
        (['in'], c_ulong, 'idObject'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['in'], VARIANT, 'var')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHwndPropStr',
        (['in'], wireHWND, 'hwnd'),
        (['in'], c_ulong, 'idObject'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['in'], WSTRING, 'str')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHwndPropServer',
        (['in'], wireHWND, 'hwnd'),
        (['in'], c_ulong, 'idObject'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps'),
        (['in'], POINTER(IAccPropServer), 'pServer'),
        (['in'], AnnoScope, 'AnnoScope')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ClearHwndProps',
        (['in'], wireHWND, 'hwnd'),
        (['in'], c_ulong, 'idObject'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ComposeHwndIdentityString',
        (['in'], wireHWND, 'hwnd'),
        (['in'], c_ulong, 'idObject'),
        (['in'], c_ulong, 'idChild'),
        (['out'], POINTER(POINTER(c_ubyte)), 'ppIDString'),
        (['out'], POINTER(c_ulong), 'pdwIDStringLen')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'DecomposeHwndIdentityString',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (['out'], POINTER(wireHWND), 'phwnd'),
        (['out'], POINTER(c_ulong), 'pidObject'),
        (['out'], POINTER(c_ulong), 'pidChild')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHmenuProp',
        (['in'], wireHMENU, 'hmenu'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['in'], VARIANT, 'var')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHmenuPropStr',
        (['in'], wireHMENU, 'hmenu'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID,
            'idProp',
        ),
        (['in'], WSTRING, 'str')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetHmenuPropServer',
        (['in'], wireHMENU, 'hmenu'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps'),
        (['in'], POINTER(IAccPropServer), 'pServer'),
        (['in'], AnnoScope, 'AnnoScope')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ClearHmenuProps',
        (['in'], wireHMENU, 'hmenu'),
        (['in'], c_ulong, 'idChild'),
        (
            ['in'],
            POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
            'paProps',
        ),
        (['in'], c_int, 'cProps')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ComposeHmenuIdentityString',
        (['in'], wireHMENU, 'hmenu'),
        (['in'], c_ulong, 'idChild'),
        (['out'], POINTER(POINTER(c_ubyte)), 'ppIDString'),
        (['out'], POINTER(c_ulong), 'pdwIDStringLen')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'DecomposeHmenuIdentityString',
        (['in'], POINTER(c_ubyte), 'pIDString'),
        (['in'], c_ulong, 'dwIDStringLen'),
        (['out'], POINTER(wireHMENU), 'phmenu'),
        (['out'], POINTER(c_ulong), 'pidChild')
    ),
]

################################################################
# code template for IAccPropServices implementation
# class IAccPropServices_Impl(object):
#     def SetPropValue(self, pIDString, dwIDStringLen, idProp, var):
#         '-no docstring-'
#         #return 
#
#     def SetPropServer(self, pIDString, dwIDStringLen, paProps, cProps, pServer, AnnoScope):
#         '-no docstring-'
#         #return 
#
#     def ClearProps(self, pIDString, dwIDStringLen, paProps, cProps):
#         '-no docstring-'
#         #return 
#
#     def SetHwndProp(self, hwnd, idObject, idChild, idProp, var):
#         '-no docstring-'
#         #return 
#
#     def SetHwndPropStr(self, hwnd, idObject, idChild, idProp, str):
#         '-no docstring-'
#         #return 
#
#     def SetHwndPropServer(self, hwnd, idObject, idChild, paProps, cProps, pServer, AnnoScope):
#         '-no docstring-'
#         #return 
#
#     def ClearHwndProps(self, hwnd, idObject, idChild, paProps, cProps):
#         '-no docstring-'
#         #return 
#
#     def ComposeHwndIdentityString(self, hwnd, idObject, idChild):
#         '-no docstring-'
#         #return ppIDString, pdwIDStringLen
#
#     def DecomposeHwndIdentityString(self, pIDString, dwIDStringLen):
#         '-no docstring-'
#         #return phwnd, pidObject, pidChild
#
#     def SetHmenuProp(self, hmenu, idChild, idProp, var):
#         '-no docstring-'
#         #return 
#
#     def SetHmenuPropStr(self, hmenu, idChild, idProp, str):
#         '-no docstring-'
#         #return 
#
#     def SetHmenuPropServer(self, hmenu, idChild, paProps, cProps, pServer, AnnoScope):
#         '-no docstring-'
#         #return 
#
#     def ClearHmenuProps(self, hmenu, idChild, paProps, cProps):
#         '-no docstring-'
#         #return 
#
#     def ComposeHmenuIdentityString(self, hmenu, idChild):
#         '-no docstring-'
#         #return ppIDString, pdwIDStringLen
#
#     def DecomposeHmenuIdentityString(self, pIDString, dwIDStringLen):
#         '-no docstring-'
#         #return phmenu, pidChild
#


class IAccessibleHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{03022430-ABC4-11D0-BDE2-00AA001A1953}')
    _idlflags_ = ['hidden', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def AccessibleObjectFromID(self, hwnd: hints.Incomplete, lObjectID: hints.Incomplete) -> 'IAccessible': ...


IAccessibleHandler._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'AccessibleObjectFromID',
        (['in'], c_int, 'hwnd'),
        (['in'], c_int, 'lObjectID'),
        (['out'], POINTER(POINTER(IAccessible)), 'pIAccessible')
    ),
]

################################################################
# code template for IAccessibleHandler implementation
# class IAccessibleHandler_Impl(object):
#     def AccessibleObjectFromID(self, hwnd, lObjectID):
#         '-no docstring-'
#         #return pIAccessible
#


class IAccIdentity(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{7852B78D-1CFD-41C1-A615-9C0C85960B5F}')
    _idlflags_ = []

    if TYPE_CHECKING:  # commembers
        def GetIdentityString(self, dwIDChild: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...


IAccIdentity._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'GetIdentityString',
        (['in'], c_ulong, 'dwIDChild'),
        (['out'], POINTER(POINTER(c_ubyte)), 'ppIDString'),
        (['out'], POINTER(c_ulong), 'pdwIDStringLen')
    ),
]

################################################################
# code template for IAccIdentity implementation
# class IAccIdentity_Impl(object):
#     def GetIdentityString(self, dwIDChild):
#         '-no docstring-'
#         #return ppIDString, pdwIDStringLen
#

__all__ = [
    'wireHMENU', 'IAccessible', 'ANNO_THIS', '__MIDL_IWinTypes_0009',
    'IAccessibleHandler', 'IAccIdentity', 'AnnoScope',
    'ANNO_CONTAINER', 'Library', 'IAccPropServer', 'typelib_path',
    'IAccPropServices', '_RemotableHandle', 'CAccPropServices'
]

_check_version('1.4.11', 1755040494.219348)

