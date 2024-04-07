@echo off
SETLOCAL

echo Creating target folder...
if not exist executable mkdir executable

echo Creating virtual environment...
python -m venv build_env
if %errorlevel% neq 0 goto :error

echo Activating virtual environment...
call build_env\Scripts\activate.bat
if %errorlevel% neq 0 goto :error

echo Installing dependencies...
pip install pyinstaller
if %errorlevel% neq 0 goto :error

REM Add any other dependencies here with pip install

echo Running PyInstaller...
pyinstaller --onefile --windowed --icon=F:\toolscontainer\icons\convert.ico --name ToolsContainer-alpha F:\toolscontainer\executable_files\video_converter_executable.py --distpath executable\dist --workpath executable\build --specpath executable
if %errorlevel% neq 0 goto :error

echo Build completed successfully.
goto organize

:error
echo There was an error during the process.
goto cleanup

:organize
echo Organizing build artifacts...

REM Move the .exe file to the executable folder.
move executable\dist\VideoConverter.exe executable\
if %errorlevel% neq 0 goto cleanup

echo Cleaning up unnecessary files and folders...
for /d %%x in (executable\*) do if /i not "%%~nxx"=="ToolsContainer-alpha.exe" rmdir /s /q "%%x"
for %%x in (executable\*) do if /i not "%%~nxx"=="ToolsContainer-alpha" del "%%x"

echo Artifacts organized.
goto cleanup

:cleanup
echo Performing final cleanup...
if exist build_env call build_env\Scripts\deactivate.bat
if exist build_env rmdir /S /Q build_env
echo Final cleanup done.

:end
pause
ENDLOCAL