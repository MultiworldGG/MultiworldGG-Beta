from enum import IntFlag

import comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 as __wrapper_module__
from comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 import (
    ANNO_THIS, IAccessibleHandler, IAccIdentity, CAccPropServices,
    BSTR, dispid, _lcid, ANNO_CONTAINER, IDispatch, IAccPropServer,
    _check_version, VARIANT, _RemotableHandle, GUID, CoClass,
    wireHMENU, IAccessible, HRESULT, COMMETHOD, wireHWND, WSTRING,
    Library, typelib_path, IAccPropServices, __MIDL_IWinTypes_0009
)


class AnnoScope(IntFlag):
    ANNO_THIS = 0
    ANNO_CONTAINER = 1


__all__ = [
    'wireHMENU', 'IAccessible', 'ANNO_THIS', '__MIDL_IWinTypes_0009',
    'IAccessibleHandler', 'IAccIdentity', 'AnnoScope',
    'ANNO_CONTAINER', 'Library', 'IAccPropServer', 'typelib_path',
    'IAccPropServices', '_RemotableHandle', 'CAccPropServices'
]

