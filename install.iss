[Setup]
AppName=Universal Media Archiver
AppVersion=1.0.0
DefaultDirName={autopf}\Universal Media Archiver
SetupIconFile=assets\app_icon.ico

[Files]
Source: "dist\UniversalMediaArchiver.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\Universal Media Archiver"; Filename: "{app}\UniversalMediaArchiver.exe"