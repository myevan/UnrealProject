@echo off

for %%i in ("%~dp0..\..\") do set "PRJ_DIR=%%~fi"
for %%i in ("%~dp0..\..") do set "PRJ_NAME=%%~ni"
set PRJ_FILE=%PRJ_DIR%%PRJ_NAME%.uproject

for %%i in ("%~dp0..\..\..\UE_4.git") do set "UE_GIT_DIR=%%~fi"
if exist %UE_GIT_DIR% (
	echo found UE_4.git: %UE_GIT_DIR%
	set UE_DIR=%UE_GIT_DIR%
	goto finish
)

for %%i in ("%~dp0..\..\..\UE_4.svn") do set "UE_SVN_DIR=%%~fi"
if exist %UE_SVN_DIR% (
	echo found UE_4.svn: %UE_GIT_DIR% 
	set UE_DIR=%UE_SVN_DIR%
	goto finish
)

for /f "tokens=2" %%i in ('findstr EngineAssociation %PRJ_FILE%') do set "PRJ_GUID_TOKEN=%%i"
set PRJ_GUID=%PRJ_GUID_TOKEN:~1,-2%

set REG_NAME=%PRJ_GUID%
set REG_PATH="HKEY_CURRENT_USER\Software\Epic Games\Unreal Engine\Builds"
for /F "usebackq tokens=3" %%i IN (`reg query %REG_PATH% /v %REG_NAME% 2^>nul ^| find "%REG_NAME%"`) do (
	echo found UE_4.registered: %%i
	set UE_DIR=%%i
	goto finish
)

set REG_PATH2="HKEY_LOCAL_MACHINE\SOFTWARE\EpicGames\Unreal Engine\%REG_NAME%"
for /F "usebackq tokens=3" %%i IN (`reg query %REG_PATH2% /v InstalledDirectory 2^>nul ^| find "InstalledDirectory"`) do (
	echo found UE_4.public: %%i
	set UE_DIR=%%i
	goto finish
)

:error
echo NOT_FOUND_UE4
echo --------------------
echo * git: %UE_GIT_DIR%
echo * svn: %UE_SVN_DIR%
echo * guid: %PRJ_GUID%
exit /b 1

:finish
exit /b 0