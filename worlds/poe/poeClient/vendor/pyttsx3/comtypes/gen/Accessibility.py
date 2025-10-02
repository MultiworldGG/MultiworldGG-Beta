from enum import IntFlag

import comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 as __wrapper_module__
from comtypes.gen._1EA4DBF0_3C3B_11CF_810C_00AA00389B71_0_1_1 import (
    GUID, IAccessibleHandler, CoClass, IAccPropServer, HRESULT, BSTR,
    dispid, IAccIdentity, wireHWND, CAccPropServices, COMMETHOD,
    IAccessible, VARIANT, _check_version, typelib_path, ANNO_THIS,
    __MIDL_IWinTypes_0009, WSTRING, IAccPropServices,
    _RemotableHandle, ANNO_CONTAINER, IDispatch, _lcid, Library,
    wireHMENU
)


class AnnoScope(IntFlag):
    ANNO_THIS = 0
    ANNO_CONTAINER = 1


__all__ = [
    'IAccessible', 'IAccessibleHandler', 'AnnoScope',
    'IAccPropServer', 'typelib_path', 'ANNO_THIS',
    '__MIDL_IWinTypes_0009', 'IAccPropServices', '_RemotableHandle',
    'ANNO_CONTAINER', 'IAccIdentity', 'CAccPropServices', 'Library',
    'wireHMENU'
]

