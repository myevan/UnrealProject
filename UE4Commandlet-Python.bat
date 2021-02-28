@echo off
setlocal
set UE-EditorOverride=UE4Editor-Cmd.exe
call %~dp0UE4Editor.bat -Run=PythonScript -Script=%*