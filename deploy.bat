@echo off
setlocal
cd /d "%~dp0"

echo.
echo ===============================
echo    Word Family Rush - Deploy
echo ===============================
echo.

echo [1/3] Rebuilding game (index.html)...
python build.py
if errorlevel 1 goto builderr

echo.
echo [2/3] Saving your changes...
git add -A
git commit -m "Update %DATE% %TIME%" >nul 2>&1
if errorlevel 1 echo      (nothing new to commit - pushing current state)

echo.
echo [3/3] Uploading to GitHub...
git push
if errorlevel 1 goto pusherr

echo.
echo === DONE! Live in about a minute at: ===
echo     https://nikolasdrimmel.github.io/word-family-game/
echo.
echo Open the app on your iPhone (with internet) once to get the update.
echo.
pause
exit /b 0

:builderr
echo.
echo *** BUILD FAILED - read the message above (check families.txt / familias.txt). ***
echo.
pause
exit /b 1

:pusherr
echo.
echo *** UPLOAD FAILED. If a GitHub sign-in window opened, finish it, then run deploy again. ***
echo.
pause
exit /b 1
