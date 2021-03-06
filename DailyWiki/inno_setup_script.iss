; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "DailyWiki"
#define MyAppVersion "1.0"
#define MyAppPublisher "Vincent Papelard"
#define MyAppURL "https://www.vincentpapelard.com"
#define MyAppExeName "DailyWiki.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B1238AF5-8EAC-407A-A670-3DD1B5DE0AF2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=DailyWiki_setup
Compression=lzma
SetupIconFile=wikipedia_iconblack.ico
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\vincent\Desktop\Windows\src\build\exe.win-amd64-3.9\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\vincent\Desktop\Windows\src\build\exe.win-amd64-3.9\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\vincent\Desktop\src\conf\*"; DestDir: "{app}\conf"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\vincent\Desktop\src\logs\*"; DestDir: "{app}\logs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\vincent\Desktop\src\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "DailyWiki"; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Policies\Microsoft\Windows\Explorer"; ValueType: dword; ValueName: "EnableLegacyBalloonNotifications"; ValueData: 1;


[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser

