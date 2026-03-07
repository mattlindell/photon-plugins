@echo off
REM Windows wrapper for running hook scripts
REM Usage: run-hook.cmd <script-name.sh>

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_NAME=%~1"

if "%SCRIPT_NAME%"=="" (
    echo Error: No script specified
    exit /b 1
)

REM Try bash first (Git Bash, WSL, etc.)
where bash >nul 2>&1
if %ERRORLEVEL%==0 (
    bash "%SCRIPT_DIR%%SCRIPT_NAME%"
    exit /b %ERRORLEVEL%
)

REM Try sh (MSYS, MinGW)
where sh >nul 2>&1
if %ERRORLEVEL%==0 (
    sh "%SCRIPT_DIR%%SCRIPT_NAME%"
    exit /b %ERRORLEVEL%
)

REM No shell found - output minimal JSON
echo {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Technical Director active. Shell not available for full initialization."}}

exit /b 0