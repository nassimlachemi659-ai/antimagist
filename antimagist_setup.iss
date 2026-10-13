; ==============================================================================
; ANTIMAGIST ENTERPRISE SECURITY V2 PRO — INNO SETUP MASTER INSTALLER SCRIPT
; ==============================================================================
; Generates: Antimagist_Setup_v2.0_Pro.exe
; Features:
; - Modern dark wizard styling with custom branding
; - Automatic Windows Startup shortcut (optional)
; - Desktop & Start Menu Program Group shortcuts
; - Windows Context Menu Shell Extensions registration
; - Full Windows Uninstaller with clean registry and temporary file removal
; - Built-in prerequisite detection (Windows 10/11 64-Bit)
; ==============================================================================

#define MyAppName "Antimagist Enterprise Security V11"
#define MyAppVersion "11.0.0-OmniWorkstation"
#define MyAppPublisher "Antimagist AI Security Group"
#define MyAppURL "https://github.com/nassimlachemi659-ai/antimagist"
#define MyAppExeName "Antimagist.exe"

[Setup]
AppId={{8B1948B2-1D47-49D6-B7E2-6C45E8F79B12}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Antimagist
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=release
OutputBaseFilename=Antimagist_Setup_v11.0_OmniWorkstation
SetupIconFile=antimagist.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Launch Antimagist Sentinel silently on Windows Startup"; GroupDescription: "Background Protection:"; Flags: unchecked

[Files]
Source: "dist\Antimagist_V4_Apex\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "website\*"; DestDir: "{app}\website"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "antimagist.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\antimagist.ico"
Name: "{group}\{#MyAppName} Web Dashboard"; Filename: "{app}\website\dashboard.html"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\antimagist.ico"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--minimized"; IconFilename: "{app}\antimagist.ico"; Tasks: startupicon

[Registry]
; Windows Run key (optional background boot)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "AntimagistSentinel"; ValueData: """{app}\{#MyAppExeName}"" --minimized"; Flags: uninsdeletevalue; Tasks: startupicon

; Antimagist Local Configuration Key
Root: HKLM; Subkey: "Software\Antimagist"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Antimagist"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Antimagist"; ValueType: dword; ValueName: "ProLicensed"; ValueData: 1; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
