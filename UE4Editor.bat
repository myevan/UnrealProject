@echo off
call %~dp0Build\BatchFiles\UE4Environ.bat || exit /b 1
start %UE_DIR%\Engine\Binaries\Win64\UE4Editor.exe %~dp0%PRJ_NAME%.uproject