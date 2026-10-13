#define MyAppName "DownloadVideo"
#define MyAppVersion "1.0.1"
#define MyAppExeName "DownloadVideo.exe"

[Setup]
AppId={{B812916D-45F6-48F9-9774-6F4C915B61D1}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}

DefaultDirName={autopf}\DownloadVideo
DefaultGroupName={#MyAppName}

OutputDir=release
OutputBaseFilename=DownloadVideo-Setup-v{#MyAppVersion}

SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible


[Files]
Source: "dist\DownloadVideo.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{autoprograms}\DownloadVideo"; Filename: "{app}\DownloadVideo.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\DownloadVideo"; Filename: "{app}\DownloadVideo.exe"; WorkingDir: "{app}"


[Run]
Filename: "{app}\DownloadVideo.exe"; Description: "DownloadVideo'yu çalıştır"; Flags: nowait postinstall skipifsilent