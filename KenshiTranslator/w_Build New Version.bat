@echo off
setlocal
set NAME=KenshiTranslator
set VERSION=v1.0.2
set TARGET_DIR=%cd%

title Build %NAME% %VERSION%
mode con: cols=60 lines=20

echo ================================
echo   BUILD %NAME% %VERSION% STARTED
echo ================================
echo.

:: Cleanup old files
echo [INFO] Cleaning old files...
rmdir /s /q build dist __pycache__ >nul 2>&1
del *.spec >nul 2>&1
del "%NAME%.exe" >nul 2>&1
del "warn-%NAME%.txt" >nul 2>&1
del "xref-%NAME%.html" >nul 2>&1
del "%NAME%*.hash.txt" >nul 2>&1
echo [OK] Cleanup done
echo.

:: Build EXE
echo [INFO] Running PyInstaller...
pyinstaller --onefile --noconsole ^
 --name "%NAME%" ^
 --icon "%cd%\icons\icon.ico" ^
 --version-file "%cd%\info.txt" ^
 --hidden-import steam_mods ^
 --hidden-import local_mods ^
 --hidden-import order_mods ^
 --hidden-import run_kenshi ^
 "%NAME%.py"

:: Check result
if exist "dist\%NAME%.exe" (
    echo [OK] Build successful
) else (
    echo [ERROR] Build failed! Check logs.
    timeout /t 5 >nul
    exit /b
)

:: Move EXE
echo [INFO] Moving EXE to %TARGET_DIR%
move /Y "dist\%NAME%.exe" "%TARGET_DIR%\%NAME%.exe" >nul
echo [OK] %NAME%.exe moved to %TARGET_DIR%

:: Generate SHA256 hash (имя с версией)
echo [INFO] Calculating SHA256 hash...
certutil -hashfile "%TARGET_DIR%\%NAME%.exe" SHA256 > "%TARGET_DIR%\KT_%VERSION%.hash.txt"
echo [OK] Hash saved to KT_%VERSION%.hash.txt

:: Final cleanup
echo [INFO] Removing temp files...
rmdir /s /q build dist __pycache__ >nul 2>&1
del *.spec >nul 2>&1
del "warn-%NAME%.txt" >nul 2>&1
del "xref-%NAME%.html" >nul 2>&1
echo [OK] Temp files removed
echo.

echo ================================
echo   BUILD FINISHED SUCCESSFULLY
echo ================================
echo.

timeout /t 2 >nul
endlocal
exit
