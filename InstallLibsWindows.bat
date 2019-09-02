@echo off

set /p u_name="Enter your user name:  " %newline%

set newline=^& echo.
echo #IMPORT TO SCRIPTS %newline%
cd C:\Users\%u_name%\AppData\Local\Programs\Python\Python37-32\Scripts
echo   C:\Users\%u_name%\AppData\Local\Programs\Python\Python37-32\Scripts
echo.
:start

python -m pip install --upgrade pip
pip install opencv-python
pip install keyboard
pip install pygame
pip install requests

PAUSE