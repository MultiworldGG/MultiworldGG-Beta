#define source_path ReadIni(SourcePath + "\setup.ini", "Data", "source_path")
#define min_windows ReadIni(SourcePath + "\setup.ini", "Data", "min_windows")

#define MyAppName "MultiworldGG-AlphaGUI"
#define MyAppExeName "MultiworldGG.exe"
#define MyAppIcon "data/icon.ico"
#dim VersionTuple[4]
#define MyAppVersion GetVersionComponents(source_path + '\MultiworldGG.exe', VersionTuple[0], VersionTuple[1], VersionTuple[2], VersionTuple[3])
#define MyAppVersionText Str(VersionTuple[0])+"."+Str(VersionTuple[1])+"."+Str(VersionTuple[2])


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{918BA46A-FAB8-460C-9DFF-AE691E1C865E}}
AppName={#MyAppName}
AppCopyright=Distributed under GPLv3 License
AppVerName={#MyAppName} {#MyAppVersionText}
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
DefaultGroupName=MultiworldGG-AlphaGUI
OutputDir=setups
OutputBaseFilename=Setup {#MyAppName} {#MyAppVersionText}
Compression=lzma2
SolidCompression=yes
LZMANumBlockThreads=8
ArchitecturesInstallIn64BitMode=x64compatible arm64
ChangesAssociations=yes
ArchitecturesAllowed=x64compatible arm64
AllowNoIcons=yes
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=docs\combined_license_inno.txt
WizardStyle= modern
SetupLogging=yes
MinVersion={#min_windows}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}";

[Types]
Name: "full"; Description: "Full installation"
Name: "minimal"; Description: "Minimal installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Dirs]
NAME: "{app}"; Flags: setntfscompression; Permissions: everyone-modify users-modify authusers-modify;

[Files]
Source: "{#source_path}\*"; Excludes: "*.sfc, *.log, data\sprites\alttp, SNI, EnemizerCLI"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#source_path}\SNI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\SNI"; Flags: ignoreversion recursesubdirs createallsubdirs;
;Source: "{#source_path}\EnemizerCLI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\EnemizerCLI"; Flags: ignoreversion recursesubdirs createallsubdirs;
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall
Source: "python-3.12.10-amd64.exe"; DestDir: {tmp}; Flags: deleteafterinstall; Check: IsPythonNeeded and IsX64
Source: "python-3.12.10-arm64.exe"; DestDir: {tmp}; Flags: deleteafterinstall; Check: IsPythonNeeded and IsARM64

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName} Launcher"; Filename: "{app}\MultiworldGG.exe"

Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName} Launcher"; Filename: "{app}\MultiworldGG.exe"; Tasks: desktopicon

[Run]

Filename: "{tmp}\python-3.12.10-amd64.exe"; Parameters: "/passive InstallAllUsers=1 PrependPath=1 Include_test=0"; Check: IsPythonNeeded and IsX64; StatusMsg: "Installing Python 3.12.10..."
Filename: "{tmp}\python-3.12.10-arm64.exe"; Parameters: "/passive InstallAllUsers=1 PrependPath=1 Include_test=0"; Check: IsPythonNeeded and IsARM64; StatusMsg: "Installing Python 3.12.10..."
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."
; Filename: "{app}\MultiworldGGLauncher"; Parameters: "--update_settings"; StatusMsg: "Updating host.yaml..."; Flags: runasoriginaluser runhidden
; Filename: "{app}\MultiworldGGLauncher"; Description: "{cm:LaunchProgram,{#StringChange('Launcher', '&', '&&')}}"; Flags: nowait postinstall skipifsilent
; Silent install from updater auto starts the launcher again
; Filename: "{app}\MultiworldGG"; StatusMsg: "MultiworldGG ... done"; Flags: nowait skipifnotsilent


[UninstallDelete]
Type: dirifempty; Name: "{app}"

[InstallDelete]
Type: files; Name: "{app}\*.exe"
Type: files; Name: "{app}\data\lua\connector_pkmn_rb.lua"
Type: files; Name: "{app}\data\lua\connector_ff1.lua"
Type: filesandordirs; Name: "{app}\SNI\lua*"
Type: filesandordirs; Name: "{app}\EnemizerCLI*"
#include "installdelete.iss"

[Registry]

[Code]
// See: https://stackoverflow.com/a/51614652/2287576
function IsVCRedist64BitNeeded(): boolean;
var
  strVersion: string;
begin
  if (RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Version', strVersion)) then
  begin
    // Is the installed version at least the packaged one ?
    Log('VC Redist x64 Version : found ' + strVersion);
    Result := (CompareStr(strVersion, 'v14.38.33130') < 0);
  end
  else
  begin
    // Not even an old version installed
    Log('VC Redist x64 is not already installed');
    Result := True;
  end;
end;

function ShouldShowDeleteLibTask: Boolean;
begin
  Result := DirExists(ExpandConstant('{app}\lib'));
end;

function IsPythonInstalled: Boolean;
var
  ResultCode: Integer;
  Output: TExecOutput;
begin
  Result := False;
  
  Log('Checking for Python installation...');
  
  // Method 1: Check if 'python' command works and has pip
  if Exec('python', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
  begin
    Log('Python found in PATH via python command');
    // Check if pip is available
    if Exec('python', '-m pip --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    begin
      Log('Python and pip are ready via python command');
      Result := True;
      Exit;
    end
    else
      Log('Python found but pip not available via python command');
  end;
  
  // Method 2: Use Windows Python Launcher
  if Exec('py', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
  begin
    Log('Python found via Windows Python Launcher (py)');
    // Check if pip is available
    if Exec('py', '-m pip --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    begin
      Log('Python and pip are ready via py command');
      Result := True;
      Exit;
    end
    else
      Log('Python found but pip not available via py command');
  end;
  
  // Method 3: Use 'where python' to find all python executables
  if ExecAndCaptureOutput('cmd.exe', '/c where python', '', SW_HIDE, ewWaitUntilTerminated, ResultCode, Output) then
  begin
    if GetArrayLength(Output.StdOut) > 0 then
      Log('where python output: ' + Output.StdOut[0]);
    // Check if output contains actual python paths (not just Windows Store aliases)
    if (GetArrayLength(Output.StdOut) > 0) and (Pos('python.exe', Output.StdOut[0]) > 0) and (Pos('WindowsApps', Output.StdOut[0]) = 0) then
    begin
      Log('Real Python executables found via where command');
      // Try to use the first python found
      if Exec('python', '-m pip --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
      begin
        Log('Python and pip are ready via where-found python');
        Result := True;
        Exit;
      end;
    end
    else
      Log('Only Windows Store Python aliases found via where command');
  end;
  
  // Method 4: Use 'py -0p' to list installed Python executables
  if ExecAndCaptureOutput('py', '-0p', '', SW_HIDE, ewWaitUntilTerminated, ResultCode, Output) then
  begin
    if GetArrayLength(Output.StdOut) > 0 then
      Log('py -0p output: ' + Output.StdOut[0]);
    // Check if output contains actual python paths
    if (GetArrayLength(Output.StdOut) > 0) and (Pos('python.exe', Output.StdOut[0]) > 0) then
    begin
      Log('Python installations found via py -0p');
      // Try to use py launcher with pip
      if Exec('py', '-m pip --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
      begin
        Log('Python and pip are ready via py launcher');
        Result := True;
        Exit;
      end;
    end
    else
      Log('No Python installations found via py -0p');
  end;
  
  if not Result then
    Log('No suitable Python installation (3.8+ with pip) found');
end;

function IsPythonNeeded: Boolean;
begin
  Result := not IsPythonInstalled;
end;

function IsX64: Boolean;
begin
  Result := Is64BitInstallMode and (ProcessorArchitecture = paX64);
end;

function IsARM64: Boolean;
begin
  Result := Is64BitInstallMode and (ProcessorArchitecture = paARM64);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
  begin
    if WizardIsTaskSelected('deletelib') then
      DelTree(ExpandConstant('{app}\lib'), True, True, True);
  end;
end;
