@echo off
setlocal
set NAME=KenshiTranslator
set VERSION=v1.3.0
set TARGET_DIR=%cd%

title Build %NAME% %VERSION%
mode con: cols=60 lines=20

echo ================================
echo   BUILD %NAME% %VERSION% STARTED
echo ================================
echo.

:: Очистка старых файлов
echo [INFO] Cleaning old files...
rmdir /s /q build dist __pycache__ >nul 2>&1
del *.spec >nul 2>&1
del "%NAME%.exe" >nul 2>&1
del "warn-%NAME%.txt" >nul 2>&1
del "xref-%NAME%.html" >nul 2>&1
del "%NAME%*.hash.txt" >nul 2>&1
echo [OK] Cleanup done
echo.

:: Сборка EXE
echo [INFO] Running PyInstaller...
pyinstaller --onefile --noconsole ^
 --name "%NAME%" ^
 --icon "%cd%\icons\icon.ico" ^
 --version-file "%cd%\info.txt" ^
 --add-data "%cd%\icons;icons" ^
 --add-data "%cd%\LICENSE.md;." ^
 --add-data "%cd%\panel_cfg.py;." ^
 --add-data "%cd%\panel_translate.py;." ^
 --add-data "%cd%\run_kenshi.py;." ^
 --add-data "%cd%\scan_mods.py;." ^
 --add-data "%cd%\sort_mods.py;." ^
 --add-data "%cd%\clear_mods.py;." ^
 --add-data "%cd%\panel_info.py;." ^
 "%cd%\GUI_translator.py"

:: Проверка результата
if exist "dist\%NAME%.exe" (
    echo [OK] Build successful
) else (
    echo [ERROR] Build failed! Check logs.
    timeout /t 5 >nul
    exit /b
)

:: Перемещение EXE
echo [INFO] Moving EXE to %TARGET_DIR%
move /Y "dist\%NAME%.exe" "%TARGET_DIR%\%NAME%.exe" >nul
echo [OK] %NAME%.exe moved to %TARGET_DIR%

:: Хеш SHA256 (с версией в имени)
echo [INFO] Calculating SHA256 hash...
certutil -hashfile "%TARGET_DIR%\%NAME%.exe" SHA256 > "%TARGET_DIR%\%VERSION%.hash.txt"
echo [OK] Hash saved to %VERSION%.hash.txt

:: Финальная очистка
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
