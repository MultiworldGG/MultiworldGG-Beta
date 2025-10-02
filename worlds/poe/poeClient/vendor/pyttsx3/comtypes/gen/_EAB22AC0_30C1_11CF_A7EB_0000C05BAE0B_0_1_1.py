# -*- coding: mbcs -*-

from ctypes import *
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import (
    _check_version, BSTR, CoClass, COMMETHOD, dispid, DISPMETHOD,
    GUID, helpstring, IUnknown
)
from ctypes import HRESULT
from comtypes.automation import IDispatch, VARIANT
from ctypes.wintypes import VARIANT_BOOL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comtypes import hints


_lcid = 0  # change this if required
typelib_path = 'C:\\Windows\\System32\\ieframe.dll'

# values for enumeration 'OLECMDID'
OLECMDID_OPEN = 1
OLECMDID_NEW = 2
OLECMDID_SAVE = 3
OLECMDID_SAVEAS = 4
OLECMDID_SAVECOPYAS = 5
OLECMDID_PRINT = 6
OLECMDID_PRINTPREVIEW = 7
OLECMDID_PAGESETUP = 8
OLECMDID_SPELL = 9
OLECMDID_PROPERTIES = 10
OLECMDID_CUT = 11
OLECMDID_COPY = 12
OLECMDID_PASTE = 13
OLECMDID_PASTESPECIAL = 14
OLECMDID_UNDO = 15
OLECMDID_REDO = 16
OLECMDID_SELECTALL = 17
OLECMDID_CLEARSELECTION = 18
OLECMDID_ZOOM = 19
OLECMDID_GETZOOMRANGE = 20
OLECMDID_UPDATECOMMANDS = 21
OLECMDID_REFRESH = 22
OLECMDID_STOP = 23
OLECMDID_HIDETOOLBARS = 24
OLECMDID_SETPROGRESSMAX = 25
OLECMDID_SETPROGRESSPOS = 26
OLECMDID_SETPROGRESSTEXT = 27
OLECMDID_SETTITLE = 28
OLECMDID_SETDOWNLOADSTATE = 29
OLECMDID_STOPDOWNLOAD = 30
OLECMDID_ONTOOLBARACTIVATED = 31
OLECMDID_FIND = 32
OLECMDID_DELETE = 33
OLECMDID_HTTPEQUIV = 34
OLECMDID_HTTPEQUIV_DONE = 35
OLECMDID_ENABLE_INTERACTION = 36
OLECMDID_ONUNLOAD = 37
OLECMDID_PROPERTYBAG2 = 38
OLECMDID_PREREFRESH = 39
OLECMDID_SHOWSCRIPTERROR = 40
OLECMDID_SHOWMESSAGE = 41
OLECMDID_SHOWFIND = 42
OLECMDID_SHOWPAGESETUP = 43
OLECMDID_SHOWPRINT = 44
OLECMDID_CLOSE = 45
OLECMDID_ALLOWUILESSSAVEAS = 46
OLECMDID_DONTDOWNLOADCSS = 47
OLECMDID_UPDATEPAGESTATUS = 48
OLECMDID_PRINT2 = 49
OLECMDID_PRINTPREVIEW2 = 50
OLECMDID_SETPRINTTEMPLATE = 51
OLECMDID_GETPRINTTEMPLATE = 52
OLECMDID_PAGEACTIONBLOCKED = 55
OLECMDID_PAGEACTIONUIQUERY = 56
OLECMDID_FOCUSVIEWCONTROLS = 57
OLECMDID_FOCUSVIEWCONTROLSQUERY = 58
OLECMDID_SHOWPAGEACTIONMENU = 59
OLECMDID_ADDTRAVELENTRY = 60
OLECMDID_UPDATETRAVELENTRY = 61
OLECMDID_UPDATEBACKFORWARDSTATE = 62
OLECMDID_OPTICAL_ZOOM = 63
OLECMDID_OPTICAL_GETZOOMRANGE = 64
OLECMDID_WINDOWSTATECHANGED = 65
OLECMDID_ACTIVEXINSTALLSCOPE = 66
OLECMDID_UPDATETRAVELENTRY_DATARECOVERY = 67
OLECMDID_SHOWTASKDLG = 68
OLECMDID_POPSTATEEVENT = 69
OLECMDID_VIEWPORT_MODE = 70
OLECMDID_LAYOUT_VIEWPORT_WIDTH = 71
OLECMDID_VISUAL_VIEWPORT_EXCLUDE_BOTTOM = 72
OLECMDID_USER_OPTICAL_ZOOM = 73
OLECMDID_PAGEAVAILABLE = 74
OLECMDID_GETUSERSCALABLE = 75
OLECMDID_UPDATE_CARET = 76
OLECMDID_ENABLE_VISIBILITY = 77
OLECMDID_MEDIA_PLAYBACK = 78
OLECMDID_SETFAVICON = 79
OLECMDID_SET_HOST_FULLSCREENMODE = 80
OLECMDID_EXITFULLSCREEN = 81
OLECMDID_SCROLLCOMPLETE = 82
OLECMDID_ONBEFOREUNLOAD = 83
OLECMDID_SHOWMESSAGE_BLOCKABLE = 84
OLECMDID_SHOWTASKDLG_BLOCKABLE = 85
OLECMDID = c_int  # enum

# values for enumeration 'OLECMDF'
OLECMDF_SUPPORTED = 1
OLECMDF_ENABLED = 2
OLECMDF_LATCHED = 4
OLECMDF_NINCHED = 8
OLECMDF_INVISIBLE = 16
OLECMDF_DEFHIDEONCTXTMENU = 32
OLECMDF = c_int  # enum

# values for enumeration 'OLECMDEXECOPT'
OLECMDEXECOPT_DODEFAULT = 0
OLECMDEXECOPT_PROMPTUSER = 1
OLECMDEXECOPT_DONTPROMPTUSER = 2
OLECMDEXECOPT_SHOWHELP = 3
OLECMDEXECOPT = c_int  # enum

# values for enumeration 'tagREADYSTATE'
READYSTATE_UNINITIALIZED = 0
READYSTATE_LOADING = 1
READYSTATE_LOADED = 2
READYSTATE_INTERACTIVE = 3
READYSTATE_COMPLETE = 4
tagREADYSTATE = c_int  # enum

# values for enumeration 'SecureLockIconConstants'
secureLockIconUnsecure = 0
secureLockIconMixed = 1
secureLockIconSecureUnknownBits = 2
secureLockIconSecure40Bit = 3
secureLockIconSecure56Bit = 4
secureLockIconSecureFortezza = 5
secureLockIconSecure128Bit = 6
SecureLockIconConstants = c_int  # enum

# values for enumeration 'CommandStateChangeConstants'
CSC_UPDATECOMMANDS = -1
CSC_NAVIGATEFORWARD = 1
CSC_NAVIGATEBACK = 2
CommandStateChangeConstants = c_int  # enum

# values for enumeration 'ShellWindowFindWindowOptions'
SWFO_NEEDDISPATCH = 1
SWFO_INCLUDEPENDING = 2
SWFO_COOKIEPASSED = 4
ShellWindowFindWindowOptions = c_int  # enum

# values for enumeration 'ShellWindowTypeConstants'
SWC_EXPLORER = 0
SWC_BROWSER = 1
SWC_3RDPARTY = 2
SWC_CALLBACK = 4
SWC_DESKTOP = 8
ShellWindowTypeConstants = c_int  # enum

# values for enumeration 'NewProcessCauseConstants'
ProtectedModeRedirect = 1
NewProcessCauseConstants = c_int  # enum



class IShellUIHelper(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Shell UI Helper Control Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{729FE2F8-1EA8-11D1-8F85-00C04FC2FBE1}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def ResetFirstBootMode(self) -> hints.Hresult: ...
        def ResetSafeMode(self) -> hints.Hresult: ...
        def RefreshOfflineDesktop(self) -> hints.Hresult: ...
        def AddFavorite(self, URL: hints.Incomplete, Title: hints.Incomplete = ...) -> hints.Hresult: ...
        def AddChannel(self, URL: hints.Incomplete) -> hints.Hresult: ...
        def AddDesktopComponent(self, URL: hints.Incomplete, Type: hints.Incomplete, Left: hints.Incomplete = ..., Top: hints.Incomplete = ..., Width: hints.Incomplete = ..., Height: hints.Incomplete = ...) -> hints.Hresult: ...
        def IsSubscribed(self, URL: hints.Incomplete) -> hints.Incomplete: ...
        def NavigateAndFind(self, URL: hints.Incomplete, strQuery: hints.Incomplete, varTargetFrame: hints.Incomplete) -> hints.Hresult: ...
        def ImportExportFavorites(self, fImport: hints.Incomplete, strImpExpPath: hints.Incomplete) -> hints.Hresult: ...
        def AutoCompleteSaveForm(self, Form: hints.Incomplete = ...) -> hints.Hresult: ...
        def AutoScan(self, strSearch: hints.Incomplete, strFailureUrl: hints.Incomplete, pvarTargetFrame: hints.Incomplete = ...) -> hints.Hresult: ...
        def AutoCompleteAttach(self, Reserved: hints.Incomplete = ...) -> hints.Hresult: ...
        def ShowBrowserUI(self, bstrName: hints.Incomplete, pvarIn: hints.Incomplete) -> hints.Incomplete: ...


class IShellUIHelper2(IShellUIHelper):
    """Shell UI Helper Control Interface 2"""
    _case_insensitive_ = True
    _iid_ = GUID('{A7FE6EDA-1932-4281-B881-87B31B8BC52C}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def AddSearchProvider(self, URL: hints.Incomplete) -> hints.Hresult: ...
        def RunOnceShown(self) -> hints.Hresult: ...
        def SkipRunOnce(self) -> hints.Hresult: ...
        def CustomizeSettings(self, fSQM: hints.Incomplete, fPhishing: hints.Incomplete, bstrLocale: hints.Incomplete) -> hints.Hresult: ...
        def SqmEnabled(self) -> hints.Incomplete: ...
        def PhishingEnabled(self) -> hints.Incomplete: ...
        def BrandImageUri(self) -> hints.Incomplete: ...
        def SkipTabsWelcome(self) -> hints.Hresult: ...
        def DiagnoseConnection(self) -> hints.Hresult: ...
        def CustomizeClearType(self, fSet: hints.Incomplete) -> hints.Hresult: ...
        def IsSearchProviderInstalled(self, URL: hints.Incomplete) -> hints.Incomplete: ...
        def IsSearchMigrated(self) -> hints.Incomplete: ...
        def DefaultSearchProvider(self) -> hints.Incomplete: ...
        def RunOnceRequiredSettingsComplete(self, fComplete: hints.Incomplete) -> hints.Hresult: ...
        def RunOnceHasShown(self) -> hints.Incomplete: ...
        def SearchGuideUrl(self) -> hints.Incomplete: ...


class IShellUIHelper3(IShellUIHelper2):
    """Shell UI Helper Control Interface 3"""
    _case_insensitive_ = True
    _iid_ = GUID('{528DF2EC-D419-40BC-9B6D-DCDBF9C1B25D}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def AddService(self, URL: hints.Incomplete) -> hints.Hresult: ...
        def IsServiceInstalled(self, URL: hints.Incomplete, Verb: hints.Incomplete) -> hints.Incomplete: ...
        def InPrivateFilteringEnabled(self) -> hints.Incomplete: ...
        def AddToFavoritesBar(self, URL: hints.Incomplete, Title: hints.Incomplete, Type: hints.Incomplete = ...) -> hints.Hresult: ...
        def BuildNewTabPage(self) -> hints.Hresult: ...
        def SetRecentlyClosedVisible(self, fVisible: hints.Incomplete) -> hints.Hresult: ...
        def SetActivitiesVisible(self, fVisible: hints.Incomplete) -> hints.Hresult: ...
        def ContentDiscoveryReset(self) -> hints.Hresult: ...
        def IsSuggestedSitesEnabled(self) -> hints.Incomplete: ...
        def EnableSuggestedSites(self, fEnable: hints.Incomplete) -> hints.Hresult: ...
        def NavigateToSuggestedSites(self, bstrRelativeUrl: hints.Incomplete) -> hints.Hresult: ...
        def ShowTabsHelp(self) -> hints.Hresult: ...
        def ShowInPrivateHelp(self) -> hints.Hresult: ...


class IShellUIHelper4(IShellUIHelper3):
    """Shell UI Helper Control Interface 4"""
    _case_insensitive_ = True
    _iid_ = GUID('{B36E6A53-8073-499E-824C-D776330A333E}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def msIsSiteMode(self) -> hints.Incomplete: ...
        def msSiteModeShowThumbBar(self) -> hints.Hresult: ...
        def msSiteModeAddThumbBarButton(self, bstrIconURL: hints.Incomplete, bstrTooltip: hints.Incomplete) -> hints.Incomplete: ...
        def msSiteModeUpdateThumbBarButton(self, ButtonID: hints.Incomplete, fEnabled: hints.Incomplete, fVisible: hints.Incomplete) -> hints.Hresult: ...
        def msSiteModeSetIconOverlay(self, IconUrl: hints.Incomplete, pvarDescription: hints.Incomplete = ...) -> hints.Hresult: ...
        def msSiteModeClearIconOverlay(self) -> hints.Hresult: ...
        def msAddSiteMode(self) -> hints.Hresult: ...
        def msSiteModeCreateJumpList(self, bstrHeader: hints.Incomplete) -> hints.Hresult: ...
        def msSiteModeAddJumpListItem(self, bstrName: hints.Incomplete, bstrActionUri: hints.Incomplete, bstrIconUri: hints.Incomplete, pvarWindowType: hints.Incomplete = ...) -> hints.Hresult: ...
        def msSiteModeClearJumpList(self) -> hints.Hresult: ...
        def msSiteModeShowJumpList(self) -> hints.Hresult: ...
        def msSiteModeAddButtonStyle(self, uiButtonID: hints.Incomplete, bstrIconURL: hints.Incomplete, bstrTooltip: hints.Incomplete) -> hints.Incomplete: ...
        def msSiteModeShowButtonStyle(self, uiButtonID: hints.Incomplete, uiStyleID: hints.Incomplete) -> hints.Hresult: ...
        def msSiteModeActivate(self) -> hints.Hresult: ...
        def msIsSiteModeFirstRun(self, fPreserveState: hints.Incomplete) -> hints.Incomplete: ...
        def msAddTrackingProtectionList(self, URL: hints.Incomplete, bstrFilterName: hints.Incomplete) -> hints.Hresult: ...
        def msTrackingProtectionEnabled(self) -> hints.Incomplete: ...
        def msActiveXFilteringEnabled(self) -> hints.Incomplete: ...


class IShellUIHelper5(IShellUIHelper4):
    """Shell UI Helper Control Interface 5"""
    _case_insensitive_ = True
    _iid_ = GUID('{A2A08B09-103D-4D3F-B91C-EA455CA82EFA}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def msProvisionNetworks(self, bstrProvisioningXml: hints.Incomplete) -> hints.Incomplete: ...
        def msReportSafeUrl(self) -> hints.Hresult: ...
        def msSiteModeRefreshBadge(self) -> hints.Hresult: ...
        def msSiteModeClearBadge(self) -> hints.Hresult: ...
        def msDiagnoseConnectionUILess(self) -> hints.Hresult: ...
        def msLaunchNetworkClientHelp(self) -> hints.Hresult: ...
        def msChangeDefaultBrowser(self, fChange: hints.Incomplete) -> hints.Hresult: ...


class IShellUIHelper6(IShellUIHelper5):
    """Shell UI Helper Control Interface 6"""
    _case_insensitive_ = True
    _iid_ = GUID('{987A573E-46EE-4E89-96AB-DDF7F8FDC98C}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def msStopPeriodicTileUpdate(self) -> hints.Hresult: ...
        def msStartPeriodicTileUpdate(self, pollingUris: hints.Incomplete, startTime: hints.Incomplete = ..., uiUpdateRecurrence: hints.Incomplete = ...) -> hints.Hresult: ...
        def msStartPeriodicTileUpdateBatch(self, pollingUris: hints.Incomplete, startTime: hints.Incomplete = ..., uiUpdateRecurrence: hints.Incomplete = ...) -> hints.Hresult: ...
        def msClearTile(self) -> hints.Hresult: ...
        def msEnableTileNotificationQueue(self, fChange: hints.Incomplete) -> hints.Hresult: ...
        def msPinnedSiteState(self) -> hints.Incomplete: ...
        def msEnableTileNotificationQueueForSquare150x150(self, fChange: hints.Incomplete) -> hints.Hresult: ...
        def msEnableTileNotificationQueueForWide310x150(self, fChange: hints.Incomplete) -> hints.Hresult: ...
        def msEnableTileNotificationQueueForSquare310x310(self, fChange: hints.Incomplete) -> hints.Hresult: ...
        def msScheduledTileNotification(self, bstrNotificationXml: hints.Incomplete, bstrNotificationId: hints.Incomplete, bstrNotificationTag: hints.Incomplete, startTime: hints.Incomplete = ..., expirationTime: hints.Incomplete = ...) -> hints.Hresult: ...
        def msRemoveScheduledTileNotification(self, bstrNotificationId: hints.Incomplete) -> hints.Hresult: ...
        def msStartPeriodicBadgeUpdate(self, pollingUri: hints.Incomplete, startTime: hints.Incomplete = ..., uiUpdateRecurrence: hints.Incomplete = ...) -> hints.Hresult: ...
        def msStopPeriodicBadgeUpdate(self) -> hints.Hresult: ...
        def msLaunchInternetOptions(self) -> hints.Hresult: ...


class IShellUIHelper7(IShellUIHelper6):
    """Shell UI Helper Control Interface 7"""
    _case_insensitive_ = True
    _iid_ = GUID('{60E567C8-9573-4AB2-A264-637C6C161CB1}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def SetExperimentalFlag(self, bstrFlagString: hints.Incomplete, vfFlag: hints.Incomplete) -> hints.Hresult: ...
        def GetExperimentalFlag(self, bstrFlagString: hints.Incomplete) -> hints.Incomplete: ...
        def SetExperimentalValue(self, bstrValueString: hints.Incomplete, dwValue: hints.Incomplete) -> hints.Hresult: ...
        def GetExperimentalValue(self, bstrValueString: hints.Incomplete) -> hints.Incomplete: ...
        def ResetAllExperimentalFlagsAndValues(self) -> hints.Hresult: ...
        def GetNeedIEAutoLaunchFlag(self, bstrUrl: hints.Incomplete) -> hints.Incomplete: ...
        def SetNeedIEAutoLaunchFlag(self, bstrUrl: hints.Incomplete, flag: hints.Incomplete) -> hints.Hresult: ...
        def HasNeedIEAutoLaunchFlag(self, bstrUrl: hints.Incomplete) -> hints.Incomplete: ...
        def LaunchIE(self, bstrUrl: hints.Incomplete, automated: hints.Incomplete) -> hints.Hresult: ...


class IShellUIHelper8(IShellUIHelper7):
    """Shell UI Helper Control Interface 8"""
    _case_insensitive_ = True
    _iid_ = GUID('{66DEBCF2-05B0-4F07-B49B-B96241A65DB2}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def GetCVListData(self) -> hints.Incomplete: ...
        def GetCVListLocalData(self) -> hints.Incomplete: ...
        def GetEMIEListData(self) -> hints.Incomplete: ...
        def GetEMIEListLocalData(self) -> hints.Incomplete: ...
        def OpenFavoritesPane(self) -> hints.Hresult: ...
        def OpenFavoritesSettings(self) -> hints.Hresult: ...
        def LaunchInHVSI(self, bstrUrl: hints.Incomplete) -> hints.Hresult: ...


class IShellUIHelper9(IShellUIHelper8):
    """Shell UI Helper Control Interface 9"""
    _case_insensitive_ = True
    _iid_ = GUID('{6CDF73B0-7F2F-451F-BC0F-63E0F3284E54}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def GetOSSku(self) -> hints.Incomplete: ...


IShellUIHelper._methods_ = [
    COMMETHOD([dispid(1), 'hidden'], HRESULT, 'ResetFirstBootMode'),
    COMMETHOD([dispid(2), 'hidden'], HRESULT, 'ResetSafeMode'),
    COMMETHOD([dispid(3), 'hidden'], HRESULT, 'RefreshOfflineDesktop'),
    COMMETHOD(
        [dispid(4)],
        HRESULT,
        'AddFavorite',
        (['in'], BSTR, 'URL'),
        (['in', 'optional'], POINTER(VARIANT), 'Title')
    ),
    COMMETHOD(
        [dispid(5)],
        HRESULT,
        'AddChannel',
        (['in'], BSTR, 'URL')
    ),
    COMMETHOD(
        [dispid(6)],
        HRESULT,
        'AddDesktopComponent',
        (['in'], BSTR, 'URL'),
        (['in'], BSTR, 'Type'),
        (['in', 'optional'], POINTER(VARIANT), 'Left'),
        (['in', 'optional'], POINTER(VARIANT), 'Top'),
        (['in', 'optional'], POINTER(VARIANT), 'Width'),
        (['in', 'optional'], POINTER(VARIANT), 'Height')
    ),
    COMMETHOD(
        [dispid(7)],
        HRESULT,
        'IsSubscribed',
        (['in'], BSTR, 'URL'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(8)],
        HRESULT,
        'NavigateAndFind',
        (['in'], BSTR, 'URL'),
        (['in'], BSTR, 'strQuery'),
        (['in'], POINTER(VARIANT), 'varTargetFrame')
    ),
    COMMETHOD(
        [dispid(9)],
        HRESULT,
        'ImportExportFavorites',
        (['in'], VARIANT_BOOL, 'fImport'),
        (['in'], BSTR, 'strImpExpPath')
    ),
    COMMETHOD(
        [dispid(10)],
        HRESULT,
        'AutoCompleteSaveForm',
        (['in', 'optional'], POINTER(VARIANT), 'Form')
    ),
    COMMETHOD(
        [dispid(11)],
        HRESULT,
        'AutoScan',
        (['in'], BSTR, 'strSearch'),
        (['in'], BSTR, 'strFailureUrl'),
        (['in', 'optional'], POINTER(VARIANT), 'pvarTargetFrame')
    ),
    COMMETHOD(
        [dispid(12), 'hidden'],
        HRESULT,
        'AutoCompleteAttach',
        (['in', 'optional'], POINTER(VARIANT), 'Reserved')
    ),
    COMMETHOD(
        [dispid(13)],
        HRESULT,
        'ShowBrowserUI',
        (['in'], BSTR, 'bstrName'),
        (['in'], POINTER(VARIANT), 'pvarIn'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarOut')
    ),
]

################################################################
# code template for IShellUIHelper implementation
# class IShellUIHelper_Impl(object):
#     def ResetFirstBootMode(self):
#         '-no docstring-'
#         #return 
#
#     def ResetSafeMode(self):
#         '-no docstring-'
#         #return 
#
#     def RefreshOfflineDesktop(self):
#         '-no docstring-'
#         #return 
#
#     def AddFavorite(self, URL, Title):
#         '-no docstring-'
#         #return 
#
#     def AddChannel(self, URL):
#         '-no docstring-'
#         #return 
#
#     def AddDesktopComponent(self, URL, Type, Left, Top, Width, Height):
#         '-no docstring-'
#         #return 
#
#     def IsSubscribed(self, URL):
#         '-no docstring-'
#         #return pBool
#
#     def NavigateAndFind(self, URL, strQuery, varTargetFrame):
#         '-no docstring-'
#         #return 
#
#     def ImportExportFavorites(self, fImport, strImpExpPath):
#         '-no docstring-'
#         #return 
#
#     def AutoCompleteSaveForm(self, Form):
#         '-no docstring-'
#         #return 
#
#     def AutoScan(self, strSearch, strFailureUrl, pvarTargetFrame):
#         '-no docstring-'
#         #return 
#
#     def AutoCompleteAttach(self, Reserved):
#         '-no docstring-'
#         #return 
#
#     def ShowBrowserUI(self, bstrName, pvarIn):
#         '-no docstring-'
#         #return pvarOut
#

IShellUIHelper2._methods_ = [
    COMMETHOD(
        [dispid(14)],
        HRESULT,
        'AddSearchProvider',
        (['in'], BSTR, 'URL')
    ),
    COMMETHOD([dispid(15)], HRESULT, 'RunOnceShown'),
    COMMETHOD([dispid(16)], HRESULT, 'SkipRunOnce'),
    COMMETHOD(
        [dispid(17)],
        HRESULT,
        'CustomizeSettings',
        (['in'], VARIANT_BOOL, 'fSQM'),
        (['in'], VARIANT_BOOL, 'fPhishing'),
        (['in'], BSTR, 'bstrLocale')
    ),
    COMMETHOD(
        [dispid(18)],
        HRESULT,
        'SqmEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
    COMMETHOD(
        [dispid(19)],
        HRESULT,
        'PhishingEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
    COMMETHOD(
        [dispid(20)],
        HRESULT,
        'BrandImageUri',
        (['out', 'retval'], POINTER(BSTR), 'pbstrUri')
    ),
    COMMETHOD([dispid(21)], HRESULT, 'SkipTabsWelcome'),
    COMMETHOD([dispid(22)], HRESULT, 'DiagnoseConnection'),
    COMMETHOD(
        [dispid(23)],
        HRESULT,
        'CustomizeClearType',
        (['in'], VARIANT_BOOL, 'fSet')
    ),
    COMMETHOD(
        [dispid(24)],
        HRESULT,
        'IsSearchProviderInstalled',
        (['in'], BSTR, 'URL'),
        (['out', 'retval'], POINTER(c_ulong), 'pdwResult')
    ),
    COMMETHOD(
        [dispid(25)],
        HRESULT,
        'IsSearchMigrated',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfMigrated')
    ),
    COMMETHOD(
        [dispid(26)],
        HRESULT,
        'DefaultSearchProvider',
        (['out', 'retval'], POINTER(BSTR), 'pbstrName')
    ),
    COMMETHOD(
        [dispid(27)],
        HRESULT,
        'RunOnceRequiredSettingsComplete',
        (['in'], VARIANT_BOOL, 'fComplete')
    ),
    COMMETHOD(
        [dispid(28)],
        HRESULT,
        'RunOnceHasShown',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfShown')
    ),
    COMMETHOD(
        [dispid(29)],
        HRESULT,
        'SearchGuideUrl',
        (['out', 'retval'], POINTER(BSTR), 'pbstrUrl')
    ),
]

################################################################
# code template for IShellUIHelper2 implementation
# class IShellUIHelper2_Impl(object):
#     def AddSearchProvider(self, URL):
#         '-no docstring-'
#         #return 
#
#     def RunOnceShown(self):
#         '-no docstring-'
#         #return 
#
#     def SkipRunOnce(self):
#         '-no docstring-'
#         #return 
#
#     def CustomizeSettings(self, fSQM, fPhishing, bstrLocale):
#         '-no docstring-'
#         #return 
#
#     def SqmEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#
#     def PhishingEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#
#     def BrandImageUri(self):
#         '-no docstring-'
#         #return pbstrUri
#
#     def SkipTabsWelcome(self):
#         '-no docstring-'
#         #return 
#
#     def DiagnoseConnection(self):
#         '-no docstring-'
#         #return 
#
#     def CustomizeClearType(self, fSet):
#         '-no docstring-'
#         #return 
#
#     def IsSearchProviderInstalled(self, URL):
#         '-no docstring-'
#         #return pdwResult
#
#     def IsSearchMigrated(self):
#         '-no docstring-'
#         #return pfMigrated
#
#     def DefaultSearchProvider(self):
#         '-no docstring-'
#         #return pbstrName
#
#     def RunOnceRequiredSettingsComplete(self, fComplete):
#         '-no docstring-'
#         #return 
#
#     def RunOnceHasShown(self):
#         '-no docstring-'
#         #return pfShown
#
#     def SearchGuideUrl(self):
#         '-no docstring-'
#         #return pbstrUrl
#

IShellUIHelper3._methods_ = [
    COMMETHOD(
        [dispid(30)],
        HRESULT,
        'AddService',
        (['in'], BSTR, 'URL')
    ),
    COMMETHOD(
        [dispid(31)],
        HRESULT,
        'IsServiceInstalled',
        (['in'], BSTR, 'URL'),
        (['in'], BSTR, 'Verb'),
        (['out', 'retval'], POINTER(c_ulong), 'pdwResult')
    ),
    COMMETHOD(
        [dispid(37)],
        HRESULT,
        'InPrivateFilteringEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
    COMMETHOD(
        [dispid(32)],
        HRESULT,
        'AddToFavoritesBar',
        (['in'], BSTR, 'URL'),
        (['in'], BSTR, 'Title'),
        (['in', 'optional'], POINTER(VARIANT), 'Type')
    ),
    COMMETHOD([dispid(33)], HRESULT, 'BuildNewTabPage'),
    COMMETHOD(
        [dispid(34)],
        HRESULT,
        'SetRecentlyClosedVisible',
        (['in'], VARIANT_BOOL, 'fVisible')
    ),
    COMMETHOD(
        [dispid(35)],
        HRESULT,
        'SetActivitiesVisible',
        (['in'], VARIANT_BOOL, 'fVisible')
    ),
    COMMETHOD([dispid(36)], HRESULT, 'ContentDiscoveryReset'),
    COMMETHOD(
        [dispid(38)],
        HRESULT,
        'IsSuggestedSitesEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
    COMMETHOD(
        [dispid(39)],
        HRESULT,
        'EnableSuggestedSites',
        (['in'], VARIANT_BOOL, 'fEnable')
    ),
    COMMETHOD(
        [dispid(40)],
        HRESULT,
        'NavigateToSuggestedSites',
        (['in'], BSTR, 'bstrRelativeUrl')
    ),
    COMMETHOD([dispid(41)], HRESULT, 'ShowTabsHelp'),
    COMMETHOD([dispid(42)], HRESULT, 'ShowInPrivateHelp'),
]

################################################################
# code template for IShellUIHelper3 implementation
# class IShellUIHelper3_Impl(object):
#     def AddService(self, URL):
#         '-no docstring-'
#         #return 
#
#     def IsServiceInstalled(self, URL, Verb):
#         '-no docstring-'
#         #return pdwResult
#
#     def InPrivateFilteringEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#
#     def AddToFavoritesBar(self, URL, Title, Type):
#         '-no docstring-'
#         #return 
#
#     def BuildNewTabPage(self):
#         '-no docstring-'
#         #return 
#
#     def SetRecentlyClosedVisible(self, fVisible):
#         '-no docstring-'
#         #return 
#
#     def SetActivitiesVisible(self, fVisible):
#         '-no docstring-'
#         #return 
#
#     def ContentDiscoveryReset(self):
#         '-no docstring-'
#         #return 
#
#     def IsSuggestedSitesEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#
#     def EnableSuggestedSites(self, fEnable):
#         '-no docstring-'
#         #return 
#
#     def NavigateToSuggestedSites(self, bstrRelativeUrl):
#         '-no docstring-'
#         #return 
#
#     def ShowTabsHelp(self):
#         '-no docstring-'
#         #return 
#
#     def ShowInPrivateHelp(self):
#         '-no docstring-'
#         #return 
#

IShellUIHelper4._methods_ = [
    COMMETHOD(
        [dispid(43)],
        HRESULT,
        'msIsSiteMode',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfSiteMode')
    ),
    COMMETHOD([dispid(47)], HRESULT, 'msSiteModeShowThumbBar'),
    COMMETHOD(
        [dispid(48)],
        HRESULT,
        'msSiteModeAddThumbBarButton',
        (['in'], BSTR, 'bstrIconURL'),
        (['in'], BSTR, 'bstrTooltip'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarButtonID')
    ),
    COMMETHOD(
        [dispid(46)],
        HRESULT,
        'msSiteModeUpdateThumbBarButton',
        (['in'], VARIANT, 'ButtonID'),
        (['in'], VARIANT_BOOL, 'fEnabled'),
        (['in'], VARIANT_BOOL, 'fVisible')
    ),
    COMMETHOD(
        [dispid(44)],
        HRESULT,
        'msSiteModeSetIconOverlay',
        (['in'], BSTR, 'IconUrl'),
        (['in', 'optional'], POINTER(VARIANT), 'pvarDescription')
    ),
    COMMETHOD([dispid(45)], HRESULT, 'msSiteModeClearIconOverlay'),
    COMMETHOD([dispid(49)], HRESULT, 'msAddSiteMode'),
    COMMETHOD(
        [dispid(51)],
        HRESULT,
        'msSiteModeCreateJumpList',
        (['in'], BSTR, 'bstrHeader')
    ),
    COMMETHOD(
        [dispid(52)],
        HRESULT,
        'msSiteModeAddJumpListItem',
        (['in'], BSTR, 'bstrName'),
        (['in'], BSTR, 'bstrActionUri'),
        (['in'], BSTR, 'bstrIconUri'),
        (['in', 'optional'], POINTER(VARIANT), 'pvarWindowType')
    ),
    COMMETHOD([dispid(53)], HRESULT, 'msSiteModeClearJumpList'),
    COMMETHOD([dispid(56)], HRESULT, 'msSiteModeShowJumpList'),
    COMMETHOD(
        [dispid(54)],
        HRESULT,
        'msSiteModeAddButtonStyle',
        (['in'], VARIANT, 'uiButtonID'),
        (['in'], BSTR, 'bstrIconURL'),
        (['in'], BSTR, 'bstrTooltip'),
        (['out', 'retval'], POINTER(VARIANT), 'pvarStyleID')
    ),
    COMMETHOD(
        [dispid(55)],
        HRESULT,
        'msSiteModeShowButtonStyle',
        (['in'], VARIANT, 'uiButtonID'),
        (['in'], VARIANT, 'uiStyleID')
    ),
    COMMETHOD([dispid(58)], HRESULT, 'msSiteModeActivate'),
    COMMETHOD(
        [dispid(59)],
        HRESULT,
        'msIsSiteModeFirstRun',
        (['in'], VARIANT_BOOL, 'fPreserveState'),
        (['out', 'retval'], POINTER(VARIANT), 'puiFirstRun')
    ),
    COMMETHOD(
        [dispid(57)],
        HRESULT,
        'msAddTrackingProtectionList',
        (['in'], BSTR, 'URL'),
        (['in'], BSTR, 'bstrFilterName')
    ),
    COMMETHOD(
        [dispid(60)],
        HRESULT,
        'msTrackingProtectionEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
    COMMETHOD(
        [dispid(61)],
        HRESULT,
        'msActiveXFilteringEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pfEnabled')
    ),
]

################################################################
# code template for IShellUIHelper4 implementation
# class IShellUIHelper4_Impl(object):
#     def msIsSiteMode(self):
#         '-no docstring-'
#         #return pfSiteMode
#
#     def msSiteModeShowThumbBar(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeAddThumbBarButton(self, bstrIconURL, bstrTooltip):
#         '-no docstring-'
#         #return pvarButtonID
#
#     def msSiteModeUpdateThumbBarButton(self, ButtonID, fEnabled, fVisible):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeSetIconOverlay(self, IconUrl, pvarDescription):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeClearIconOverlay(self):
#         '-no docstring-'
#         #return 
#
#     def msAddSiteMode(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeCreateJumpList(self, bstrHeader):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeAddJumpListItem(self, bstrName, bstrActionUri, bstrIconUri, pvarWindowType):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeClearJumpList(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeShowJumpList(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeAddButtonStyle(self, uiButtonID, bstrIconURL, bstrTooltip):
#         '-no docstring-'
#         #return pvarStyleID
#
#     def msSiteModeShowButtonStyle(self, uiButtonID, uiStyleID):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeActivate(self):
#         '-no docstring-'
#         #return 
#
#     def msIsSiteModeFirstRun(self, fPreserveState):
#         '-no docstring-'
#         #return puiFirstRun
#
#     def msAddTrackingProtectionList(self, URL, bstrFilterName):
#         '-no docstring-'
#         #return 
#
#     def msTrackingProtectionEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#
#     def msActiveXFilteringEnabled(self):
#         '-no docstring-'
#         #return pfEnabled
#

IShellUIHelper5._methods_ = [
    COMMETHOD(
        [dispid(62)],
        HRESULT,
        'msProvisionNetworks',
        (['in'], BSTR, 'bstrProvisioningXml'),
        (['out', 'retval'], POINTER(VARIANT), 'puiResult')
    ),
    COMMETHOD([dispid(63)], HRESULT, 'msReportSafeUrl'),
    COMMETHOD([dispid(64)], HRESULT, 'msSiteModeRefreshBadge'),
    COMMETHOD([dispid(65)], HRESULT, 'msSiteModeClearBadge'),
    COMMETHOD([dispid(66)], HRESULT, 'msDiagnoseConnectionUILess'),
    COMMETHOD([dispid(67)], HRESULT, 'msLaunchNetworkClientHelp'),
    COMMETHOD(
        [dispid(68)],
        HRESULT,
        'msChangeDefaultBrowser',
        (['in'], VARIANT_BOOL, 'fChange')
    ),
]

################################################################
# code template for IShellUIHelper5 implementation
# class IShellUIHelper5_Impl(object):
#     def msProvisionNetworks(self, bstrProvisioningXml):
#         '-no docstring-'
#         #return puiResult
#
#     def msReportSafeUrl(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeRefreshBadge(self):
#         '-no docstring-'
#         #return 
#
#     def msSiteModeClearBadge(self):
#         '-no docstring-'
#         #return 
#
#     def msDiagnoseConnectionUILess(self):
#         '-no docstring-'
#         #return 
#
#     def msLaunchNetworkClientHelp(self):
#         '-no docstring-'
#         #return 
#
#     def msChangeDefaultBrowser(self, fChange):
#         '-no docstring-'
#         #return 
#

IShellUIHelper6._methods_ = [
    COMMETHOD([dispid(69)], HRESULT, 'msStopPeriodicTileUpdate'),
    COMMETHOD(
        [dispid(70)],
        HRESULT,
        'msStartPeriodicTileUpdate',
        (['in'], VARIANT, 'pollingUris'),
        (['in', 'optional'], VARIANT, 'startTime'),
        (['in', 'optional'], VARIANT, 'uiUpdateRecurrence')
    ),
    COMMETHOD(
        [dispid(75)],
        HRESULT,
        'msStartPeriodicTileUpdateBatch',
        (['in'], VARIANT, 'pollingUris'),
        (['in', 'optional'], VARIANT, 'startTime'),
        (['in', 'optional'], VARIANT, 'uiUpdateRecurrence')
    ),
    COMMETHOD([dispid(71)], HRESULT, 'msClearTile'),
    COMMETHOD(
        [dispid(72)],
        HRESULT,
        'msEnableTileNotificationQueue',
        (['in'], VARIANT_BOOL, 'fChange')
    ),
    COMMETHOD(
        [dispid(73)],
        HRESULT,
        'msPinnedSiteState',
        (['out', 'retval'], POINTER(VARIANT), 'pvarSiteState')
    ),
    COMMETHOD(
        [dispid(76)],
        HRESULT,
        'msEnableTileNotificationQueueForSquare150x150',
        (['in'], VARIANT_BOOL, 'fChange')
    ),
    COMMETHOD(
        [dispid(77)],
        HRESULT,
        'msEnableTileNotificationQueueForWide310x150',
        (['in'], VARIANT_BOOL, 'fChange')
    ),
    COMMETHOD(
        [dispid(78)],
        HRESULT,
        'msEnableTileNotificationQueueForSquare310x310',
        (['in'], VARIANT_BOOL, 'fChange')
    ),
    COMMETHOD(
        [dispid(79)],
        HRESULT,
        'msScheduledTileNotification',
        (['in'], BSTR, 'bstrNotificationXml'),
        (['in'], BSTR, 'bstrNotificationId'),
        (['in'], BSTR, 'bstrNotificationTag'),
        (['in', 'optional'], VARIANT, 'startTime'),
        (['in', 'optional'], VARIANT, 'expirationTime')
    ),
    COMMETHOD(
        [dispid(80)],
        HRESULT,
        'msRemoveScheduledTileNotification',
        (['in'], BSTR, 'bstrNotificationId')
    ),
    COMMETHOD(
        [dispid(81)],
        HRESULT,
        'msStartPeriodicBadgeUpdate',
        (['in'], BSTR, 'pollingUri'),
        (['in', 'optional'], VARIANT, 'startTime'),
        (['in', 'optional'], VARIANT, 'uiUpdateRecurrence')
    ),
    COMMETHOD([dispid(82)], HRESULT, 'msStopPeriodicBadgeUpdate'),
    COMMETHOD([dispid(74)], HRESULT, 'msLaunchInternetOptions'),
]

################################################################
# code template for IShellUIHelper6 implementation
# class IShellUIHelper6_Impl(object):
#     def msStopPeriodicTileUpdate(self):
#         '-no docstring-'
#         #return 
#
#     def msStartPeriodicTileUpdate(self, pollingUris, startTime, uiUpdateRecurrence):
#         '-no docstring-'
#         #return 
#
#     def msStartPeriodicTileUpdateBatch(self, pollingUris, startTime, uiUpdateRecurrence):
#         '-no docstring-'
#         #return 
#
#     def msClearTile(self):
#         '-no docstring-'
#         #return 
#
#     def msEnableTileNotificationQueue(self, fChange):
#         '-no docstring-'
#         #return 
#
#     def msPinnedSiteState(self):
#         '-no docstring-'
#         #return pvarSiteState
#
#     def msEnableTileNotificationQueueForSquare150x150(self, fChange):
#         '-no docstring-'
#         #return 
#
#     def msEnableTileNotificationQueueForWide310x150(self, fChange):
#         '-no docstring-'
#         #return 
#
#     def msEnableTileNotificationQueueForSquare310x310(self, fChange):
#         '-no docstring-'
#         #return 
#
#     def msScheduledTileNotification(self, bstrNotificationXml, bstrNotificationId, bstrNotificationTag, startTime, expirationTime):
#         '-no docstring-'
#         #return 
#
#     def msRemoveScheduledTileNotification(self, bstrNotificationId):
#         '-no docstring-'
#         #return 
#
#     def msStartPeriodicBadgeUpdate(self, pollingUri, startTime, uiUpdateRecurrence):
#         '-no docstring-'
#         #return 
#
#     def msStopPeriodicBadgeUpdate(self):
#         '-no docstring-'
#         #return 
#
#     def msLaunchInternetOptions(self):
#         '-no docstring-'
#         #return 
#

IShellUIHelper7._methods_ = [
    COMMETHOD(
        [dispid(85)],
        HRESULT,
        'SetExperimentalFlag',
        (['in'], BSTR, 'bstrFlagString'),
        (['in'], VARIANT_BOOL, 'vfFlag')
    ),
    COMMETHOD(
        [dispid(84)],
        HRESULT,
        'GetExperimentalFlag',
        (['in'], BSTR, 'bstrFlagString'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'vfFlag')
    ),
    COMMETHOD(
        [dispid(86)],
        HRESULT,
        'SetExperimentalValue',
        (['in'], BSTR, 'bstrValueString'),
        (['in'], c_ulong, 'dwValue')
    ),
    COMMETHOD(
        [dispid(87)],
        HRESULT,
        'GetExperimentalValue',
        (['in'], BSTR, 'bstrValueString'),
        (['out', 'retval'], POINTER(c_ulong), 'pdwValue')
    ),
    COMMETHOD([dispid(92)], HRESULT, 'ResetAllExperimentalFlagsAndValues'),
    COMMETHOD(
        [dispid(89)],
        HRESULT,
        'GetNeedIEAutoLaunchFlag',
        (['in'], BSTR, 'bstrUrl'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'flag')
    ),
    COMMETHOD(
        [dispid(90)],
        HRESULT,
        'SetNeedIEAutoLaunchFlag',
        (['in'], BSTR, 'bstrUrl'),
        (['in'], VARIANT_BOOL, 'flag')
    ),
    COMMETHOD(
        [dispid(88)],
        HRESULT,
        'HasNeedIEAutoLaunchFlag',
        (['in'], BSTR, 'bstrUrl'),
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'exists')
    ),
    COMMETHOD(
        [dispid(91)],
        HRESULT,
        'LaunchIE',
        (['in'], BSTR, 'bstrUrl'),
        (['in'], VARIANT_BOOL, 'automated')
    ),
]

################################################################
# code template for IShellUIHelper7 implementation
# class IShellUIHelper7_Impl(object):
#     def SetExperimentalFlag(self, bstrFlagString, vfFlag):
#         '-no docstring-'
#         #return 
#
#     def GetExperimentalFlag(self, bstrFlagString):
#         '-no docstring-'
#         #return vfFlag
#
#     def SetExperimentalValue(self, bstrValueString, dwValue):
#         '-no docstring-'
#         #return 
#
#     def GetExperimentalValue(self, bstrValueString):
#         '-no docstring-'
#         #return pdwValue
#
#     def ResetAllExperimentalFlagsAndValues(self):
#         '-no docstring-'
#         #return 
#
#     def GetNeedIEAutoLaunchFlag(self, bstrUrl):
#         '-no docstring-'
#         #return flag
#
#     def SetNeedIEAutoLaunchFlag(self, bstrUrl, flag):
#         '-no docstring-'
#         #return 
#
#     def HasNeedIEAutoLaunchFlag(self, bstrUrl):
#         '-no docstring-'
#         #return exists
#
#     def LaunchIE(self, bstrUrl, automated):
#         '-no docstring-'
#         #return 
#

IShellUIHelper8._methods_ = [
    COMMETHOD(
        [dispid(93)],
        HRESULT,
        'GetCVListData',
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(94)],
        HRESULT,
        'GetCVListLocalData',
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(95)],
        HRESULT,
        'GetEMIEListData',
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD(
        [dispid(96)],
        HRESULT,
        'GetEMIEListLocalData',
        (['out', 'retval'], POINTER(BSTR), 'pbstrResult')
    ),
    COMMETHOD([dispid(97)], HRESULT, 'OpenFavoritesPane'),
    COMMETHOD([dispid(98)], HRESULT, 'OpenFavoritesSettings'),
    COMMETHOD(
        [dispid(99)],
        HRESULT,
        'LaunchInHVSI',
        (['in'], BSTR, 'bstrUrl')
    ),
]

################################################################
# code template for IShellUIHelper8 implementation
# class IShellUIHelper8_Impl(object):
#     def GetCVListData(self):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetCVListLocalData(self):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetEMIEListData(self):
#         '-no docstring-'
#         #return pbstrResult
#
#     def GetEMIEListLocalData(self):
#         '-no docstring-'
#         #return pbstrResult
#
#     def OpenFavoritesPane(self):
#         '-no docstring-'
#         #return 
#
#     def OpenFavoritesSettings(self):
#         '-no docstring-'
#         #return 
#
#     def LaunchInHVSI(self, bstrUrl):
#         '-no docstring-'
#         #return 
#

IShellUIHelper9._methods_ = [
    COMMETHOD(
        [dispid(103)],
        HRESULT,
        'GetOSSku',
        (['out', 'retval'], POINTER(c_ulong), 'pdwResult')
    ),
]

################################################################
# code template for IShellUIHelper9 implementation
# class IShellUIHelper9_Impl(object):
#     def GetOSSku(self):
#         '-no docstring-'
#         #return pdwResult
#


class IWebBrowser(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Web Browser interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{EAB22AC1-30C1-11CF-A7EB-0000C05BAE0B}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def GoBack(self) -> hints.Hresult: ...
        def GoForward(self) -> hints.Hresult: ...
        def GoHome(self) -> hints.Hresult: ...
        def GoSearch(self) -> hints.Hresult: ...
        def Navigate(self, URL: hints.Incomplete, Flags: hints.Incomplete = ..., TargetFrameName: hints.Incomplete = ..., PostData: hints.Incomplete = ..., Headers: hints.Incomplete = ...) -> hints.Hresult: ...
        def Refresh(self) -> hints.Hresult: ...
        def Refresh2(self, Level: hints.Incomplete = ...) -> hints.Hresult: ...
        def Stop(self) -> hints.Hresult: ...
        def _get_Application(self) -> hints.Incomplete: ...
        Application = hints.normal_property(_get_Application)
        def _get_Parent(self) -> hints.Incomplete: ...
        Parent = hints.normal_property(_get_Parent)
        def _get_Container(self) -> hints.Incomplete: ...
        Container = hints.normal_property(_get_Container)
        def _get_Document(self) -> hints.Incomplete: ...
        Document = hints.normal_property(_get_Document)
        def _get_TopLevelContainer(self) -> hints.Incomplete: ...
        TopLevelContainer = hints.normal_property(_get_TopLevelContainer)
        def _get_Type(self) -> hints.Incomplete: ...
        Type = hints.normal_property(_get_Type)
        def _get_Left(self) -> hints.Incomplete: ...
        def _set_Left(self, pl: hints.Incomplete) -> hints.Hresult: ...
        Left = hints.normal_property(_get_Left, _set_Left)
        def _get_Top(self) -> hints.Incomplete: ...
        def _set_Top(self, pl: hints.Incomplete) -> hints.Hresult: ...
        Top = hints.normal_property(_get_Top, _set_Top)
        def _get_Width(self) -> hints.Incomplete: ...
        def _set_Width(self, pl: hints.Incomplete) -> hints.Hresult: ...
        Width = hints.normal_property(_get_Width, _set_Width)
        def _get_Height(self) -> hints.Incomplete: ...
        def _set_Height(self, pl: hints.Incomplete) -> hints.Hresult: ...
        Height = hints.normal_property(_get_Height, _set_Height)
        def _get_LocationName(self) -> hints.Incomplete: ...
        LocationName = hints.normal_property(_get_LocationName)
        def _get_LocationURL(self) -> hints.Incomplete: ...
        LocationURL = hints.normal_property(_get_LocationURL)
        def _get_Busy(self) -> hints.Incomplete: ...
        Busy = hints.normal_property(_get_Busy)


class IWebBrowserApp(IWebBrowser):
    """Web Browser Application Interface."""
    _case_insensitive_ = True
    _iid_ = GUID('{0002DF05-0000-0000-C000-000000000046}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def Quit(self) -> hints.Hresult: ...
        def ClientToWindow(self, pcx: hints.Incomplete, pcy: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...
        def PutProperty(self, Property: hints.Incomplete, vtValue: hints.Incomplete) -> hints.Hresult: ...
        def GetProperty(self, Property: hints.Incomplete) -> hints.Incomplete: ...
        def _get_Name(self) -> hints.Incomplete: ...
        Name = hints.normal_property(_get_Name)
        def _get_HWND(self) -> hints.Incomplete: ...
        HWND = hints.normal_property(_get_HWND)
        def _get_FullName(self) -> hints.Incomplete: ...
        FullName = hints.normal_property(_get_FullName)
        def _get_Path(self) -> hints.Incomplete: ...
        Path = hints.normal_property(_get_Path)
        def _get_Visible(self) -> hints.Incomplete: ...
        def _set_Visible(self, pBool: hints.Incomplete) -> hints.Hresult: ...
        Visible = hints.normal_property(_get_Visible, _set_Visible)
        def _get_StatusBar(self) -> hints.Incomplete: ...
        def _set_StatusBar(self, pBool: hints.Incomplete) -> hints.Hresult: ...
        StatusBar = hints.normal_property(_get_StatusBar, _set_StatusBar)
        def _get_StatusText(self) -> hints.Incomplete: ...
        def _set_StatusText(self, StatusText: hints.Incomplete) -> hints.Hresult: ...
        StatusText = hints.normal_property(_get_StatusText, _set_StatusText)
        def _get_ToolBar(self) -> hints.Incomplete: ...
        def _set_ToolBar(self, Value: hints.Incomplete) -> hints.Hresult: ...
        ToolBar = hints.normal_property(_get_ToolBar, _set_ToolBar)
        def _get_MenuBar(self) -> hints.Incomplete: ...
        def _set_MenuBar(self, Value: hints.Incomplete) -> hints.Hresult: ...
        MenuBar = hints.normal_property(_get_MenuBar, _set_MenuBar)
        def _get_FullScreen(self) -> hints.Incomplete: ...
        def _set_FullScreen(self, pbFullScreen: hints.Incomplete) -> hints.Hresult: ...
        FullScreen = hints.normal_property(_get_FullScreen, _set_FullScreen)


class IWebBrowser2(IWebBrowserApp):
    """Web Browser Interface for IE4."""
    _case_insensitive_ = True
    _iid_ = GUID('{D30C1661-CDAF-11D0-8A3E-00C04FC9E26E}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def Navigate2(self, URL: hints.Incomplete, Flags: hints.Incomplete = ..., TargetFrameName: hints.Incomplete = ..., PostData: hints.Incomplete = ..., Headers: hints.Incomplete = ...) -> hints.Hresult: ...
        def QueryStatusWB(self, cmdID: hints.Incomplete) -> hints.Incomplete: ...
        def ExecWB(self, cmdID: hints.Incomplete, cmdexecopt: hints.Incomplete, pvaIn: hints.Incomplete = ..., pvaOut: hints.Incomplete = ...) -> hints.Incomplete: ...
        def ShowBrowserBar(self, pvaClsid: hints.Incomplete, pvarShow: hints.Incomplete = ..., pvarSize: hints.Incomplete = ...) -> hints.Hresult: ...
        def _get_ReadyState(self) -> hints.Incomplete: ...
        ReadyState = hints.normal_property(_get_ReadyState)
        def _get_Offline(self) -> hints.Incomplete: ...
        def _set_Offline(self, pbOffline: hints.Incomplete) -> hints.Hresult: ...
        Offline = hints.normal_property(_get_Offline, _set_Offline)
        def _get_Silent(self) -> hints.Incomplete: ...
        def _set_Silent(self, pbSilent: hints.Incomplete) -> hints.Hresult: ...
        Silent = hints.normal_property(_get_Silent, _set_Silent)
        def _get_RegisterAsBrowser(self) -> hints.Incomplete: ...
        def _set_RegisterAsBrowser(self, pbRegister: hints.Incomplete) -> hints.Hresult: ...
        RegisterAsBrowser = hints.normal_property(_get_RegisterAsBrowser, _set_RegisterAsBrowser)
        def _get_RegisterAsDropTarget(self) -> hints.Incomplete: ...
        def _set_RegisterAsDropTarget(self, pbRegister: hints.Incomplete) -> hints.Hresult: ...
        RegisterAsDropTarget = hints.normal_property(_get_RegisterAsDropTarget, _set_RegisterAsDropTarget)
        def _get_TheaterMode(self) -> hints.Incomplete: ...
        def _set_TheaterMode(self, pbRegister: hints.Incomplete) -> hints.Hresult: ...
        TheaterMode = hints.normal_property(_get_TheaterMode, _set_TheaterMode)
        def _get_AddressBar(self) -> hints.Incomplete: ...
        def _set_AddressBar(self, Value: hints.Incomplete) -> hints.Hresult: ...
        AddressBar = hints.normal_property(_get_AddressBar, _set_AddressBar)
        def _get_Resizable(self) -> hints.Incomplete: ...
        def _set_Resizable(self, Value: hints.Incomplete) -> hints.Hresult: ...
        Resizable = hints.normal_property(_get_Resizable, _set_Resizable)


IWebBrowser._methods_ = [
    COMMETHOD(
        [dispid(100), helpstring('Navigates to the previous item in the history list.')],
        HRESULT,
        'GoBack',
    ),
    COMMETHOD(
        [dispid(101), helpstring('Navigates to the next item in the history list.')],
        HRESULT,
        'GoForward',
    ),
    COMMETHOD(
        [dispid(102), helpstring('Go home/start page.')],
        HRESULT,
        'GoHome',
    ),
    COMMETHOD(
        [dispid(103), helpstring('Go Search Page.')],
        HRESULT,
        'GoSearch',
    ),
    COMMETHOD(
        [dispid(104), helpstring('Navigates to a URL or file.')],
        HRESULT,
        'Navigate',
        (['in'], BSTR, 'URL'),
        (['in', 'optional'], POINTER(VARIANT), 'Flags'),
        (['in', 'optional'], POINTER(VARIANT), 'TargetFrameName'),
        (['in', 'optional'], POINTER(VARIANT), 'PostData'),
        (['in', 'optional'], POINTER(VARIANT), 'Headers')
    ),
    COMMETHOD(
        [dispid(-550), helpstring('Refresh the currently viewed page.')],
        HRESULT,
        'Refresh',
    ),
    COMMETHOD(
        [dispid(105), helpstring('Refresh the currently viewed page.')],
        HRESULT,
        'Refresh2',
        (['in', 'optional'], POINTER(VARIANT), 'Level')
    ),
    COMMETHOD(
        [dispid(106), helpstring('Stops opening a file.')],
        HRESULT,
        'Stop',
    ),
    COMMETHOD(
        [dispid(200), helpstring('Returns the application automation object if accessible, this automation object otherwise..'), 'propget'],
        HRESULT,
        'Application',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppDisp')
    ),
    COMMETHOD(
        [dispid(201), helpstring('Returns the automation object of the container/parent if one exists or this automation object.'), 'propget'],
        HRESULT,
        'Parent',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppDisp')
    ),
    COMMETHOD(
        [dispid(202), helpstring('Returns the container/parent automation object, if any.'), 'propget'],
        HRESULT,
        'Container',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppDisp')
    ),
    COMMETHOD(
        [dispid(203), helpstring('Returns the active Document automation object, if any.'), 'propget'],
        HRESULT,
        'Document',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppDisp')
    ),
    COMMETHOD(
        [dispid(204), helpstring('Returns True if this is the top level object.'), 'propget'],
        HRESULT,
        'TopLevelContainer',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(205), helpstring('Returns the type of the contained document object.'), 'propget'],
        HRESULT,
        'Type',
        (['out', 'retval'], POINTER(BSTR), 'Type')
    ),
    COMMETHOD(
        [dispid(206), helpstring('The horizontal position (pixels) of the frame window relative to the screen/container.'), 'propget'],
        HRESULT,
        'Left',
        (['out', 'retval'], POINTER(c_int), 'pl')
    ),
    COMMETHOD(
        [dispid(206), helpstring('The horizontal position (pixels) of the frame window relative to the screen/container.'), 'propput'],
        HRESULT,
        'Left',
        (['in'], c_int, 'pl')
    ),
    COMMETHOD(
        [dispid(207), helpstring('The vertical position (pixels) of the frame window relative to the screen/container.'), 'propget'],
        HRESULT,
        'Top',
        (['out', 'retval'], POINTER(c_int), 'pl')
    ),
    COMMETHOD(
        [dispid(207), helpstring('The vertical position (pixels) of the frame window relative to the screen/container.'), 'propput'],
        HRESULT,
        'Top',
        (['in'], c_int, 'pl')
    ),
    COMMETHOD(
        [dispid(208), helpstring('The horizontal dimension (pixels) of the frame window/object.'), 'propget'],
        HRESULT,
        'Width',
        (['out', 'retval'], POINTER(c_int), 'pl')
    ),
    COMMETHOD(
        [dispid(208), helpstring('The horizontal dimension (pixels) of the frame window/object.'), 'propput'],
        HRESULT,
        'Width',
        (['in'], c_int, 'pl')
    ),
    COMMETHOD(
        [dispid(209), helpstring('The vertical dimension (pixels) of the frame window/object.'), 'propget'],
        HRESULT,
        'Height',
        (['out', 'retval'], POINTER(c_int), 'pl')
    ),
    COMMETHOD(
        [dispid(209), helpstring('The vertical dimension (pixels) of the frame window/object.'), 'propput'],
        HRESULT,
        'Height',
        (['in'], c_int, 'pl')
    ),
    COMMETHOD(
        [dispid(210), helpstring('Gets the short (UI-friendly) name of the URL/file currently viewed.'), 'propget'],
        HRESULT,
        'LocationName',
        (['out', 'retval'], POINTER(BSTR), 'LocationName')
    ),
    COMMETHOD(
        [dispid(211), helpstring('Gets the full URL/path currently viewed.'), 'propget'],
        HRESULT,
        'LocationURL',
        (['out', 'retval'], POINTER(BSTR), 'LocationURL')
    ),
    COMMETHOD(
        [dispid(212), helpstring('Query to see if something is still in progress.'), 'propget'],
        HRESULT,
        'Busy',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
]

################################################################
# code template for IWebBrowser implementation
# class IWebBrowser_Impl(object):
#     def GoBack(self):
#         'Navigates to the previous item in the history list.'
#         #return 
#
#     def GoForward(self):
#         'Navigates to the next item in the history list.'
#         #return 
#
#     def GoHome(self):
#         'Go home/start page.'
#         #return 
#
#     def GoSearch(self):
#         'Go Search Page.'
#         #return 
#
#     def Navigate(self, URL, Flags, TargetFrameName, PostData, Headers):
#         'Navigates to a URL or file.'
#         #return 
#
#     def Refresh(self):
#         'Refresh the currently viewed page.'
#         #return 
#
#     def Refresh2(self, Level):
#         'Refresh the currently viewed page.'
#         #return 
#
#     def Stop(self):
#         'Stops opening a file.'
#         #return 
#
#     @property
#     def Application(self):
#         'Returns the application automation object if accessible, this automation object otherwise..'
#         #return ppDisp
#
#     @property
#     def Parent(self):
#         'Returns the automation object of the container/parent if one exists or this automation object.'
#         #return ppDisp
#
#     @property
#     def Container(self):
#         'Returns the container/parent automation object, if any.'
#         #return ppDisp
#
#     @property
#     def Document(self):
#         'Returns the active Document automation object, if any.'
#         #return ppDisp
#
#     @property
#     def TopLevelContainer(self):
#         'Returns True if this is the top level object.'
#         #return pBool
#
#     @property
#     def Type(self):
#         'Returns the type of the contained document object.'
#         #return Type
#
#     def _get(self):
#         'The horizontal position (pixels) of the frame window relative to the screen/container.'
#         #return pl
#     def _set(self, pl):
#         'The horizontal position (pixels) of the frame window relative to the screen/container.'
#     Left = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'The vertical position (pixels) of the frame window relative to the screen/container.'
#         #return pl
#     def _set(self, pl):
#         'The vertical position (pixels) of the frame window relative to the screen/container.'
#     Top = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'The horizontal dimension (pixels) of the frame window/object.'
#         #return pl
#     def _set(self, pl):
#         'The horizontal dimension (pixels) of the frame window/object.'
#     Width = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'The vertical dimension (pixels) of the frame window/object.'
#         #return pl
#     def _set(self, pl):
#         'The vertical dimension (pixels) of the frame window/object.'
#     Height = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def LocationName(self):
#         'Gets the short (UI-friendly) name of the URL/file currently viewed.'
#         #return LocationName
#
#     @property
#     def LocationURL(self):
#         'Gets the full URL/path currently viewed.'
#         #return LocationURL
#
#     @property
#     def Busy(self):
#         'Query to see if something is still in progress.'
#         #return pBool
#

IWebBrowserApp._methods_ = [
    COMMETHOD(
        [dispid(300), helpstring('Exits application and closes the open document.')],
        HRESULT,
        'Quit',
    ),
    COMMETHOD(
        [dispid(301), helpstring('Converts client sizes into window sizes.')],
        HRESULT,
        'ClientToWindow',
        (['in', 'out'], POINTER(c_int), 'pcx'),
        (['in', 'out'], POINTER(c_int), 'pcy')
    ),
    COMMETHOD(
        [dispid(302), helpstring('Associates vtValue with the name szProperty in the context of the object.')],
        HRESULT,
        'PutProperty',
        (['in'], BSTR, 'Property'),
        (['in'], VARIANT, 'vtValue')
    ),
    COMMETHOD(
        [dispid(303), helpstring('Retrieve the Associated value for the property vtValue in the context of the object.')],
        HRESULT,
        'GetProperty',
        (['in'], BSTR, 'Property'),
        (['out', 'retval'], POINTER(VARIANT), 'pvtValue')
    ),
    COMMETHOD(
        [dispid(0), helpstring('Returns name of the application.'), 'propget'],
        HRESULT,
        'Name',
        (['out', 'retval'], POINTER(BSTR), 'Name')
    ),
    COMMETHOD(
        [dispid(-515), helpstring('Returns the HWND of the current IE window.'), 'propget'],
        HRESULT,
        'HWND',
        (['out', 'retval'], POINTER(c_longlong), 'pHWND')
    ),
    COMMETHOD(
        [dispid(400), helpstring('Returns file specification of the application, including path.'), 'propget'],
        HRESULT,
        'FullName',
        (['out', 'retval'], POINTER(BSTR), 'FullName')
    ),
    COMMETHOD(
        [dispid(401), helpstring('Returns the path to the application.'), 'propget'],
        HRESULT,
        'Path',
        (['out', 'retval'], POINTER(BSTR), 'Path')
    ),
    COMMETHOD(
        [dispid(402), helpstring('Determines whether the application is visible or hidden.'), 'propget'],
        HRESULT,
        'Visible',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(402), helpstring('Determines whether the application is visible or hidden.'), 'propput'],
        HRESULT,
        'Visible',
        (['in'], VARIANT_BOOL, 'pBool')
    ),
    COMMETHOD(
        [dispid(403), helpstring('Turn on or off the statusbar.'), 'propget'],
        HRESULT,
        'StatusBar',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(403), helpstring('Turn on or off the statusbar.'), 'propput'],
        HRESULT,
        'StatusBar',
        (['in'], VARIANT_BOOL, 'pBool')
    ),
    COMMETHOD(
        [dispid(404), helpstring('Text of Status window.'), 'propget'],
        HRESULT,
        'StatusText',
        (['out', 'retval'], POINTER(BSTR), 'StatusText')
    ),
    COMMETHOD(
        [dispid(404), helpstring('Text of Status window.'), 'propput'],
        HRESULT,
        'StatusText',
        (['in'], BSTR, 'StatusText')
    ),
    COMMETHOD(
        [dispid(405), helpstring('Controls which toolbar is shown.'), 'propget'],
        HRESULT,
        'ToolBar',
        (['out', 'retval'], POINTER(c_int), 'Value')
    ),
    COMMETHOD(
        [dispid(405), helpstring('Controls which toolbar is shown.'), 'propput'],
        HRESULT,
        'ToolBar',
        (['in'], c_int, 'Value')
    ),
    COMMETHOD(
        [dispid(406), helpstring('Controls whether menubar is shown.'), 'propget'],
        HRESULT,
        'MenuBar',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'Value')
    ),
    COMMETHOD(
        [dispid(406), helpstring('Controls whether menubar is shown.'), 'propput'],
        HRESULT,
        'MenuBar',
        (['in'], VARIANT_BOOL, 'Value')
    ),
    COMMETHOD(
        [dispid(407), helpstring('Maximizes window and turns off statusbar, toolbar, menubar, and titlebar.'), 'propget'],
        HRESULT,
        'FullScreen',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbFullScreen')
    ),
    COMMETHOD(
        [dispid(407), helpstring('Maximizes window and turns off statusbar, toolbar, menubar, and titlebar.'), 'propput'],
        HRESULT,
        'FullScreen',
        (['in'], VARIANT_BOOL, 'pbFullScreen')
    ),
]

################################################################
# code template for IWebBrowserApp implementation
# class IWebBrowserApp_Impl(object):
#     def Quit(self):
#         'Exits application and closes the open document.'
#         #return 
#
#     def ClientToWindow(self):
#         'Converts client sizes into window sizes.'
#         #return pcx, pcy
#
#     def PutProperty(self, Property, vtValue):
#         'Associates vtValue with the name szProperty in the context of the object.'
#         #return 
#
#     def GetProperty(self, Property):
#         'Retrieve the Associated value for the property vtValue in the context of the object.'
#         #return pvtValue
#
#     @property
#     def Name(self):
#         'Returns name of the application.'
#         #return Name
#
#     @property
#     def HWND(self):
#         'Returns the HWND of the current IE window.'
#         #return pHWND
#
#     @property
#     def FullName(self):
#         'Returns file specification of the application, including path.'
#         #return FullName
#
#     @property
#     def Path(self):
#         'Returns the path to the application.'
#         #return Path
#
#     def _get(self):
#         'Determines whether the application is visible or hidden.'
#         #return pBool
#     def _set(self, pBool):
#         'Determines whether the application is visible or hidden.'
#     Visible = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Turn on or off the statusbar.'
#         #return pBool
#     def _set(self, pBool):
#         'Turn on or off the statusbar.'
#     StatusBar = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Text of Status window.'
#         #return StatusText
#     def _set(self, StatusText):
#         'Text of Status window.'
#     StatusText = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls which toolbar is shown.'
#         #return Value
#     def _set(self, Value):
#         'Controls which toolbar is shown.'
#     ToolBar = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls whether menubar is shown.'
#         #return Value
#     def _set(self, Value):
#         'Controls whether menubar is shown.'
#     MenuBar = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Maximizes window and turns off statusbar, toolbar, menubar, and titlebar.'
#         #return pbFullScreen
#     def _set(self, pbFullScreen):
#         'Maximizes window and turns off statusbar, toolbar, menubar, and titlebar.'
#     FullScreen = property(_get, _set, doc = _set.__doc__)
#

IWebBrowser2._methods_ = [
    COMMETHOD(
        [dispid(500), helpstring('Navigates to a URL or file or pidl.')],
        HRESULT,
        'Navigate2',
        (['in'], POINTER(VARIANT), 'URL'),
        (['in', 'optional'], POINTER(VARIANT), 'Flags'),
        (['in', 'optional'], POINTER(VARIANT), 'TargetFrameName'),
        (['in', 'optional'], POINTER(VARIANT), 'PostData'),
        (['in', 'optional'], POINTER(VARIANT), 'Headers')
    ),
    COMMETHOD(
        [dispid(501), helpstring('IOleCommandTarget::QueryStatus')],
        HRESULT,
        'QueryStatusWB',
        (['in'], OLECMDID, 'cmdID'),
        (['out', 'retval'], POINTER(OLECMDF), 'pcmdf')
    ),
    COMMETHOD(
        [dispid(502), helpstring('IOleCommandTarget::Exec')],
        HRESULT,
        'ExecWB',
        (['in'], OLECMDID, 'cmdID'),
        (['in'], OLECMDEXECOPT, 'cmdexecopt'),
        (['in', 'optional'], POINTER(VARIANT), 'pvaIn'),
        (['in', 'out', 'optional'], POINTER(VARIANT), 'pvaOut')
    ),
    COMMETHOD(
        [dispid(503), helpstring('Set BrowserBar to Clsid')],
        HRESULT,
        'ShowBrowserBar',
        (['in'], POINTER(VARIANT), 'pvaClsid'),
        (['in', 'optional'], POINTER(VARIANT), 'pvarShow'),
        (['in', 'optional'], POINTER(VARIANT), 'pvarSize')
    ),
    COMMETHOD(
        [dispid(-525), 'bindable', 'propget'],
        HRESULT,
        'ReadyState',
        (['out', 'retval'], POINTER(tagREADYSTATE), 'plReadyState')
    ),
    COMMETHOD(
        [dispid(550), helpstring('Controls if the frame is offline (read from cache)'), 'propget'],
        HRESULT,
        'Offline',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbOffline')
    ),
    COMMETHOD(
        [dispid(550), helpstring('Controls if the frame is offline (read from cache)'), 'propput'],
        HRESULT,
        'Offline',
        (['in'], VARIANT_BOOL, 'pbOffline')
    ),
    COMMETHOD(
        [dispid(551), helpstring('Controls if any dialog boxes can be shown'), 'propget'],
        HRESULT,
        'Silent',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbSilent')
    ),
    COMMETHOD(
        [dispid(551), helpstring('Controls if any dialog boxes can be shown'), 'propput'],
        HRESULT,
        'Silent',
        (['in'], VARIANT_BOOL, 'pbSilent')
    ),
    COMMETHOD(
        [dispid(552), helpstring('Registers OC as a top-level browser (for target name resolution)'), 'propget'],
        HRESULT,
        'RegisterAsBrowser',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbRegister')
    ),
    COMMETHOD(
        [dispid(552), helpstring('Registers OC as a top-level browser (for target name resolution)'), 'propput'],
        HRESULT,
        'RegisterAsBrowser',
        (['in'], VARIANT_BOOL, 'pbRegister')
    ),
    COMMETHOD(
        [dispid(553), helpstring('Registers OC as a drop target for navigation'), 'propget'],
        HRESULT,
        'RegisterAsDropTarget',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbRegister')
    ),
    COMMETHOD(
        [dispid(553), helpstring('Registers OC as a drop target for navigation'), 'propput'],
        HRESULT,
        'RegisterAsDropTarget',
        (['in'], VARIANT_BOOL, 'pbRegister')
    ),
    COMMETHOD(
        [dispid(554), helpstring('Controls if the browser is in theater mode'), 'propget'],
        HRESULT,
        'TheaterMode',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pbRegister')
    ),
    COMMETHOD(
        [dispid(554), helpstring('Controls if the browser is in theater mode'), 'propput'],
        HRESULT,
        'TheaterMode',
        (['in'], VARIANT_BOOL, 'pbRegister')
    ),
    COMMETHOD(
        [dispid(555), helpstring('Controls whether address bar is shown'), 'propget'],
        HRESULT,
        'AddressBar',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'Value')
    ),
    COMMETHOD(
        [dispid(555), helpstring('Controls whether address bar is shown'), 'propput'],
        HRESULT,
        'AddressBar',
        (['in'], VARIANT_BOOL, 'Value')
    ),
    COMMETHOD(
        [dispid(556), helpstring('Controls whether the window is resizable'), 'propget'],
        HRESULT,
        'Resizable',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'Value')
    ),
    COMMETHOD(
        [dispid(556), helpstring('Controls whether the window is resizable'), 'propput'],
        HRESULT,
        'Resizable',
        (['in'], VARIANT_BOOL, 'Value')
    ),
]

################################################################
# code template for IWebBrowser2 implementation
# class IWebBrowser2_Impl(object):
#     def Navigate2(self, URL, Flags, TargetFrameName, PostData, Headers):
#         'Navigates to a URL or file or pidl.'
#         #return 
#
#     def QueryStatusWB(self, cmdID):
#         'IOleCommandTarget::QueryStatus'
#         #return pcmdf
#
#     def ExecWB(self, cmdID, cmdexecopt, pvaIn):
#         'IOleCommandTarget::Exec'
#         #return pvaOut
#
#     def ShowBrowserBar(self, pvaClsid, pvarShow, pvarSize):
#         'Set BrowserBar to Clsid'
#         #return 
#
#     @property
#     def ReadyState(self):
#         '-no docstring-'
#         #return plReadyState
#
#     def _get(self):
#         'Controls if the frame is offline (read from cache)'
#         #return pbOffline
#     def _set(self, pbOffline):
#         'Controls if the frame is offline (read from cache)'
#     Offline = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls if any dialog boxes can be shown'
#         #return pbSilent
#     def _set(self, pbSilent):
#         'Controls if any dialog boxes can be shown'
#     Silent = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Registers OC as a top-level browser (for target name resolution)'
#         #return pbRegister
#     def _set(self, pbRegister):
#         'Registers OC as a top-level browser (for target name resolution)'
#     RegisterAsBrowser = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Registers OC as a drop target for navigation'
#         #return pbRegister
#     def _set(self, pbRegister):
#         'Registers OC as a drop target for navigation'
#     RegisterAsDropTarget = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls if the browser is in theater mode'
#         #return pbRegister
#     def _set(self, pbRegister):
#         'Controls if the browser is in theater mode'
#     TheaterMode = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls whether address bar is shown'
#         #return Value
#     def _set(self, Value):
#         'Controls whether address bar is shown'
#     AddressBar = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'Controls whether the window is resizable'
#         #return Value
#     def _set(self, Value):
#         'Controls whether the window is resizable'
#     Resizable = property(_get, _set, doc = _set.__doc__)
#


class IShellFavoritesNameSpace(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """IShellFavoritesNameSpace Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{55136804-B2DE-11D1-B9F2-00A0C98BC547}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def MoveSelectionUp(self) -> hints.Hresult: ...
        def MoveSelectionDown(self) -> hints.Hresult: ...
        def ResetSort(self) -> hints.Hresult: ...
        def NewFolder(self) -> hints.Hresult: ...
        def Synchronize(self) -> hints.Hresult: ...
        def Import(self) -> hints.Hresult: ...
        def Export(self) -> hints.Hresult: ...
        def InvokeContextMenuCommand(self, strCommand: hints.Incomplete) -> hints.Hresult: ...
        def MoveSelectionTo(self) -> hints.Hresult: ...
        def _get_SubscriptionsEnabled(self) -> hints.Incomplete: ...
        SubscriptionsEnabled = hints.normal_property(_get_SubscriptionsEnabled)
        def CreateSubscriptionForSelection(self) -> hints.Incomplete: ...
        def DeleteSubscriptionForSelection(self) -> hints.Incomplete: ...
        def SetRoot(self, bstrFullPath: hints.Incomplete) -> hints.Hresult: ...


class IShellNameSpace(IShellFavoritesNameSpace):
    """IShellNameSpace Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{E572D3C9-37BE-4AE2-825D-D521763E3108}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_EnumOptions(self) -> hints.Incomplete: ...
        def _set_EnumOptions(self, pgrfEnumFlags: hints.Incomplete) -> hints.Hresult: ...
        EnumOptions = hints.normal_property(_get_EnumOptions, _set_EnumOptions)
        def _get_SelectedItem(self) -> hints.Incomplete: ...
        def _set_SelectedItem(self, pItem: hints.Incomplete) -> hints.Hresult: ...
        SelectedItem = hints.normal_property(_get_SelectedItem, _set_SelectedItem)
        def _get_Root(self) -> hints.Incomplete: ...
        def _set_Root(self, pvar: hints.Incomplete) -> hints.Hresult: ...
        Root = hints.normal_property(_get_Root, _set_Root)
        def _get_Depth(self) -> hints.Incomplete: ...
        def _set_Depth(self, piDepth: hints.Incomplete) -> hints.Hresult: ...
        Depth = hints.normal_property(_get_Depth, _set_Depth)
        def _get_Mode(self) -> hints.Incomplete: ...
        def _set_Mode(self, puMode: hints.Incomplete) -> hints.Hresult: ...
        Mode = hints.normal_property(_get_Mode, _set_Mode)
        def _get_Flags(self) -> hints.Incomplete: ...
        def _set_Flags(self, pdwFlags: hints.Incomplete) -> hints.Hresult: ...
        Flags = hints.normal_property(_get_Flags, _set_Flags)
        def _get_TVFlags(self) -> hints.Incomplete: ...
        def _set_TVFlags(self, dwFlags: hints.Incomplete) -> hints.Hresult: ...
        TVFlags = hints.normal_property(_get_TVFlags, _set_TVFlags)
        def _get_Columns(self) -> hints.Incomplete: ...
        def _set_Columns(self, bstrColumns: hints.Incomplete) -> hints.Hresult: ...
        Columns = hints.normal_property(_get_Columns, _set_Columns)
        def _get_CountViewTypes(self) -> hints.Incomplete: ...
        CountViewTypes = hints.normal_property(_get_CountViewTypes)
        def SetViewType(self, iType: hints.Incomplete) -> hints.Hresult: ...
        def SelectedItems(self) -> hints.Incomplete: ...
        def Expand(self, var: hints.Incomplete, iDepth: hints.Incomplete) -> hints.Hresult: ...
        def UnselectAll(self) -> hints.Hresult: ...


IShellFavoritesNameSpace._methods_ = [
    COMMETHOD(
        [dispid(1), helpstring('method MoveSelectionUp')],
        HRESULT,
        'MoveSelectionUp',
    ),
    COMMETHOD(
        [dispid(2), helpstring('method MoveSelectionDown')],
        HRESULT,
        'MoveSelectionDown',
    ),
    COMMETHOD(
        [dispid(3), helpstring('method ResetSort')],
        HRESULT,
        'ResetSort',
    ),
    COMMETHOD(
        [dispid(4), helpstring('method NewFolder')],
        HRESULT,
        'NewFolder',
    ),
    COMMETHOD(
        [dispid(5), helpstring('method Synchronize')],
        HRESULT,
        'Synchronize',
    ),
    COMMETHOD([dispid(6), helpstring('method Import')], HRESULT, 'Import'),
    COMMETHOD([dispid(7), helpstring('method Export')], HRESULT, 'Export'),
    COMMETHOD(
        [dispid(8), helpstring('method InvokeContextMenuCommand')],
        HRESULT,
        'InvokeContextMenuCommand',
        (['in'], BSTR, 'strCommand')
    ),
    COMMETHOD(
        [dispid(9), helpstring('method MoveSelectionTo')],
        HRESULT,
        'MoveSelectionTo',
    ),
    COMMETHOD(
        [dispid(10), helpstring('Query to see if subscriptions are enabled'), 'propget'],
        HRESULT,
        'SubscriptionsEnabled',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(11), helpstring('method CreateSubscriptionForSelection')],
        HRESULT,
        'CreateSubscriptionForSelection',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(12), helpstring('method DeleteSubscriptionForSelection')],
        HRESULT,
        'DeleteSubscriptionForSelection',
        (['out', 'retval'], POINTER(VARIANT_BOOL), 'pBool')
    ),
    COMMETHOD(
        [dispid(13), helpstring('old, use put_Root() instead')],
        HRESULT,
        'SetRoot',
        (['in'], BSTR, 'bstrFullPath')
    ),
]

################################################################
# code template for IShellFavoritesNameSpace implementation
# class IShellFavoritesNameSpace_Impl(object):
#     def MoveSelectionUp(self):
#         'method MoveSelectionUp'
#         #return 
#
#     def MoveSelectionDown(self):
#         'method MoveSelectionDown'
#         #return 
#
#     def ResetSort(self):
#         'method ResetSort'
#         #return 
#
#     def NewFolder(self):
#         'method NewFolder'
#         #return 
#
#     def Synchronize(self):
#         'method Synchronize'
#         #return 
#
#     def Import(self):
#         'method Import'
#         #return 
#
#     def Export(self):
#         'method Export'
#         #return 
#
#     def InvokeContextMenuCommand(self, strCommand):
#         'method InvokeContextMenuCommand'
#         #return 
#
#     def MoveSelectionTo(self):
#         'method MoveSelectionTo'
#         #return 
#
#     @property
#     def SubscriptionsEnabled(self):
#         'Query to see if subscriptions are enabled'
#         #return pBool
#
#     def CreateSubscriptionForSelection(self):
#         'method CreateSubscriptionForSelection'
#         #return pBool
#
#     def DeleteSubscriptionForSelection(self):
#         'method DeleteSubscriptionForSelection'
#         #return pBool
#
#     def SetRoot(self, bstrFullPath):
#         'old, use put_Root() instead'
#         #return 
#

IShellNameSpace._methods_ = [
    COMMETHOD(
        [dispid(14), helpstring('options '), 'propget'],
        HRESULT,
        'EnumOptions',
        (['out', 'retval'], POINTER(c_int), 'pgrfEnumFlags')
    ),
    COMMETHOD(
        [dispid(14), helpstring('options '), 'propput'],
        HRESULT,
        'EnumOptions',
        (['in'], c_int, 'pgrfEnumFlags')
    ),
    COMMETHOD(
        [dispid(15), helpstring('get the selected item'), 'propget'],
        HRESULT,
        'SelectedItem',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'pItem')
    ),
    COMMETHOD(
        [dispid(15), helpstring('get the selected item'), 'propput'],
        HRESULT,
        'SelectedItem',
        (['in'], POINTER(IDispatch), 'pItem')
    ),
    COMMETHOD(
        [dispid(16), helpstring('get the root item'), 'propget'],
        HRESULT,
        'Root',
        (['out', 'retval'], POINTER(VARIANT), 'pvar')
    ),
    COMMETHOD(
        [dispid(16), helpstring('get the root item'), 'propput'],
        HRESULT,
        'Root',
        (['in'], VARIANT, 'pvar')
    ),
    COMMETHOD(
        [dispid(17), 'propget'],
        HRESULT,
        'Depth',
        (['out', 'retval'], POINTER(c_int), 'piDepth')
    ),
    COMMETHOD(
        [dispid(17), 'propput'],
        HRESULT,
        'Depth',
        (['in'], c_int, 'piDepth')
    ),
    COMMETHOD(
        [dispid(18), 'propget'],
        HRESULT,
        'Mode',
        (['out', 'retval'], POINTER(c_uint), 'puMode')
    ),
    COMMETHOD(
        [dispid(18), 'propput'],
        HRESULT,
        'Mode',
        (['in'], c_uint, 'puMode')
    ),
    COMMETHOD(
        [dispid(19), 'propget'],
        HRESULT,
        'Flags',
        (['out', 'retval'], POINTER(c_ulong), 'pdwFlags')
    ),
    COMMETHOD(
        [dispid(19), 'propput'],
        HRESULT,
        'Flags',
        (['in'], c_ulong, 'pdwFlags')
    ),
    COMMETHOD(
        [dispid(20), 'propput'],
        HRESULT,
        'TVFlags',
        (['in'], c_ulong, 'dwFlags')
    ),
    COMMETHOD(
        [dispid(20), 'propget'],
        HRESULT,
        'TVFlags',
        (['out', 'retval'], POINTER(c_ulong), 'dwFlags')
    ),
    COMMETHOD(
        [dispid(21), 'propget'],
        HRESULT,
        'Columns',
        (['out', 'retval'], POINTER(BSTR), 'bstrColumns')
    ),
    COMMETHOD(
        [dispid(21), 'propput'],
        HRESULT,
        'Columns',
        (['in'], BSTR, 'bstrColumns')
    ),
    COMMETHOD(
        [dispid(22), helpstring('number of view types'), 'propget'],
        HRESULT,
        'CountViewTypes',
        (['out', 'retval'], POINTER(c_int), 'piTypes')
    ),
    COMMETHOD(
        [dispid(23), helpstring('set view type')],
        HRESULT,
        'SetViewType',
        (['in'], c_int, 'iType')
    ),
    COMMETHOD(
        [dispid(24), helpstring('collection of selected items')],
        HRESULT,
        'SelectedItems',
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppid')
    ),
    COMMETHOD(
        [dispid(25), helpstring('expands item specified depth')],
        HRESULT,
        'Expand',
        (['in'], VARIANT, 'var'),
        ([], c_int, 'iDepth')
    ),
    COMMETHOD(
        [dispid(26), helpstring('unselects all items')],
        HRESULT,
        'UnselectAll',
    ),
]

################################################################
# code template for IShellNameSpace implementation
# class IShellNameSpace_Impl(object):
#     def _get(self):
#         'options '
#         #return pgrfEnumFlags
#     def _set(self, pgrfEnumFlags):
#         'options '
#     EnumOptions = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'get the selected item'
#         #return pItem
#     def _set(self, pItem):
#         'get the selected item'
#     SelectedItem = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         'get the root item'
#         #return pvar
#     def _set(self, pvar):
#         'get the root item'
#     Root = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return piDepth
#     def _set(self, piDepth):
#         '-no docstring-'
#     Depth = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return puMode
#     def _set(self, puMode):
#         '-no docstring-'
#     Mode = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return pdwFlags
#     def _set(self, pdwFlags):
#         '-no docstring-'
#     Flags = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return dwFlags
#     def _set(self, dwFlags):
#         '-no docstring-'
#     TVFlags = property(_get, _set, doc = _set.__doc__)
#
#     def _get(self):
#         '-no docstring-'
#         #return bstrColumns
#     def _set(self, bstrColumns):
#         '-no docstring-'
#     Columns = property(_get, _set, doc = _set.__doc__)
#
#     @property
#     def CountViewTypes(self):
#         'number of view types'
#         #return piTypes
#
#     def SetViewType(self, iType):
#         'set view type'
#         #return 
#
#     def SelectedItems(self):
#         'collection of selected items'
#         #return ppid
#
#     def Expand(self, var, iDepth):
#         'expands item specified depth'
#         #return 
#
#     def UnselectAll(self):
#         'unselects all items'
#         #return 
#


class InternetExplorerMedium(CoClass):
    """Internet Explorer Application with default integrity of Medium"""
    _reg_clsid_ = GUID('{D5E8041D-920F-45E9-B8FB-B1DEB82C6E5E}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


class DWebBrowserEvents2(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Web Browser Control events interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{34A715A0-6587-11D0-924A-0020AFC7AC4D}')
    _idlflags_ = ['hidden']
    _methods_ = []

    if TYPE_CHECKING:  # dispmembers
        def StatusTextChange(self, Text: hints.Incomplete) -> hints.Incomplete: ...
        def ProgressChange(self, Progress: hints.Incomplete, ProgressMax: hints.Incomplete) -> hints.Incomplete: ...
        def CommandStateChange(self, Command: hints.Incomplete, Enable: hints.Incomplete) -> hints.Incomplete: ...
        def DownloadBegin(self) -> hints.Incomplete: ...
        def DownloadComplete(self) -> hints.Incomplete: ...
        def TitleChange(self, Text: hints.Incomplete) -> hints.Incomplete: ...
        def PropertyChange(self, szProperty: hints.Incomplete) -> hints.Incomplete: ...
        def BeforeNavigate2(self, pDisp: hints.Incomplete, URL: hints.Incomplete, Flags: hints.Incomplete, TargetFrameName: hints.Incomplete, PostData: hints.Incomplete, Headers: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def NewWindow2(self, ppDisp: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def NavigateComplete2(self, pDisp: hints.Incomplete, URL: hints.Incomplete) -> hints.Incomplete: ...
        def DocumentComplete(self, pDisp: hints.Incomplete, URL: hints.Incomplete) -> hints.Incomplete: ...
        def OnQuit(self) -> hints.Incomplete: ...
        def OnVisible(self, Visible: hints.Incomplete) -> hints.Incomplete: ...
        def OnToolBar(self, ToolBar: hints.Incomplete) -> hints.Incomplete: ...
        def OnMenuBar(self, MenuBar: hints.Incomplete) -> hints.Incomplete: ...
        def OnStatusBar(self, StatusBar: hints.Incomplete) -> hints.Incomplete: ...
        def OnFullScreen(self, FullScreen: hints.Incomplete) -> hints.Incomplete: ...
        def OnTheaterMode(self, TheaterMode: hints.Incomplete) -> hints.Incomplete: ...
        def WindowSetResizable(self, Resizable: hints.Incomplete) -> hints.Incomplete: ...
        def WindowSetLeft(self, Left: hints.Incomplete) -> hints.Incomplete: ...
        def WindowSetTop(self, Top: hints.Incomplete) -> hints.Incomplete: ...
        def WindowSetWidth(self, Width: hints.Incomplete) -> hints.Incomplete: ...
        def WindowSetHeight(self, Height: hints.Incomplete) -> hints.Incomplete: ...
        def WindowClosing(self, IsChildWindow: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def ClientToHostWindow(self, CX: hints.Incomplete, CY: hints.Incomplete) -> hints.Incomplete: ...
        def SetSecureLockIcon(self, SecureLockIcon: hints.Incomplete) -> hints.Incomplete: ...
        def FileDownload(self, ActiveDocument: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def NavigateError(self, pDisp: hints.Incomplete, URL: hints.Incomplete, Frame: hints.Incomplete, StatusCode: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def PrintTemplateInstantiation(self, pDisp: hints.Incomplete) -> hints.Incomplete: ...
        def PrintTemplateTeardown(self, pDisp: hints.Incomplete) -> hints.Incomplete: ...
        def UpdatePageStatus(self, pDisp: hints.Incomplete, nPage: hints.Incomplete, fDone: hints.Incomplete) -> hints.Incomplete: ...
        def PrivacyImpactedStateChange(self, bImpacted: hints.Incomplete) -> hints.Incomplete: ...
        def NewWindow3(self, ppDisp: hints.Incomplete, Cancel: hints.Incomplete, dwFlags: hints.Incomplete, bstrUrlContext: hints.Incomplete, bstrUrl: hints.Incomplete) -> hints.Incomplete: ...
        def SetPhishingFilterStatus(self, PhishingFilterStatus: hints.Incomplete) -> hints.Incomplete: ...
        def WindowStateChanged(self, dwWindowStateFlags: hints.Incomplete, dwValidFlagsMask: hints.Incomplete) -> hints.Incomplete: ...
        def NewProcess(self, lCauseFlag: hints.Incomplete, pWB2: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def ThirdPartyUrlBlocked(self, URL: hints.Incomplete, dwCount: hints.Incomplete) -> hints.Incomplete: ...
        def RedirectXDomainBlocked(self, pDisp: hints.Incomplete, StartURL: hints.Incomplete, RedirectURL: hints.Incomplete, Frame: hints.Incomplete, StatusCode: hints.Incomplete) -> hints.Incomplete: ...
        def BeforeScriptExecute(self, pDispWindow: hints.Incomplete) -> hints.Incomplete: ...
        def WebWorkerStarted(self, dwUniqueID: hints.Incomplete, bstrWorkerLabel: hints.Incomplete) -> hints.Incomplete: ...
        def WebWorkerFinsihed(self, dwUniqueID: hints.Incomplete) -> hints.Incomplete: ...


class DWebBrowserEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Web Browser Control Events (old)"""
    _case_insensitive_ = True
    _iid_ = GUID('{EAB22AC2-30C1-11CF-A7EB-0000C05BAE0B}')
    _idlflags_ = ['hidden']
    _methods_ = []

    if TYPE_CHECKING:  # dispmembers
        def BeforeNavigate(self, URL: hints.Incomplete, Flags: hints.Incomplete, TargetFrameName: hints.Incomplete, PostData: hints.Incomplete, Headers: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def NavigateComplete(self, URL: hints.Incomplete) -> hints.Incomplete: ...
        def StatusTextChange(self, Text: hints.Incomplete) -> hints.Incomplete: ...
        def ProgressChange(self, Progress: hints.Incomplete, ProgressMax: hints.Incomplete) -> hints.Incomplete: ...
        def DownloadComplete(self) -> hints.Incomplete: ...
        def CommandStateChange(self, Command: hints.Incomplete, Enable: hints.Incomplete) -> hints.Incomplete: ...
        def DownloadBegin(self) -> hints.Incomplete: ...
        def NewWindow(self, URL: hints.Incomplete, Flags: hints.Incomplete, TargetFrameName: hints.Incomplete, PostData: hints.Incomplete, Headers: hints.Incomplete, Processed: hints.Incomplete) -> hints.Incomplete: ...
        def TitleChange(self, Text: hints.Incomplete) -> hints.Incomplete: ...
        def FrameBeforeNavigate(self, URL: hints.Incomplete, Flags: hints.Incomplete, TargetFrameName: hints.Incomplete, PostData: hints.Incomplete, Headers: hints.Incomplete, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def FrameNavigateComplete(self, URL: hints.Incomplete) -> hints.Incomplete: ...
        def FrameNewWindow(self, URL: hints.Incomplete, Flags: hints.Incomplete, TargetFrameName: hints.Incomplete, PostData: hints.Incomplete, Headers: hints.Incomplete, Processed: hints.Incomplete) -> hints.Incomplete: ...
        def Quit(self, Cancel: hints.Incomplete) -> hints.Incomplete: ...
        def WindowMove(self) -> hints.Incomplete: ...
        def WindowResize(self) -> hints.Incomplete: ...
        def WindowActivate(self) -> hints.Incomplete: ...
        def PropertyChange(self, Property: hints.Incomplete) -> hints.Incomplete: ...


InternetExplorerMedium._com_interfaces_ = [IWebBrowser2, IWebBrowserApp]
InternetExplorerMedium._outgoing_interfaces_ = [DWebBrowserEvents2, DWebBrowserEvents]


class ShellBrowserWindow(CoClass):
    """Shell Browser Window."""
    _reg_clsid_ = GUID('{C08AFD90-F2A1-11D1-8455-00A0C91F3880}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


ShellBrowserWindow._com_interfaces_ = [IWebBrowser2, IWebBrowserApp]
ShellBrowserWindow._outgoing_interfaces_ = [DWebBrowserEvents2, DWebBrowserEvents]


class IScriptErrorList(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Script Error List Interface"""
    _case_insensitive_ = True
    _iid_ = GUID('{F3470F24-15FD-11D2-BB2E-00805FF7EFCA}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def advanceError(self) -> hints.Hresult: ...
        def retreatError(self) -> hints.Hresult: ...
        def canAdvanceError(self) -> hints.Incomplete: ...
        def canRetreatError(self) -> hints.Incomplete: ...
        def getErrorLine(self) -> hints.Incomplete: ...
        def getErrorChar(self) -> hints.Incomplete: ...
        def getErrorCode(self) -> hints.Incomplete: ...
        def getErrorMsg(self) -> hints.Incomplete: ...
        def getErrorUrl(self) -> hints.Incomplete: ...
        def getAlwaysShowLockState(self) -> hints.Incomplete: ...
        def getDetailsPaneOpen(self) -> hints.Incomplete: ...
        def setDetailsPaneOpen(self, fDetailsPaneOpen: hints.Incomplete) -> hints.Hresult: ...
        def getPerErrorDisplay(self) -> hints.Incomplete: ...
        def setPerErrorDisplay(self, fPerErrorDisplay: hints.Incomplete) -> hints.Hresult: ...


IScriptErrorList._methods_ = [
    COMMETHOD([dispid(10)], HRESULT, 'advanceError'),
    COMMETHOD([dispid(11)], HRESULT, 'retreatError'),
    COMMETHOD(
        [dispid(12)],
        HRESULT,
        'canAdvanceError',
        (['out', 'retval'], POINTER(c_int), 'pfCanAdvance')
    ),
    COMMETHOD(
        [dispid(13)],
        HRESULT,
        'canRetreatError',
        (['out', 'retval'], POINTER(c_int), 'pfCanRetreat')
    ),
    COMMETHOD(
        [dispid(14)],
        HRESULT,
        'getErrorLine',
        (['out', 'retval'], POINTER(c_int), 'plLine')
    ),
    COMMETHOD(
        [dispid(15)],
        HRESULT,
        'getErrorChar',
        (['out', 'retval'], POINTER(c_int), 'plChar')
    ),
    COMMETHOD(
        [dispid(16)],
        HRESULT,
        'getErrorCode',
        (['out', 'retval'], POINTER(c_int), 'plCode')
    ),
    COMMETHOD(
        [dispid(17)],
        HRESULT,
        'getErrorMsg',
        (['out', 'retval'], POINTER(BSTR), 'pstr')
    ),
    COMMETHOD(
        [dispid(18)],
        HRESULT,
        'getErrorUrl',
        (['out', 'retval'], POINTER(BSTR), 'pstr')
    ),
    COMMETHOD(
        [dispid(23)],
        HRESULT,
        'getAlwaysShowLockState',
        (['out', 'retval'], POINTER(c_int), 'pfAlwaysShowLocked')
    ),
    COMMETHOD(
        [dispid(19)],
        HRESULT,
        'getDetailsPaneOpen',
        (['out', 'retval'], POINTER(c_int), 'pfDetailsPaneOpen')
    ),
    COMMETHOD(
        [dispid(20)],
        HRESULT,
        'setDetailsPaneOpen',
        ([], c_int, 'fDetailsPaneOpen')
    ),
    COMMETHOD(
        [dispid(21)],
        HRESULT,
        'getPerErrorDisplay',
        (['out', 'retval'], POINTER(c_int), 'pfPerErrorDisplay')
    ),
    COMMETHOD(
        [dispid(22)],
        HRESULT,
        'setPerErrorDisplay',
        ([], c_int, 'fPerErrorDisplay')
    ),
]

################################################################
# code template for IScriptErrorList implementation
# class IScriptErrorList_Impl(object):
#     def advanceError(self):
#         '-no docstring-'
#         #return 
#
#     def retreatError(self):
#         '-no docstring-'
#         #return 
#
#     def canAdvanceError(self):
#         '-no docstring-'
#         #return pfCanAdvance
#
#     def canRetreatError(self):
#         '-no docstring-'
#         #return pfCanRetreat
#
#     def getErrorLine(self):
#         '-no docstring-'
#         #return plLine
#
#     def getErrorChar(self):
#         '-no docstring-'
#         #return plChar
#
#     def getErrorCode(self):
#         '-no docstring-'
#         #return plCode
#
#     def getErrorMsg(self):
#         '-no docstring-'
#         #return pstr
#
#     def getErrorUrl(self):
#         '-no docstring-'
#         #return pstr
#
#     def getAlwaysShowLockState(self):
#         '-no docstring-'
#         #return pfAlwaysShowLocked
#
#     def getDetailsPaneOpen(self):
#         '-no docstring-'
#         #return pfDetailsPaneOpen
#
#     def setDetailsPaneOpen(self, fDetailsPaneOpen):
#         '-no docstring-'
#         #return 
#
#     def getPerErrorDisplay(self):
#         '-no docstring-'
#         #return pfPerErrorDisplay
#
#     def setPerErrorDisplay(self, fPerErrorDisplay):
#         '-no docstring-'
#         #return 
#


class Library(object):
    """Microsoft Internet Controls"""
    name = 'SHDocVw'
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


class WebBrowser_V1(CoClass):
    """WebBrowser Control"""
    _reg_clsid_ = GUID('{EAB22AC3-30C1-11CF-A7EB-0000C05BAE0B}')
    _idlflags_ = ['control']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


WebBrowser_V1._com_interfaces_ = [IWebBrowser, IWebBrowser2]
WebBrowser_V1._outgoing_interfaces_ = [DWebBrowserEvents, DWebBrowserEvents2]

DWebBrowserEvents._disp_methods_ = [
    DISPMETHOD(
        [dispid(100), helpstring('Fired when a new hyperlink is being navigated to.')],
        None,
        'BeforeNavigate',
        (['in'], BSTR, 'URL'),
        ([], c_int, 'Flags'),
        ([], BSTR, 'TargetFrameName'),
        ([], POINTER(VARIANT), 'PostData'),
        ([], BSTR, 'Headers'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(101), helpstring('Fired when the document being navigated to becomes visible and enters the navigation stack.')],
        None,
        'NavigateComplete',
        (['in'], BSTR, 'URL')
    ),
    DISPMETHOD(
        [dispid(102), helpstring('Statusbar text changed.')],
        None,
        'StatusTextChange',
        (['in'], BSTR, 'Text')
    ),
    DISPMETHOD(
        [dispid(108), helpstring('Fired when download progress is updated.')],
        None,
        'ProgressChange',
        (['in'], c_int, 'Progress'),
        (['in'], c_int, 'ProgressMax')
    ),
    DISPMETHOD(
        [dispid(104), helpstring('Download of page complete.')],
        None,
        'DownloadComplete',
    ),
    DISPMETHOD(
        [dispid(105), helpstring('The enabled state of a command changed')],
        None,
        'CommandStateChange',
        (['in'], c_int, 'Command'),
        (['in'], VARIANT_BOOL, 'Enable')
    ),
    DISPMETHOD(
        [dispid(106), helpstring('Download of a page started.')],
        None,
        'DownloadBegin',
    ),
    DISPMETHOD(
        [dispid(107), helpstring('Fired when a new window should be created.')],
        None,
        'NewWindow',
        (['in'], BSTR, 'URL'),
        (['in'], c_int, 'Flags'),
        (['in'], BSTR, 'TargetFrameName'),
        (['in'], POINTER(VARIANT), 'PostData'),
        (['in'], BSTR, 'Headers'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Processed')
    ),
    DISPMETHOD(
        [dispid(113), helpstring('Document title changed.')],
        None,
        'TitleChange',
        (['in'], BSTR, 'Text')
    ),
    DISPMETHOD(
        [dispid(200), helpstring('Fired when a new hyperlink is being navigated to in a frame.')],
        None,
        'FrameBeforeNavigate',
        (['in'], BSTR, 'URL'),
        ([], c_int, 'Flags'),
        ([], BSTR, 'TargetFrameName'),
        ([], POINTER(VARIANT), 'PostData'),
        ([], BSTR, 'Headers'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(201), helpstring('Fired when a new hyperlink is being navigated to in a frame.')],
        None,
        'FrameNavigateComplete',
        (['in'], BSTR, 'URL')
    ),
    DISPMETHOD(
        [dispid(204), helpstring('Fired when a new window should be created.')],
        None,
        'FrameNewWindow',
        (['in'], BSTR, 'URL'),
        (['in'], c_int, 'Flags'),
        (['in'], BSTR, 'TargetFrameName'),
        (['in'], POINTER(VARIANT), 'PostData'),
        (['in'], BSTR, 'Headers'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Processed')
    ),
    DISPMETHOD(
        [dispid(103), helpstring('Fired when application is quiting.')],
        None,
        'Quit',
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(109), helpstring('Fired when window has been moved.')],
        None,
        'WindowMove',
    ),
    DISPMETHOD(
        [dispid(110), helpstring('Fired when window has been sized.')],
        None,
        'WindowResize',
    ),
    DISPMETHOD(
        [dispid(111), helpstring('Fired when window has been activated.')],
        None,
        'WindowActivate',
    ),
    DISPMETHOD(
        [dispid(112), helpstring('Fired when the PutProperty method has been called.')],
        None,
        'PropertyChange',
        (['in'], BSTR, 'Property')
    ),
]


class ShellUIHelper(CoClass):
    _reg_clsid_ = GUID('{64AB4BB7-111E-11D1-8F79-00C04FC2FBE1}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


ShellUIHelper._com_interfaces_ = [IShellUIHelper9]

DWebBrowserEvents2._disp_methods_ = [
    DISPMETHOD(
        [dispid(102), helpstring('Statusbar text changed.')],
        None,
        'StatusTextChange',
        (['in'], BSTR, 'Text')
    ),
    DISPMETHOD(
        [dispid(108), helpstring('Fired when download progress is updated.')],
        None,
        'ProgressChange',
        (['in'], c_int, 'Progress'),
        (['in'], c_int, 'ProgressMax')
    ),
    DISPMETHOD(
        [dispid(105), helpstring('The enabled state of a command changed.')],
        None,
        'CommandStateChange',
        (['in'], c_int, 'Command'),
        (['in'], VARIANT_BOOL, 'Enable')
    ),
    DISPMETHOD(
        [dispid(106), helpstring('Download of a page started.')],
        None,
        'DownloadBegin',
    ),
    DISPMETHOD(
        [dispid(104), helpstring('Download of page complete.')],
        None,
        'DownloadComplete',
    ),
    DISPMETHOD(
        [dispid(113), helpstring('Document title changed.')],
        None,
        'TitleChange',
        (['in'], BSTR, 'Text')
    ),
    DISPMETHOD(
        [dispid(112), helpstring('Fired when the PutProperty method has been called.')],
        None,
        'PropertyChange',
        (['in'], BSTR, 'szProperty')
    ),
    DISPMETHOD(
        [dispid(250), helpstring('Fired before navigate occurs in the given WebBrowser (window or frameset element). The processing of this navigation may be modified.')],
        None,
        'BeforeNavigate2',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'URL'),
        (['in'], POINTER(VARIANT), 'Flags'),
        (['in'], POINTER(VARIANT), 'TargetFrameName'),
        (['in'], POINTER(VARIANT), 'PostData'),
        (['in'], POINTER(VARIANT), 'Headers'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(251), helpstring('A new, hidden, non-navigated WebBrowser window is needed.')],
        None,
        'NewWindow2',
        (['in', 'out'], POINTER(POINTER(IDispatch)), 'ppDisp'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(252), helpstring('Fired when the document being navigated to becomes visible and enters the navigation stack.')],
        None,
        'NavigateComplete2',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'URL')
    ),
    DISPMETHOD(
        [dispid(259), helpstring('Fired when the document being navigated to reaches ReadyState_Complete.')],
        None,
        'DocumentComplete',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'URL')
    ),
    DISPMETHOD(
        [dispid(253), helpstring('Fired when application is quiting.')],
        None,
        'OnQuit',
    ),
    DISPMETHOD(
        [dispid(254), helpstring('Fired when the window should be shown/hidden')],
        None,
        'OnVisible',
        (['in'], VARIANT_BOOL, 'Visible')
    ),
    DISPMETHOD(
        [dispid(255), helpstring('Fired when the toolbar  should be shown/hidden')],
        None,
        'OnToolBar',
        (['in'], VARIANT_BOOL, 'ToolBar')
    ),
    DISPMETHOD(
        [dispid(256), helpstring('Fired when the menubar should be shown/hidden')],
        None,
        'OnMenuBar',
        (['in'], VARIANT_BOOL, 'MenuBar')
    ),
    DISPMETHOD(
        [dispid(257), helpstring('Fired when the statusbar should be shown/hidden')],
        None,
        'OnStatusBar',
        (['in'], VARIANT_BOOL, 'StatusBar')
    ),
    DISPMETHOD(
        [dispid(258), helpstring('Fired when fullscreen mode should be on/off')],
        None,
        'OnFullScreen',
        (['in'], VARIANT_BOOL, 'FullScreen')
    ),
    DISPMETHOD(
        [dispid(260), helpstring('Fired when theater mode should be on/off')],
        None,
        'OnTheaterMode',
        (['in'], VARIANT_BOOL, 'TheaterMode')
    ),
    DISPMETHOD(
        [dispid(262), helpstring('Fired when the host window should allow/disallow resizing')],
        None,
        'WindowSetResizable',
        (['in'], VARIANT_BOOL, 'Resizable')
    ),
    DISPMETHOD(
        [dispid(264), helpstring('Fired when the host window should change its Left coordinate')],
        None,
        'WindowSetLeft',
        (['in'], c_int, 'Left')
    ),
    DISPMETHOD(
        [dispid(265), helpstring('Fired when the host window should change its Top coordinate')],
        None,
        'WindowSetTop',
        (['in'], c_int, 'Top')
    ),
    DISPMETHOD(
        [dispid(266), helpstring('Fired when the host window should change its width')],
        None,
        'WindowSetWidth',
        (['in'], c_int, 'Width')
    ),
    DISPMETHOD(
        [dispid(267), helpstring('Fired when the host window should change its height')],
        None,
        'WindowSetHeight',
        (['in'], c_int, 'Height')
    ),
    DISPMETHOD(
        [dispid(263), helpstring('Fired when the WebBrowser is about to be closed by script')],
        None,
        'WindowClosing',
        (['in'], VARIANT_BOOL, 'IsChildWindow'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(268), helpstring('Fired to request client sizes be converted to host window sizes')],
        None,
        'ClientToHostWindow',
        (['in', 'out'], POINTER(c_int), 'CX'),
        (['in', 'out'], POINTER(c_int), 'CY')
    ),
    DISPMETHOD(
        [dispid(269), helpstring('Fired to indicate the security level of the current web page contents')],
        None,
        'SetSecureLockIcon',
        (['in'], c_int, 'SecureLockIcon')
    ),
    DISPMETHOD(
        [dispid(270), helpstring('Fired to indicate the File Download dialog is opening')],
        None,
        'FileDownload',
        (['in'], VARIANT_BOOL, 'ActiveDocument'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(271), helpstring('Fired when a binding error occurs (window or frameset element).')],
        None,
        'NavigateError',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'URL'),
        (['in'], POINTER(VARIANT), 'Frame'),
        (['in'], POINTER(VARIANT), 'StatusCode'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(225), helpstring('Fired when a print template is instantiated.')],
        None,
        'PrintTemplateInstantiation',
        (['in'], POINTER(IDispatch), 'pDisp')
    ),
    DISPMETHOD(
        [dispid(226), helpstring('Fired when a print template destroyed.')],
        None,
        'PrintTemplateTeardown',
        (['in'], POINTER(IDispatch), 'pDisp')
    ),
    DISPMETHOD(
        [dispid(227), helpstring('Fired when a page is spooled. When it is fired can be changed by a custom template.')],
        None,
        'UpdatePageStatus',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'nPage'),
        (['in'], POINTER(VARIANT), 'fDone')
    ),
    DISPMETHOD(
        [dispid(272), helpstring('Fired when the global privacy impacted state changes')],
        None,
        'PrivacyImpactedStateChange',
        (['in'], VARIANT_BOOL, 'bImpacted')
    ),
    DISPMETHOD(
        [dispid(273), helpstring('A new, hidden, non-navigated WebBrowser window is needed.')],
        None,
        'NewWindow3',
        (['in', 'out'], POINTER(POINTER(IDispatch)), 'ppDisp'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel'),
        (['in'], c_ulong, 'dwFlags'),
        (['in'], BSTR, 'bstrUrlContext'),
        (['in'], BSTR, 'bstrUrl')
    ),
    DISPMETHOD(
        [dispid(282), helpstring('Fired to indicate the progress and status of the Phishing Filter analysis of the current web page')],
        None,
        'SetPhishingFilterStatus',
        (['in'], c_int, 'PhishingFilterStatus')
    ),
    DISPMETHOD(
        [dispid(283), helpstring("Fired to indicate that the browser window's visibility or enabled state has changed.")],
        None,
        'WindowStateChanged',
        (['in'], c_ulong, 'dwWindowStateFlags'),
        (['in'], c_ulong, 'dwValidFlagsMask')
    ),
    DISPMETHOD(
        [dispid(284), helpstring('A new, hidden, non-navigated process is created to handle the navigation.')],
        None,
        'NewProcess',
        (['in'], c_int, 'lCauseFlag'),
        (['in'], POINTER(IDispatch), 'pWB2'),
        (['in', 'out'], POINTER(VARIANT_BOOL), 'Cancel')
    ),
    DISPMETHOD(
        [dispid(285), helpstring('Fired when a third-party URL is blocked.')],
        None,
        'ThirdPartyUrlBlocked',
        (['in'], POINTER(VARIANT), 'URL'),
        (['in'], c_ulong, 'dwCount')
    ),
    DISPMETHOD(
        [dispid(286), helpstring('Fired when a x-domain redirect is blocked.')],
        None,
        'RedirectXDomainBlocked',
        (['in'], POINTER(IDispatch), 'pDisp'),
        (['in'], POINTER(VARIANT), 'StartURL'),
        (['in'], POINTER(VARIANT), 'RedirectURL'),
        (['in'], POINTER(VARIANT), 'Frame'),
        (['in'], POINTER(VARIANT), 'StatusCode')
    ),
    DISPMETHOD(
        [dispid(290), helpstring('Fired prior to the first script execution.')],
        None,
        'BeforeScriptExecute',
        (['in'], POINTER(IDispatch), 'pDispWindow')
    ),
    DISPMETHOD(
        [dispid(288), helpstring('Fired after a Web Worker has been started.')],
        None,
        'WebWorkerStarted',
        (['in'], c_ulong, 'dwUniqueID'),
        (['in'], BSTR, 'bstrWorkerLabel')
    ),
    DISPMETHOD(
        [dispid(289), helpstring('Fired after a Web Worker has closed')],
        None,
        'WebWorkerFinsihed',
        (['in'], c_ulong, 'dwUniqueID')
    ),
]


class DShellNameSpaceEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{55136806-B2DE-11D1-B9F2-00A0C98BC547}')
    _idlflags_ = []
    _methods_ = []

    if TYPE_CHECKING:  # dispmembers
        def FavoritesSelectionChange(self, cItems: hints.Incomplete, hItem: hints.Incomplete, strName: hints.Incomplete, strUrl: hints.Incomplete, cVisits: hints.Incomplete, strDate: hints.Incomplete, fAvailableOffline: hints.Incomplete) -> hints.Incomplete: ...
        def SelectionChange(self) -> hints.Incomplete: ...
        def DoubleClick(self) -> hints.Incomplete: ...
        def Initialized(self) -> hints.Incomplete: ...


DShellNameSpaceEvents._disp_methods_ = [
    DISPMETHOD(
        [dispid(1)],
        None,
        'FavoritesSelectionChange',
        (['in'], c_int, 'cItems'),
        (['in'], c_int, 'hItem'),
        (['in'], BSTR, 'strName'),
        (['in'], BSTR, 'strUrl'),
        (['in'], c_int, 'cVisits'),
        (['in'], BSTR, 'strDate'),
        (['in'], c_int, 'fAvailableOffline')
    ),
    DISPMETHOD([dispid(2)], None, 'SelectionChange'),
    DISPMETHOD([dispid(3)], None, 'DoubleClick'),
    DISPMETHOD([dispid(4)], None, 'Initialized'),
]


class CScriptErrorList(CoClass):
    _reg_clsid_ = GUID('{EFD01300-160F-11D2-BB2E-00805FF7EFCA}')
    _idlflags_ = ['hidden', 'noncreatable']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


CScriptErrorList._com_interfaces_ = [IScriptErrorList]


class ShellWindows(CoClass):
    """ShellDispatch Load in Shell Context"""
    _reg_clsid_ = GUID('{9BA05972-F6A8-11CF-A442-00A0C90A8F39}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


class IShellWindows(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Definition of interface IShellWindows"""
    _case_insensitive_ = True
    _iid_ = GUID('{85CB6900-4D95-11CF-960C-0080C7F4EE85}')
    _idlflags_ = ['dual', 'oleautomation']

    if TYPE_CHECKING:  # commembers
        def _get_Count(self) -> hints.Incomplete: ...
        Count = hints.normal_property(_get_Count)
        __len__ = hints.to_dunder_len(Count)
        def Item(self, index: hints.Incomplete = ...) -> hints.Incomplete: ...
        __call__ = hints.to_dunder_call(Item)
        __getitem__ = hints.to_dunder_getitem(Item)
        __setitem__ = hints.to_dunder_setitem(Item)
        def _NewEnum(self) -> hints.Incomplete: ...
        __iter__ = hints.to_dunder_iter(_NewEnum)
        def Register(self, pid: hints.Incomplete, HWND: hints.Incomplete, swClass: hints.Incomplete) -> hints.Incomplete: ...
        def RegisterPending(self, lThreadId: hints.Incomplete, pvarloc: hints.Incomplete, pvarlocRoot: hints.Incomplete, swClass: hints.Incomplete) -> hints.Incomplete: ...
        def Revoke(self, lCookie: hints.Incomplete) -> hints.Hresult: ...
        def OnNavigate(self, lCookie: hints.Incomplete, pvarloc: hints.Incomplete) -> hints.Hresult: ...
        def OnActivated(self, lCookie: hints.Incomplete, fActive: hints.Incomplete) -> hints.Hresult: ...
        def FindWindowSW(self, pvarloc: hints.Incomplete, pvarlocRoot: hints.Incomplete, swClass: hints.Incomplete, swfwOptions: hints.Incomplete) -> hints.Tuple[hints.Incomplete, hints.Incomplete]: ...
        def OnCreated(self, lCookie: hints.Incomplete, punk: hints.Incomplete) -> hints.Hresult: ...
        def ProcessAttachDetach(self, fAttach: hints.Incomplete) -> hints.Hresult: ...


class DShellWindowsEvents(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    """Event interface for IShellWindows"""
    _case_insensitive_ = True
    _iid_ = GUID('{FE4106E0-399A-11D0-A48C-00A0C90A8F39}')
    _idlflags_ = []
    _methods_ = []

    if TYPE_CHECKING:  # dispmembers
        def WindowRegistered(self, lCookie: hints.Incomplete) -> hints.Incomplete: ...
        def WindowRevoked(self, lCookie: hints.Incomplete) -> hints.Incomplete: ...


ShellWindows._com_interfaces_ = [IShellWindows]
ShellWindows._outgoing_interfaces_ = [DShellWindowsEvents]


class ShellNameSpace(CoClass):
    _reg_clsid_ = GUID('{55136805-B2DE-11D1-B9F2-00A0C98BC547}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


ShellNameSpace._com_interfaces_ = [IShellNameSpace]
ShellNameSpace._outgoing_interfaces_ = [DShellNameSpaceEvents]

DShellWindowsEvents._disp_methods_ = [
    DISPMETHOD(
        [dispid(200), helpstring('A new window was registered.')],
        None,
        'WindowRegistered',
        (['in'], c_int, 'lCookie')
    ),
    DISPMETHOD(
        [dispid(201), helpstring('A new window was revoked.')],
        None,
        'WindowRevoked',
        (['in'], c_int, 'lCookie')
    ),
]

IShellWindows._methods_ = [
    COMMETHOD(
        [dispid(1610743808), helpstring('Get count of open Shell windows'), 'propget'],
        HRESULT,
        'Count',
        (['out', 'retval'], POINTER(c_int), 'Count')
    ),
    COMMETHOD(
        [dispid(0), helpstring('Return the shell window for the given index')],
        HRESULT,
        'Item',
        (['in', 'optional'], VARIANT, 'index'),
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'Folder')
    ),
    COMMETHOD(
        [dispid(-4), helpstring('Enumerates the figures')],
        HRESULT,
        '_NewEnum',
        (['out', 'retval'], POINTER(POINTER(IUnknown)), 'ppunk')
    ),
    COMMETHOD(
        [dispid(1610743811), helpstring('Register a window with the list'), 'hidden'],
        HRESULT,
        'Register',
        (['in'], POINTER(IDispatch), 'pid'),
        (['in'], c_int, 'HWND'),
        (['in'], c_int, 'swClass'),
        (['out'], POINTER(c_int), 'plCookie')
    ),
    COMMETHOD(
        [dispid(1610743812), helpstring('Register a pending open with the list'), 'hidden'],
        HRESULT,
        'RegisterPending',
        (['in'], c_int, 'lThreadId'),
        (['in'], POINTER(VARIANT), 'pvarloc'),
        (['in'], POINTER(VARIANT), 'pvarlocRoot'),
        (['in'], c_int, 'swClass'),
        (['out'], POINTER(c_int), 'plCookie')
    ),
    COMMETHOD(
        [dispid(1610743813), helpstring('Remove a window from the list'), 'hidden'],
        HRESULT,
        'Revoke',
        (['in'], c_int, 'lCookie')
    ),
    COMMETHOD(
        [dispid(1610743814), helpstring('Notifies the new location'), 'hidden'],
        HRESULT,
        'OnNavigate',
        (['in'], c_int, 'lCookie'),
        (['in'], POINTER(VARIANT), 'pvarloc')
    ),
    COMMETHOD(
        [dispid(1610743815), helpstring('Notifies the activation'), 'hidden'],
        HRESULT,
        'OnActivated',
        (['in'], c_int, 'lCookie'),
        (['in'], VARIANT_BOOL, 'fActive')
    ),
    COMMETHOD(
        [dispid(1610743816), helpstring('Find the window based on the location'), 'hidden'],
        HRESULT,
        'FindWindowSW',
        (['in'], POINTER(VARIANT), 'pvarloc'),
        (['in'], POINTER(VARIANT), 'pvarlocRoot'),
        (['in'], c_int, 'swClass'),
        (['out'], POINTER(c_int), 'pHWND'),
        (['in'], c_int, 'swfwOptions'),
        (['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppdispOut')
    ),
    COMMETHOD(
        [dispid(1610743817), helpstring('Notifies on creation and frame name set'), 'hidden'],
        HRESULT,
        'OnCreated',
        (['in'], c_int, 'lCookie'),
        (['in'], POINTER(IUnknown), 'punk')
    ),
    COMMETHOD(
        [dispid(1610743818), helpstring('Used by IExplore to register different processes'), 'hidden'],
        HRESULT,
        'ProcessAttachDetach',
        (['in'], VARIANT_BOOL, 'fAttach')
    ),
]

################################################################
# code template for IShellWindows implementation
# class IShellWindows_Impl(object):
#     @property
#     def Count(self):
#         'Get count of open Shell windows'
#         #return Count
#
#     def Item(self, index):
#         'Return the shell window for the given index'
#         #return Folder
#
#     def _NewEnum(self):
#         'Enumerates the figures'
#         #return ppunk
#
#     def Register(self, pid, HWND, swClass):
#         'Register a window with the list'
#         #return plCookie
#
#     def RegisterPending(self, lThreadId, pvarloc, pvarlocRoot, swClass):
#         'Register a pending open with the list'
#         #return plCookie
#
#     def Revoke(self, lCookie):
#         'Remove a window from the list'
#         #return 
#
#     def OnNavigate(self, lCookie, pvarloc):
#         'Notifies the new location'
#         #return 
#
#     def OnActivated(self, lCookie, fActive):
#         'Notifies the activation'
#         #return 
#
#     def FindWindowSW(self, pvarloc, pvarlocRoot, swClass, swfwOptions):
#         'Find the window based on the location'
#         #return pHWND, ppdispOut
#
#     def OnCreated(self, lCookie, punk):
#         'Notifies on creation and frame name set'
#         #return 
#
#     def ProcessAttachDetach(self, fAttach):
#         'Used by IExplore to register different processes'
#         #return 
#


class WebBrowser(CoClass):
    """WebBrowser Control"""
    _reg_clsid_ = GUID('{8856F961-340A-11D0-A96B-00C04FD705A2}')
    _idlflags_ = ['control']
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


WebBrowser._com_interfaces_ = [IWebBrowser2, IWebBrowser]
WebBrowser._outgoing_interfaces_ = [DWebBrowserEvents2, DWebBrowserEvents]


class InternetExplorer(CoClass):
    """Internet Explorer Application."""
    _reg_clsid_ = GUID('{0002DF01-0000-0000-C000-000000000046}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}', 1, 1)


InternetExplorer._com_interfaces_ = [IWebBrowser2, IWebBrowserApp]
InternetExplorer._outgoing_interfaces_ = [DWebBrowserEvents2, DWebBrowserEvents]

__all__ = [
    'OLECMDID_SETPROGRESSPOS', 'OLECMDID_PRINTPREVIEW',
    'ShellNameSpace', 'OLECMDID_UPDATETRAVELENTRY_DATARECOVERY',
    'secureLockIconMixed', 'OLECMDID_SAVECOPYAS',
    'OLECMDID_PAGEAVAILABLE', 'OLECMDID_PROPERTIES', 'WebBrowser_V1',
    'ShellWindows', 'IShellWindows', 'IShellUIHelper4',
    'OLECMDID_PAGESETUP', 'OLECMDF', 'SecureLockIconConstants',
    'IShellNameSpace', 'OLECMDID_CLEARSELECTION', 'OLECMDID',
    'OLECMDID_STOP', 'OLECMDID_PREREFRESH',
    'OLECMDID_GETPRINTTEMPLATE', 'OLECMDF_NINCHED',
    'OLECMDID_POPSTATEEVENT', 'OLECMDID_SETFAVICON',
    'OLECMDID_SELECTALL', 'CScriptErrorList',
    'secureLockIconSecure128Bit', 'OLECMDID_DONTDOWNLOADCSS',
    'OLECMDID_PASTE', 'READYSTATE_INTERACTIVE', 'READYSTATE_COMPLETE',
    'IWebBrowser', 'SWC_BROWSER', 'OLECMDID_DELETE',
    'OLECMDID_SCROLLCOMPLETE', 'DShellWindowsEvents',
    'OLECMDID_USER_OPTICAL_ZOOM', 'OLECMDID_PROPERTYBAG2',
    'secureLockIconUnsecure', 'OLECMDID_ACTIVEXINSTALLSCOPE',
    'SWC_CALLBACK', 'OLECMDID_FOCUSVIEWCONTROLS', 'SWC_3RDPARTY',
    'OLECMDID_PAGEACTIONUIQUERY', 'OLECMDID_ONTOOLBARACTIVATED',
    'OLECMDID_SAVE', 'OLECMDID_SETPROGRESSTEXT', 'OLECMDID_UNDO',
    'IShellUIHelper8', 'secureLockIconSecureUnknownBits',
    'OLECMDID_WINDOWSTATECHANGED', 'CSC_NAVIGATEBACK',
    'SWFO_INCLUDEPENDING', 'SWC_EXPLORER',
    'ShellWindowFindWindowOptions', 'OLECMDID_UPDATEBACKFORWARDSTATE',
    'SWFO_COOKIEPASSED', 'OLECMDEXECOPT', 'SWFO_NEEDDISPATCH',
    'OLECMDID_LAYOUT_VIEWPORT_WIDTH', 'OLECMDID_UPDATETRAVELENTRY',
    'OLECMDID_UPDATEPAGESTATUS', 'OLECMDID_PRINT', 'IShellUIHelper5',
    'OLECMDF_LATCHED', 'OLECMDID_HTTPEQUIV_DONE',
    'OLECMDID_ENABLE_VISIBILITY', 'OLECMDF_SUPPORTED',
    'OLECMDID_FIND', 'secureLockIconSecure56Bit',
    'OLECMDID_GETZOOMRANGE', 'OLECMDID_ENABLE_INTERACTION',
    'IShellUIHelper2', 'OLECMDEXECOPT_DODEFAULT', 'OLECMDID_SPELL',
    'READYSTATE_LOADING', 'OLECMDID_SHOWPRINT',
    'OLECMDID_PAGEACTIONBLOCKED', 'OLECMDID_EXITFULLSCREEN',
    'DShellNameSpaceEvents', 'secureLockIconSecure40Bit',
    'ShellUIHelper', 'OLECMDID_PRINTPREVIEW2', 'IWebBrowser2',
    'OLECMDF_ENABLED', 'OLECMDID_CLOSE', 'OLECMDID_SHOWPAGESETUP',
    'DWebBrowserEvents', 'OLECMDID_VIEWPORT_MODE', 'OLECMDID_REFRESH',
    'OLECMDID_STOPDOWNLOAD', 'CSC_NAVIGATEFORWARD', 'tagREADYSTATE',
    'OLECMDID_FOCUSVIEWCONTROLSQUERY', 'OLECMDID_ZOOM',
    'InternetExplorer', 'OLECMDID_OPTICAL_ZOOM',
    'secureLockIconSecureFortezza', 'ShellWindowTypeConstants',
    'Library', 'OLECMDID_REDO', 'NewProcessCauseConstants',
    'OLECMDID_VISUAL_VIEWPORT_EXCLUDE_BOTTOM',
    'OLECMDID_PASTESPECIAL', 'ProtectedModeRedirect',
    'OLECMDEXECOPT_PROMPTUSER', 'IScriptErrorList', 'IShellUIHelper7',
    'READYSTATE_UNINITIALIZED', 'IShellUIHelper9',
    'OLECMDID_SHOWSCRIPTERROR', 'READYSTATE_LOADED',
    'IShellUIHelper3', 'IShellFavoritesNameSpace',
    'OLECMDID_ONUNLOAD', 'typelib_path',
    'OLECMDID_SHOWTASKDLG_BLOCKABLE', 'OLECMDID_HIDETOOLBARS',
    'OLECMDID_NEW', 'OLECMDID_UPDATECOMMANDS', 'OLECMDF_INVISIBLE',
    'OLECMDID_SHOWTASKDLG', 'OLECMDID_ADDTRAVELENTRY',
    'OLECMDID_SETTITLE', 'OLECMDEXECOPT_SHOWHELP',
    'OLECMDID_SHOWPAGEACTIONMENU', 'SWC_DESKTOP',
    'OLECMDID_UPDATE_CARET', 'OLECMDID_SET_HOST_FULLSCREENMODE',
    'OLECMDID_HTTPEQUIV', 'OLECMDID_ALLOWUILESSSAVEAS',
    'OLECMDID_SETPROGRESSMAX', 'IShellUIHelper', 'IShellUIHelper6',
    'WebBrowser', 'OLECMDID_SHOWMESSAGE', 'OLECMDID_SHOWFIND',
    'OLECMDF_DEFHIDEONCTXTMENU', 'OLECMDID_COPY', 'IWebBrowserApp',
    'OLECMDEXECOPT_DONTPROMPTUSER', 'CSC_UPDATECOMMANDS',
    'OLECMDID_OPEN', 'OLECMDID_SAVEAS', 'OLECMDID_CUT',
    'OLECMDID_PRINT2', 'OLECMDID_GETUSERSCALABLE',
    'OLECMDID_MEDIA_PLAYBACK', 'OLECMDID_SETPRINTTEMPLATE',
    'InternetExplorerMedium', 'OLECMDID_OPTICAL_GETZOOMRANGE',
    'DWebBrowserEvents2', 'OLECMDID_ONBEFOREUNLOAD',
    'OLECMDID_SETDOWNLOADSTATE', 'OLECMDID_SHOWMESSAGE_BLOCKABLE',
    'CommandStateChangeConstants', 'ShellBrowserWindow'
]

_check_version('1.4.11', 1757470665.724663)

