@echo off
if "%UE-SharedDataCachePath%" == "" goto not_found_ddc_env
if not exist %UE-SharedDataCachePath% goto not_found_ddc_dir

call %~dp0Build\BatchFiles\UE4Environ.bat || exit /b 1
start %UE_DIR%\Engine\Binaries\Win64\UE4Editor.exe %~dp0%PRJ_NAME%.uproject -SkipCompile %*
goto finish

:not_found_ddc_env
echo NOT_FOUND_DDC_ENVIRONMENT_VARIABLE: UE-SharedDataCachePath
pause
exit /b 2

:not_found_ddc_dir
echo NOT_FOUND_DDC_DIRECTORY: %UE-SharedDataCachePath%
pause
exit /b 3

:finish