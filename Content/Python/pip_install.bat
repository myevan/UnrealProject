@echo off
call %~dp0..\..\Build\BatchFiles\UE4Environ.bat || exit /b 1
%UE_DIR%\Engine\Binaries\ThirdParty\Python3\Win64\python.exe -m pip install -t %~dp0\pb\platforms\Python-3.7.7-Windows %*