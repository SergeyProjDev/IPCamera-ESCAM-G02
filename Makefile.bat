@echo off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)



set newline=^& echo.
call :ColorText 0a "#PROGRAM STARTED" %newline%

@for /f "tokens=1 delims=." %%i in ('dir /B /d *.py') do (
	set file= %%i
)



echo.
py %file%.py
echo.


PAUSE



:ColorText
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1