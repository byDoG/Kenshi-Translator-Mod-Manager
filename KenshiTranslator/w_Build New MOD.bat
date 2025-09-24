@echo off
chcp 65001 >nul
title Build KT-Setup.exe
mode con: cols=80 lines=20
echo ================================
echo   Building KT-Setup.exe
echo ================================

:: Clean old builds
rmdir /s /q build dist >nul 2>&1
del KT-Setup.spec >nul 2>&1
del KT-Setup.exe >nul 2>&1

:: Check if icon.ico exists
if not exist icons\icon.ico (
    echo [ERROR] icons\icon.ico not found!
    pause
    exit /b
)

:: Check if version file exists
if not exist info.txt (
    echo [ERROR] info.txt not found!
    pause
    exit /b
)

:: Build exe with files packed inside
pyinstaller --onefile --noconsole ^
 --icon=icons\icon.ico ^
 --version-file=info.txt ^
 --add-data "KenshiTranslator.exe;." ^
 --add-data "LICENSE.md;." ^
 --add-data "icons;icons" ^
 KT-Setup.py

:: Move result to current folder
if exist dist\KT-Setup.exe (
    move /Y dist\KT-Setup.exe . >nul
)

:: Cleanup
rmdir /s /q build dist >nul 2>&1
del KT-Setup.spec >nul 2>&1

echo.
echo [OK] Build completed!
echo Output file: KT-Setup.exe

timeout /t 2 >nul
exit
