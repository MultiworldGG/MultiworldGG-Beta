from enum import IntFlag

import comtypes.gen._0002E157_0000_0000_C000_000000000046_0_5_3 as __wrapper_module__
from comtypes.gen._0002E157_0000_0000_C000_000000000046_0_5_3 import (
    References, Property, vbext_wt_MainWindow, vbext_wt_Browser, BSTR,
    vbext_ct_Document, vbext_wt_Find, _dispVBComponentsEvents,
    vbextFileTypeModule, VBComponent, IDispatch, Properties,
    Components, Events, vbextFileTypeProject, vbextFileTypeForm,
    _VBProject_Old, vbextFileTypeDesigners, AddIn, vbextFileTypeExe,
    COMMETHOD, typelib_path, VARIANT, vbext_pk_Let, CodePane,
    vbext_wt_CodeWindow, Window, vbext_pk_Get, Component,
    vbext_wt_Immediate, _Components, _Component, ProjectTemplate,
    _VBProjectsEvents, _dispReferencesEvents, vbext_pp_locked, _lcid,
    vbext_vm_Design, _VBComponent, vbextFileTypeClass, VBComponents,
    CommandBarEvents, _check_version, CodeModule, vbext_wt_Designer,
    CoClass, vbext_ct_ActiveXDesigner, _dispReferences_Events,
    vbext_pk_Proc, vbext_ws_Maximize, _CommandBarControlEvents,
    vbext_wt_PropertyWindow, vbext_ws_Minimize, vbext_pp_none,
    _LinkedWindows, _CodePane, VBE, Addins, _Windows_old,
    _VBComponent_Old, vbextFileTypeDocObject, _CodePanes, VBProjects,
    vbext_cv_ProcedureView, dispid, vbext_ws_Normal,
    vbext_wt_ProjectWindow, vbext_wt_Toolbox, vbextFileTypeFrx, GUID,
    _VBComponents_Old, HRESULT, _VBComponents, vbext_vm_Run,
    vbext_cv_FullModuleView, _ReferencesEvents, vbext_wt_Locals,
    vbext_pt_StandAlone, vbextFileTypeRes, _VBComponentsEvents,
    LinkedWindows, _References, _AddIns, _VBProject,
    SelectedComponents, DISPMETHOD, CodePanes, ReferencesEvents,
    _dispVBProjectsEvents, vbext_rk_Project, IUnknown, _CodeModule,
    _VBProjects_Old, vbextFileTypeUserControl, vbext_ct_MSForm,
    vbext_pk_Set, _dispCommandBarControlEvents, Reference,
    vbextFileTypeBinary, vbext_wt_ToolWindow, _Properties,
    vbext_pt_HostProject, Windows, vbext_ct_StdModule,
    vbextFileTypePropertyPage, vbext_vm_Break, vbext_wt_Watch,
    vbextFileTypeGroupProject, _Windows, vbext_ct_ClassModule,
    vbext_wt_FindReplace, vbext_rk_TypeLib, _ProjectTemplate,
    Application, Library, VARIANT_BOOL, _VBProjects, VBProject,
    vbext_wt_LinkedWindowFrame
)


class vbext_ComponentType(IntFlag):
    vbext_ct_StdModule = 1
    vbext_ct_ClassModule = 2
    vbext_ct_MSForm = 3
    vbext_ct_ActiveXDesigner = 11
    vbext_ct_Document = 100


class vbext_CodePaneview(IntFlag):
    vbext_cv_ProcedureView = 0
    vbext_cv_FullModuleView = 1


class vbext_WindowType(IntFlag):
    vbext_wt_CodeWindow = 0
    vbext_wt_Designer = 1
    vbext_wt_Browser = 2
    vbext_wt_Watch = 3
    vbext_wt_Locals = 4
    vbext_wt_Immediate = 5
    vbext_wt_ProjectWindow = 6
    vbext_wt_PropertyWindow = 7
    vbext_wt_Find = 8
    vbext_wt_FindReplace = 9
    vbext_wt_Toolbox = 10
    vbext_wt_LinkedWindowFrame = 11
    vbext_wt_MainWindow = 12
    vbext_wt_ToolWindow = 15


class vbextFileTypes(IntFlag):
    vbextFileTypeForm = 0
    vbextFileTypeModule = 1
    vbextFileTypeClass = 2
    vbextFileTypeProject = 3
    vbextFileTypeExe = 4
    vbextFileTypeFrx = 5
    vbextFileTypeRes = 6
    vbextFileTypeUserControl = 7
    vbextFileTypePropertyPage = 8
    vbextFileTypeDocObject = 9
    vbextFileTypeBinary = 10
    vbextFileTypeGroupProject = 11
    vbextFileTypeDesigners = 12


class vbext_ProjectType(IntFlag):
    vbext_pt_HostProject = 100
    vbext_pt_StandAlone = 101


class vbext_RefKind(IntFlag):
    vbext_rk_TypeLib = 0
    vbext_rk_Project = 1


class vbext_VBAMode(IntFlag):
    vbext_vm_Run = 0
    vbext_vm_Break = 1
    vbext_vm_Design = 2


class vbext_ProjectProtection(IntFlag):
    vbext_pp_none = 0
    vbext_pp_locked = 1


class vbext_ProcKind(IntFlag):
    vbext_pk_Proc = 0
    vbext_pk_Let = 1
    vbext_pk_Set = 2
    vbext_pk_Get = 3


class vbext_WindowState(IntFlag):
    vbext_ws_Normal = 0
    vbext_ws_Minimize = 1
    vbext_ws_Maximize = 2


__all__ = [
    'Property', 'vbext_wt_MainWindow', 'vbext_wt_Browser',
    'vbext_ct_Document', '_dispVBComponentsEvents',
    'vbextFileTypeModule', 'Properties', 'Components', 'Events',
    'vbextFileTypeProject', 'vbextFileTypeForm', '_VBProject_Old',
    'vbextFileTypeExe', 'vbext_WindowState', 'vbext_WindowType',
    'vbext_VBAMode', 'vbext_pk_Let', 'CodePane',
    'vbext_wt_CodeWindow', 'Window', 'Component', '_Components',
    '_VBComponent', 'CommandBarEvents', 'vbext_wt_LinkedWindowFrame',
    'vbext_wt_Designer', '_dispReferences_Events',
    'vbext_ws_Maximize', '_CommandBarControlEvents', 'VBE',
    '_Windows_old', '_VBComponent_Old', '_CodePanes', 'VBProjects',
    'vbext_RefKind', 'vbext_ws_Normal', 'vbext_wt_ProjectWindow',
    'vbext_vm_Run', '_ReferencesEvents', 'vbextFileTypeRes',
    'LinkedWindows', '_References', '_AddIns', 'ReferencesEvents',
    'vbext_pk_Set', '_dispCommandBarControlEvents', 'Windows',
    'vbext_ct_StdModule', 'vbextFileTypePropertyPage',
    'vbextFileTypeGroupProject', 'vbext_ct_ClassModule', 'Library',
    '_VBProjects', 'VBProject', '_dispVBProjectsEvents', 'References',
    'vbext_wt_Find', 'VBComponent', 'vbextFileTypeDesigners', 'AddIn',
    'vbext_ProjectType', 'typelib_path', 'vbext_pk_Get',
    'vbext_wt_Immediate', '_Component', 'vbext_CodePaneview',
    'ProjectTemplate', '_VBProjectsEvents', '_dispReferencesEvents',
    'vbext_pp_locked', 'vbext_vm_Design', 'vbextFileTypeClass',
    'VBComponents', 'CodeModule', 'vbext_ct_ActiveXDesigner',
    'vbext_ProjectProtection', 'vbext_pk_Proc',
    'vbext_wt_PropertyWindow', 'vbext_ws_Minimize', 'vbext_pp_none',
    'vbext_ProcKind', '_LinkedWindows', '_CodePane', 'Addins',
    'vbextFileTypeDocObject', 'vbext_cv_ProcedureView',
    'vbext_wt_Toolbox', 'vbextFileTypeFrx', '_VBComponents_Old',
    '_VBComponents', 'vbext_cv_FullModuleView', 'vbext_wt_Locals',
    'vbext_pt_StandAlone', '_VBComponentsEvents', '_VBProject',
    'SelectedComponents', 'CodePanes', 'vbext_rk_Project',
    '_CodeModule', '_VBProjects_Old', 'vbextFileTypeUserControl',
    'vbext_ct_MSForm', 'Reference', 'vbextFileTypeBinary',
    'vbext_wt_ToolWindow', '_Properties', 'vbext_vm_Break',
    'vbext_wt_Watch', '_Windows', 'vbext_wt_FindReplace',
    'vbext_rk_TypeLib', 'vbextFileTypes', '_ProjectTemplate',
    'Application', 'vbext_ComponentType', 'vbext_pt_HostProject'
]

