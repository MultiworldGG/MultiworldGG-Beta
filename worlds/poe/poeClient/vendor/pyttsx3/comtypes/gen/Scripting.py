from enum import IntFlag

import comtypes.gen._420B2830_E718_11CF_893D_00A0C9054228_0_1_0 as __wrapper_module__
from comtypes.gen._420B2830_E718_11CF_893D_00A0C9054228_0_1_0 import (
    IFolderCollection, BSTR, IDictionary, TristateUseDefault, Volume,
    IFolder, IFileCollection, File, TextStream, COMMETHOD, Folder,
    IDriveCollection, Removable, typelib_path, VARIANT, Hidden,
    helpstring, Dictionary, ForReading, _lcid, ForAppending,
    TextCompare, DatabaseCompare, CDRom, FileSystemObject, Files,
    Directory, IScriptEncoder, _check_version, CoClass, SystemFolder,
    Encoder, ITextStream, Alias, Drives, UnknownType, ReadOnly,
    WindowsFolder, Normal, Drive, dispid, StdIn, StdErr, Compressed,
    GUID, Archive, StdOut, TristateMixed, HRESULT, ForWriting,
    TemporaryFolder, TristateTrue, Remote, RamDisk, Folders, IUnknown,
    IDrive, Fixed, IFileSystem, BinaryCompare, System, Library,
    TristateFalse, VARIANT_BOOL, IFile, IFileSystem3
)


class __MIDL___MIDL_itf_scrrun_0001_0001_0003(IntFlag):
    StdIn = 0
    StdOut = 1
    StdErr = 2


class __MIDL___MIDL_itf_scrrun_0001_0001_0001(IntFlag):
    UnknownType = 0
    Removable = 1
    Fixed = 2
    Remote = 3
    CDRom = 4
    RamDisk = 5


class __MIDL___MIDL_itf_scrrun_0000_0000_0001(IntFlag):
    Normal = 0
    ReadOnly = 1
    Hidden = 2
    System = 4
    Volume = 8
    Directory = 16
    Archive = 32
    Alias = 1024
    Compressed = 2048


class __MIDL___MIDL_itf_scrrun_0001_0001_0002(IntFlag):
    WindowsFolder = 0
    SystemFolder = 1
    TemporaryFolder = 2


class IOMode(IntFlag):
    ForReading = 1
    ForWriting = 2
    ForAppending = 8


class Tristate(IntFlag):
    TristateTrue = -1
    TristateFalse = 0
    TristateUseDefault = -2
    TristateMixed = -2


class CompareMethod(IntFlag):
    BinaryCompare = 0
    TextCompare = 1
    DatabaseCompare = 2


DriveTypeConst = __MIDL___MIDL_itf_scrrun_0001_0001_0001
FileAttribute = __MIDL___MIDL_itf_scrrun_0000_0000_0001
SpecialFolderConst = __MIDL___MIDL_itf_scrrun_0001_0001_0002
StandardStreamTypes = __MIDL___MIDL_itf_scrrun_0001_0001_0003


__all__ = [
    'ReadOnly', 'WindowsFolder',
    '__MIDL___MIDL_itf_scrrun_0000_0000_0001', 'Normal', 'Drive',
    'IFolderCollection', 'Tristate', 'CompareMethod', 'StdIn',
    'StdErr', 'IDictionary', 'Compressed', 'Volume', 'IFolder',
    'TristateUseDefault', 'Archive', 'StdOut', 'IFileCollection',
    '__MIDL___MIDL_itf_scrrun_0001_0001_0001', 'IOMode',
    'TristateMixed', 'File', 'Folder', 'IDriveCollection',
    'TextStream', 'ForWriting', 'Removable', 'TemporaryFolder',
    'TristateTrue', 'typelib_path', 'Hidden', 'DriveTypeConst',
    'Remote', '__MIDL___MIDL_itf_scrrun_0001_0001_0003', 'RamDisk',
    'StandardStreamTypes', 'Folders', 'Dictionary', 'IDrive',
    'ForReading', 'ForAppending', 'TextCompare', 'Fixed', 'CDRom',
    'FileSystemObject', 'IFileSystem', 'Directory', 'FileAttribute',
    'BinaryCompare', 'DatabaseCompare', 'Files', 'IScriptEncoder',
    '__MIDL___MIDL_itf_scrrun_0001_0001_0002', 'SystemFolder',
    'System', 'SpecialFolderConst', 'Encoder', 'ITextStream', 'Alias',
    'Library', 'Drives', 'TristateFalse', 'IFile', 'IFileSystem3',
    'UnknownType'
]

