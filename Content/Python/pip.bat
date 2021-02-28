@echo off
call %~dp0..\..\Build\BatchFiles\UE4Environ.bat || exit /b 1
%UE_DIR%\Engine\Binaries\ThirdParty\Python3\Win64\python.exe -m pip %*