[Setup]
AppName=UniversalMediaArchiver
AppVersion=1.0.0
DefaultDirName={autopf}\UniversalMediaArchiver
SetupIconFile=assets\app_icon.ico

[Files]
Source: "dist\UniversalMediaArchiver.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\UniversalMediaArchiver"; Filename: "{app}\UniversalMediaArchiver.exe"